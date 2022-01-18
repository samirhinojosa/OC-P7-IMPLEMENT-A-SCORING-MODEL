import io
import os
import json 
import pandas as pd
import numpy as np
from datetime import date, timedelta

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


@app.get("/api/customers")
async def customers_id():

    df = read_csv()
    customersId = df["SK_ID_CURR"].tolist()

    return {"customersId": customersId}


@app.get("/api/customers/{id}")
async def customers(id: int):

    # Defining the features to get
    COLUMNS = [
        "SK_ID_CURR", "CODE_GENDER", "DAYS_BIRTH", "DAYS_EMPLOYED",
        "CNT_CHILDREN", "FLAG_OWN_REALTY", "AMT_INCOME_TOTAL", 
        "AMT_CREDIT"
    ]

    # Reading the dataset
    df = read_csv()

    # Filtering by customer id
    df = df[COLUMNS][df["SK_ID_CURR"] == id]
    
    for col in df.columns:
        globals()[col] = df.iloc[0, df.columns.get_loc(col)]
    
    customer = {
        "customerId" : int(SK_ID_CURR),
        "gender" : "Man" if int(CODE_GENDER) == 0 else "Woman",
        "age" : calculate_years(int(DAYS_BIRTH)),
        "yearsEmployed" : calculate_years(int(DAYS_EMPLOYED)),
        "children" : int(CNT_CHILDREN),
        "ownRealty" : "No" if int(FLAG_OWN_REALTY) == 0 else "Yes",
        "totalIncome" : float(AMT_INCOME_TOTAL),
        "credit" : float(AMT_CREDIT)
    }
    
    return customer


@app.get("/api/predictions/customers/{id}")
async def predict(id: int):

    # Loading the model
    model = joblib.load("model/model_1.0.2.pkl")

    # reading the csv
    df = read_csv()

    # Filtering by customer id
    df = df[df["SK_ID_CURR"] == id]
    df.drop(columns=["SK_ID_CURR"], axis=1, inplace=True)

    # Predicting
    result = model.predict(df)
    result_proba = model.predict_proba(df)

    if result == 1:
        result = "No"
    else:
        result = "Yes"    

    return {"repay" : result, "probability" : result_proba}


def calculate_years(days):

    today = date.today()
    initial_date = today - timedelta(abs(days))
    years = today.year - initial_date.year - ((today.month, today.day) < (initial_date.month, initial_date.day))

    return years