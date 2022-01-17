import io
import os
import json 
import pandas as pd
import numpy as np

from fastapi import FastAPI, File

app = FastAPI(
    title="Home Credit Default Risk",
    description="""Obtain information related to probability of a customer defaulting on loan.""",
    version="0.1.0",
)


def read_csv():

    df = pd.read_csv("datasets/df_customers_to_predict.csv")

    return df


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/customers-id")
def customers_id():

    df = read_csv()
    customersId = df["SK_ID_CURR"].tolist()

    return {"customersId": customersId}


@app.get("/customers/{customer_id}")
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