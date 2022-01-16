import io
import os
import pandas as pd
import numpy as np

from fastapi import FastAPI, File

app = FastAPI(
    title="Home Credit Default Risk",
    description="""Obtain information related to probability of a customer defaulting on loan.""",
    version="0.1.0",
)


def is_debug(debug=True):

    if debug:
        df = pd.read_csv(r"datasets/df_processed.csv", nrows=10000)
    else:
        df = pd.read_csv(r"datasets/df_processed.csv")

    return df


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/customers-id")
async def customers_id():

    df = is_debug(True)
    customersId = df["SK_ID_CURR"].tolist()

    return {"customersId": customersId}