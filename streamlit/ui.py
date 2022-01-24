import streamlit as st

st.title("Hola mundo")



import requests
import pandas as pd

# http://127.0.01:5000/ is from the flask api
response = requests.get("http://localhost:8008/api/customers")
#print(response.json())
data_table1 = pd.DataFrame(response.json())
st.write(data_table1)