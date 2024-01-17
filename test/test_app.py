import pytest
from httpx import AsyncClient
from src.backend.app import app


@pytest.mark.anyio
async def test_read_main():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"Status": "Healthy"}


@pytest.mark.anyio
async def test_predict():
    data = {
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
    }
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/predict", json=data)
    assert response.status_code == 200
    assert "prediction" in response.json()
