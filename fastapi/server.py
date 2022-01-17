import io
import os
import json 
import pandas as pd
import numpy as np

from fastapi import FastAPI, File
import lightgbm as lgb
from lightgbm import LGBMClassifier
import joblib


app = FastAPI(
    title="Home Credit Default Risk",
    description="""Obtain information related to probability of a customer defaulting on loan.""",
    version="0.1.0",
)


def read_csv():

    df = pd.read_csv("datasets/df_customers_to_predict.csv")

    return df


@app.get("/api")
def root():
    return {"message": "Hello World"}


@app.get("/api/customers-id")
def customers_id():

    df = read_csv()
    customersId = df["SK_ID_CURR"].tolist()

    return {"customersId": customersId}


@app.get("/api/customers/{customer_id}")
def customers(customer_id: int):

    # reading the csv
    df = read_csv()

    # Defining the features to get
    COLUMNS = [
        "SK_ID_CURR", "CODE_GENDER", "DAYS_BIRTH", "DAYS_EMPLOYED",
        "CNT_CHILDREN", "FLAG_OWN_REALTY", "AMT_INCOME_TOTAL", 
        "AMT_CREDIT"
    ]

    # Filtering by customer id
    result = df[COLUMNS][df["SK_ID_CURR"] == customer_id].to_json(orient="records")
    
    # Serializing json 
    parsed = json.loads(result)
    json_object = json.dumps(parsed) 

    return json_object


@app.get("/api/predict/{customer_id}")
def predict(customer_id: int):

    # Loading the model
    model = joblib.load("model/model_1.0.2.pkl")

    # reading the csv
    df = read_csv()

    # Filtering by customer id
    df = df[df["SK_ID_CURR"] == customer_id]
    df.drop(columns=["SK_ID_CURR"], axis=1, inplace=True)

    # Predicting
    result = model.predict(df)
    result_proba = model.predict_proba(df)

    if result == 1:
        result = "No"
    else:
        result = "Yes"    

    return {"repay" : result, "probability" : result_proba}