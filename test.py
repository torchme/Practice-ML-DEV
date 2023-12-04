import requests

url = "http://localhost:8000/predict"

data = {
    "Gender": "Male",
    "Age_at_diagnosis": "51 years 108 days",
    "Primary_Diagnosis": "Oligodendroglioma, NOS",
    "Race": "white",
    "IDH1": "MUTATED",
    "TP53": "NOT_MUTATED",
    "ATRX": "NOT_MUTATED",
    "PTEN": "NOT_MUTATED",
    "EGFR": "NOT_MUTATED",
    "CIC": "NOT_MUTATED",
    "MUC16": "NOT_MUTATED",
    "PIK3CA": "MUTATED",
    "NF1": "NOT_MUTATED",
    "PIK3R1": "NOT_MUTATED",
    "FUBP1": "MUTATED",
    "RB1": "NOT_MUTATED",
    "NOTCH1": "NOT_MUTATED",
    "BCOR": "NOT_MUTATED",
    "CSMD3": "NOT_MUTATED",
    "SMARCA4": "NOT_MUTATED",
    "GRIN2A": "NOT_MUTATED",
    "IDH2": "NOT_MUTATED",
    "FAT4": "NOT_MUTATED",
    "PDGFRA": "NOT_MUTATED"
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")