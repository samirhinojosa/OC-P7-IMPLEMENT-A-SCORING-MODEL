import streamlit as st
import requests


st.set_page_config(page_title="Credit Score Service", page_icon="🤖")
st.title("Welcome to Credit Score Service!")


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


session = requests.Session()


def main():

    data = fetch(session, f"http://fastapi:8008/api/customers")
    if data:
        st.dataframe(data)
    else:
        st.error("Error")


if __name__ == '__main__':
    main()

# def main():
#     st.set_page_config(page_title="Example App", page_icon="🤖")
#     st.title("Get Image by Id")
#     session = requests.Session()
#     with st.form("my_form"):
#         index = st.number_input("ID", min_value=0, max_value=100, key="index")

#         submitted = st.form_submit_button("Submit")

#         if submitted:
#             st.write("Result")
#             data = fetch(session, f"https://picsum.photos/id/{index}/info")
#             if data:
#                 st.image(data['download_url'], caption=f"Author: {data['author']}")
#             else:
#                 st.error("Error")


# if __name__ == '__main__':
#     main()








#response = requests.get("http://localhost:8008/api/customers")
#session = requests.Session()
#data = fetch(session, f"http://localhost:8008/api/customers")
#if data:
 #   print(response.json())
    #data_table1 = pd.DataFrame(data.json())
    #st.write(data_table1)
#else:
 #    st.error("Error XX")

# json = requests.get("http://fastapi:8008/api/customers").json()

# st.dataframe(json)




#import streamlit as st
#import requests
#import pandas as pd


# def fetch(session, url):
#     try:
#         result = session.get(url)
#         return result.json()
#     except Exception:
#         return {}


# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))


# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })

# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option

#







# import requests
# import pandas as pd

# # http://127.0.01:5000/ is from the flask api
# response = requests.get("http://localhost:8008/api/customers")
# #print(response.json())
# data_table1 = pd.DataFrame(response.json())
# st.write(data_table1)


