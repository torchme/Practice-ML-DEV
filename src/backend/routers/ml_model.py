import os
import sys

import pandas as pd
from fastapi import APIRouter, HTTPException
from pycaret.classification import load_model, predict_model
from pydantic import create_model

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


@ml_router.get("/")
def model_list():
    return {"models": ["rcf", "lda", "gnb"]}


@ml_router.post("/model/{model_name}", response_model=output_model)
def predict(model_name: str, data: input_model):
    data = pd.DataFrame([data.dict()])
    if model_name == "rcf":
        predictions = predict_model(rcf_model, data=data)
    elif model_name == "lda":
        predictions = predict_model(lda_model, data=data)
    elif model_name == "gnb":
        predictions = predict_model(gnb_model, data=data)
    else:
        raise HTTPException(status_code=400, detail="Invalid model name")
    return {"prediction": predictions["prediction_label"].iloc[0]}
