from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pycaret.classification import *
import pandas as pd
from pydantic import BaseModel
import logging

logging.basicConfig(
    filename="applogs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = FastAPI()

loaded_best_pipeline = load_model("models/model")


class InputData(BaseModel):
    Gender: str
    Age_at_diagnosis: str
    Primary_Diagnosis: str
    Race: str
    IDH1: str
    TP53: str
    ATRX: str
    PTEN: str
    EGFR: str
    CIC: str
    MUC16: str
    PIK3CA: str
    NF1: str
    PIK3R1: str
    FUBP1: str
    RB1: str
    NOTCH1: str
    BCOR: str
    CSMD3: str
    SMARCA4: str
    GRIN2A: str
    IDH2: str
    FAT4: str
    PDGFRA: str


def preprocess(data: InputData):
    data_dict = data.dict()
    data = pd.DataFrame([data_dict])

    age_list = []
    for date in data["Age_at_diagnosis"]:
        if ("days" in date) & ("years" in date):
            age = 365 * int(date.split(" ")[0]) + int(date.split(" ")[2])
            age_list.append(age)
        elif "years" in date:
            age = 365 * int(date.split(" ")[0])
            age_list.append(age)
        elif "days" in date:
            age = int(date.split(" ")[0])
            age_list.append(age)
        else:
            age_list.append(None)

    data["Age_at_diagnosis"] = age_list
    return data


@app.post("/predict")
def make_prediction(data: InputData):
    logger.info("Received request for prediction")
    data = preprocess(data)
    try:
        prediction = loaded_best_pipeline.predict(data)
        return {"prediction": prediction[0]}
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
