import io
import os
import json 
import gc
import pandas as pd
import numpy as np
from datetime import date, timedelta
from fastapi import FastAPI, File
import lightgbm as lgb
from lightgbm import LGBMClassifier
import joblib


app = FastAPI(
    title="Home Credit Default Risk",
    description="""Obtain information related to probability of a client defaulting on loan.""",
    version="0.1.0",
)


def calculate_years(days):
    """
    Method used to calculate years based on date (today - quantity of days).

    Parameters:
    -----------------
        days (int): Numbers of day to rest of today

    Returns:
    -----------------
        years (int): Numbers of years
    """

    today = date.today()
    initial_date = today - timedelta(abs(days))
    years = today.year - initial_date.year - ((today.month, today.day) < (initial_date.month, initial_date.day))

    return years


# Columns to read on CSVs
COLUMNS = [
    "SK_ID_CURR", "CODE_GENDER", "DAYS_BIRTH", "DAYS_EMPLOYED",
    "CNT_CHILDREN", "FLAG_OWN_REALTY", "FLAG_OWN_CAR",
    "AMT_INCOME_TOTAL", "AMT_CREDIT"
]

# Reading the csv
df_clients_to_predict = pd.read_csv("datasets/df_clients_reduced_to_predict.csv")
df_optimized = pd.read_csv("datasets/df_optimized_and_reduced.csv")

df_optimized["AGE"] = df_optimized["DAYS_BIRTH"].apply(lambda x: calculate_years(x))
df_optimized["YEARS_EMPLOYED"] = df_optimized["DAYS_EMPLOYED"].apply(lambda x: calculate_years(x))

df_optimized_by_target_repaid = df_optimized[df_optimized["TARGET"] == 0]
df_optimized_by_target_not_repaid = df_optimized[df_optimized["TARGET"] == 1]

# Deleting and freeing memory
del df_optimized
gc.collect()


@app.get("/api/clients")
async def clients_id():
    """ 
    EndPoint to get all clients id
    """

    clientsId = df_clients_to_predict["SK_ID_CURR"].tolist()

    return {"clientsId": clientsId}


@app.get("/api/clients/{id}")
async def clients(id: int):
    """ 
    EndPoint to get client's detail 
    """ 
    
    # Filtering by clients id
    df_by_id = df_clients_to_predict[COLUMNS][df_clients_to_predict["SK_ID_CURR"] == id]
    
    for col in df_by_id.columns:
        globals()[col] = df_by_id.iloc[0, df_by_id.columns.get_loc(col)]
    
    client = {
        "clientId" : int(SK_ID_CURR),
        "gender" : "Man" if int(CODE_GENDER) == 0 else "Woman",
        "age" : calculate_years(int(DAYS_BIRTH)),
        "yearsEmployed" : calculate_years(int(DAYS_EMPLOYED)),
        "children" : int(CNT_CHILDREN),
        "ownRealty" : "No" if int(FLAG_OWN_REALTY) == 0 else "Yes",
        "ownCar" : "No" if int(FLAG_OWN_CAR) == 0 else "Yes",
        "totalIncome" : float(AMT_INCOME_TOTAL),
        "credit" : float(AMT_CREDIT)
    }

    return client


@app.get("/api/predictions/clients/{id}")
async def predict(id: int):
    """ 
    EndPoint to get the probability honor/compliance of a client
    """ 

    # Loading the model
    model = joblib.load("models/model_p7.pkl")

    # Filtering by client id
    df_prediction_by_id = df_clients_to_predict[df_clients_to_predict["SK_ID_CURR"] == id]
    df_prediction_by_id = df_prediction_by_id.drop(columns=["SK_ID_CURR"])

    # Predicting
    result = model.predict(df_prediction_by_id)
    result_proba = model.predict_proba(df_prediction_by_id)

    if (int(result[0]) == 0):
         result = "Yes"
    else:
         result = "No"    

    return {"repay" : result, "probability" : result_proba}


@app.get("/api/statistics/ages")
async def statistical_age():
    """ 
    EndPoint to get some statistics - ages
    """

    ages_data_repaid = df_optimized_by_target_repaid.groupby("AGE").size()
    ages_data_repaid = pd.DataFrame(ages_data_repaid).reset_index()
    ages_data_repaid.columns = ["AGE", "AMOUNT"]
    ages_data_repaid = ages_data_repaid.set_index("AGE").to_dict()["AMOUNT"]

    ages_data_not_repaid = df_optimized_by_target_not_repaid.groupby("AGE").size()
    ages_data_not_repaid = pd.DataFrame(ages_data_not_repaid).reset_index()
    ages_data_not_repaid.columns = ["AGE", "AMOUNT"]
    ages_data_not_repaid = ages_data_not_repaid.set_index("AGE").to_dict()["AMOUNT"]

    return {"ages_repaid" : ages_data_repaid, "ages_not_repaid" : ages_data_not_repaid}


@app.get("/api/statistics/yearsEmployed")
async def statistical_years_employed():
    """ 
    EndPoint to get some statistics - years employed
    """

    years_employed_data_repaid = df_optimized_by_target_repaid.groupby("YEARS_EMPLOYED").size()
    years_employed_data_repaid = pd.DataFrame(years_employed_data_repaid).reset_index()
    years_employed_data_repaid.columns = ["YEARS_EMPLOYED", "AMOUNT"]
    years_employed_data_repaid = years_employed_data_repaid.set_index("YEARS_EMPLOYED").to_dict()["AMOUNT"]

    years_employed_data_not_repaid = df_optimized_by_target_not_repaid.groupby("YEARS_EMPLOYED").size()
    years_employed_data_not_repaid = pd.DataFrame(years_employed_data_not_repaid).reset_index()
    years_employed_data_not_repaid.columns = ["YEARS_EMPLOYED", "AMOUNT"]
    years_employed_data_not_repaid = years_employed_data_not_repaid.set_index("YEARS_EMPLOYED").to_dict()["AMOUNT"]

    return {"years_employed_repaid" : years_employed_data_repaid, "years_employed_not_repaid" : years_employed_data_not_repaid}