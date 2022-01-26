import streamlit as st
from PIL import Image
import requests


# Loading images to the website
icon = Image.open("images/favicon.ico")
image = Image.open("images/home-credit.png")


# General settings
st.set_page_config(
    page_title="Home credit Default Risk",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug" : None,
        "Get help" : "https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model",
        "About" : 
        '''
        Made with ❤️ by [@samirhinojosa](https://www.samirhinojosa.com/) in OpenClassRooms Data Scientist Training.

        For more information visit the following [link](https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model).
        '''
    }
)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True
)


# Page information
st.title("Home Credit - Default Risk")
# st.header("This is the header")
# st.subheader("This is the subheader")
# st.text("Esto es una prueba.")
# st.caption("This is a string that explains something above.")
# st.markdown('Streamlit is **_really_ cool**.')
# st.text("-------------FLAG-------------")

# Session for the API
def fetch(session, url):

    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

session = requests.Session()

@st.cache
def customer():
    # Getting customers Id
    data = fetch(session, f"http://fastapi:8008/api/customers")
    if data:
        return data["customersId"]
    else:
        return "Error"

def customer_details(id):
    # Getting customer's details
    data = fetch(session, f"http://fastapi:8008/api/customers/{id}")
    if data:
        return data
    else:
        return "Error"



# Sidebar section
st.sidebar.image(image)
msg_info = st.sidebar.info("Select a customer to **predict** whether he will **pay the loan**")
st.sidebar.markdown("🔎 **Customer selection**")
customer_selection_form = st.sidebar.form(key="customer_selection")
customer_id = customer_selection_form.selectbox(
    "Customer ID", customer()
)
result = customer_selection_form.form_submit_button(label="Results")

if result:
    
    data = customer_details(customer_id)
    customer_container = st.container()

    with customer_container:

        st.subheader("Client's information")

        col1_cc, col2_cc, col3_cc, col4_cc = customer_container.columns([2, 1, 1, 1])

        with col1_cc:
            import numpy as np
            data2 = np.random.randn(10, 1)
            col1_cc.line_chart(data2)
        
        with col2_cc:
            st.markdown("**Customer id:**")
            st.caption(data["customerId"])
            st.markdown("**Children:**")
            st.caption(data["children"])
            st.markdown("**Years employed:**")
            st.caption(data["yearsEmployed"])

        with col3_cc:
            st.markdown("**Gender:**")
            st.caption(data["gender"])
            st.markdown("**Own realty:**")
            st.caption(data["ownRealty"])
            st.markdown("**Total income:**")
            st.caption(data["totalIncome"])

        with col4_cc:
            st.markdown("**Age:**")
            st.caption(data["age"])
            st.markdown("**Own Care:**")
            st.caption(data["ownCar"])
            st.markdown("**Current credit:**")
            st.caption(data["credit"])







# st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

# expander = st.expander("See explanation", expanded=True)

# with expander:
#      st.write("""
#          The chart above shows some numbers I picked for you.
#          I rolled actual dice for these, so they're *guaranteed* to
#          be random.
#      """)
#      st.image("https://static.streamlit.io/examples/dice.jpg")

#def main():
# if __name__ == '__main__':
#     main()