import os
import sys

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pycaret.classification import load_model, predict_model
from pydantic import create_model
from sqlalchemy.orm import Session
from src.backend.dependencies import get_current_user
from src.backend.models import UserOut
from src.db.crud.items import create_item
from src.db.crud.users import decrement_user_balance
from src.db.database import get_db

ml_router = APIRouter()

rcf_model = load_model(os.path.join(sys.path[0], "artifacts/models/rcf"))
lda_model = load_model(os.path.join(sys.path[0], "artifacts/models/lda"))
gnb_model = load_model(os.path.join(sys.path[0], "artifacts/models/gnb"))


input_model = create_model(
    "lr_api_input",
    **{
        "Gender": "Male",
        "Age_at_diagnosis": 26747.0,
        "Race": "white",
        "IDH1": "NOT_MUTATED",
        "TP53": "NOT_MUTATED",
        "ATRX": "NOT_MUTATED",
        "PTEN": "MUTATED",
        "EGFR": "MUTATED",
        "CIC": "NOT_MUTATED",
        "MUC16": "NOT_MUTATED",
        "PIK3CA": "NOT_MUTATED",
        "NF1": "NOT_MUTATED",
        "PIK3R1": "NOT_MUTATED",
        "FUBP1": "NOT_MUTATED",
        "RB1": "NOT_MUTATED",
        "NOTCH1": "NOT_MUTATED",
        "BCOR": "NOT_MUTATED",
        "CSMD3": "NOT_MUTATED",
        "SMARCA4": "NOT_MUTATED",
        "GRIN2A": "NOT_MUTATED",
        "IDH2": "NOT_MUTATED",
        "FAT4": "NOT_MUTATED",
        "PDGFRA": "NOT_MUTATED",
    },
)

output_model = create_model("lr_api_output", prediction="GBM")

model_prices = {"rcf": 100, "lda": 200, "gnb": 300}


@ml_router.get("/price")
def model_list():
    return {"models": {"rcf": 100, "lda": 200, "gnb": 300}}


@ml_router.post("/model/{model_name}", response_model=output_model)
def predict(
    model_name: str,
    data: input_model,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.balance < model_prices.get(model_name, 0):
        raise HTTPException(status_code=400, detail="Insufficient funds for RCF model")
    if current_user.balance < model_prices.get(model_name, 1):
        raise HTTPException(status_code=400, detail="Insufficient funds for LDA model")
    if current_user.balance < model_prices.get(model_name, 2):
        raise HTTPException(status_code=400, detail="Insufficient funds for GNB model")

    decrement_user_balance(db, current_user.username, model_prices.get(model_name, 0))

    item_data = data.dict()
    data = pd.DataFrame([data.dict()])
    if model_name == "rcf":
        predictions = predict_model(rcf_model, data=data)
    elif model_name == "lda":
        predictions = predict_model(lda_model, data=data)
    elif model_name == "gnb":
        predictions = predict_model(gnb_model, data=data)
    else:
        raise HTTPException(status_code=400, detail="Invalid model name")

    item_data_db = {
        "gender": item_data["Gender"],
        "age_at_diagnosis": item_data["Age_at_diagnosis"],
        "race": item_data["Race"],
        "idh1": item_data["IDH1"],
        "tp53": item_data["TP53"],
        "atrx": item_data["ATRX"],
        "pten": item_data["PTEN"],
        "egfr": item_data["EGFR"],
        "cic": item_data["CIC"],
        "muc16": item_data["MUC16"],
        "pik3ca": item_data["PIK3CA"],
        "nf1": item_data["NF1"],
        "pik3r1": item_data["PIK3R1"],
        "fubp1": item_data["FUBP1"],
        "rb1": item_data["RB1"],
        "notch1": item_data["NOTCH1"],
        "bcor": item_data["BCOR"],
        "csmd3": item_data["CSMD3"],
        "smarca4": item_data["SMARCA4"],
        "grin2a": item_data["GRIN2A"],
        "idh2": item_data["IDH2"],
        "fat4": item_data["FAT4"],
        "pdgfra": item_data["PDGFRA"],
        "prediction": predictions["prediction_label"].iloc[0],
        "owner_id": current_user.id,
    }
    create_item(db, item_data_db)

    return {"prediction": predictions["prediction_label"].iloc[0]}
