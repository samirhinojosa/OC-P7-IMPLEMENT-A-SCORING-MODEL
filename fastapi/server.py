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
async def root():
    return {"message": "Hello World"}


@app.get("/customers-id")
async def customers_id():

    df = read_csv()
    customersId = df["SK_ID_CURR"].tolist()

    return {"customersId": customersId}


@app.get("/customers/{customer_id}")
def customers(customer_id: int):

    df = read_csv()

    df = df.head()
    #data = df[df["SK_ID_CURR"] == customer_id]
    #data = df[df["SK_ID_CURR"] == customer_id].to_json(orient="records")
    df = df.to_dict("records")
      
    # Serializing json  
    json_object = json.dumps(df) 
    


    return json_object #{"item_id": customer_id} #data.to_dict("records") #{"message": data}
    #return df.to_json(orient="records")