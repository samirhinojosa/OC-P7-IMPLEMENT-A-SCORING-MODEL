import streamlit as st
import requests
from PIL import Image
import plotly.graph_objects as go

########################################################
# Loading images to the website
########################################################
icon = Image.open("images/favicon.ico")
image = Image.open("images/home-credit.png")


########################################################
# General settings
########################################################
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
        Made with ❤️ by [@samirhinojosa](https://www.samirhinojosa.com/) 
        in OpenClassRooms Data Scientist Training.

        For more information visit the following 
        [link](https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model).
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


########################################################
# Page information
########################################################
st_title = '<h1 style="color:#C80F2E;">Home Credit - Default Risk</h1>'
st.markdown(st_title, unsafe_allow_html=True)


#st.title("Home Credit - Default Risk")



# st.header("This is the header")
# st.subheader("This is the subheader")
# st.text("Esto es una prueba.")
# st.caption("This is a string that explains something above.")
# st.markdown('Streamlit is **_really_ cool**.')
# st.text("-------------FLAG-------------")


########################################################
# Session for the API
########################################################
def fetch(session, url):

    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

session = requests.Session()


########################################################
# Functions to call the EndPoints
########################################################
@st.cache
def client():
    # Getting clients Id
    data = fetch(session, f"http://fastapi:8008/api/clients")
    if data:
        return data["clientsId"]
    else:
        return "Error"

def client_details(id):
    # Getting client's details
    data = fetch(session, f"http://fastapi:8008/api/clients/{id}")
    if data:
        return data
    else:
        return "Error"

def client_prediction(id):
    # Getting client's prediction
    data = fetch(session, f"http://fastapi:8008/api/predictions/clients/{id}")
    if data:
        return data
    else:
        return "Error"


########################################################
# Sidebar section
########################################################
st.sidebar.image(image)
#msg_info = st.sidebar.info("Select a client to **predict** whether he will **pay the loan**")
msg_info = st.sidebar.info("Select a client to **obtain** " \
                "information related to **probability** of a client **defaulting on loan**")
st.sidebar.markdown("🔎 **Client selection**")
client_selection_form = st.sidebar.form(key="client_selection")
client_id = client_selection_form.selectbox(
    "Client ID", client()
)
result = client_selection_form.form_submit_button(label="Results")

if result:
    
    data = client_details(client_id)
    client_container = st.container()

    with client_container:

        st.subheader("Client's information")

        col1_cc, col2_cc, col3_cc, col4_cc = client_container.columns([2, 1, 1, 1])

        with col1_cc:

            prediction = client_prediction(client_id)

            figP = go.Figure(
                    go.Indicator(
                        mode = "gauge+number",
                        value = round(float(list(prediction["probability"].keys())[0]), 3) * 100,
                        domain = {"x": [0, 1], "y": [0, 1]},
                        gauge = {
                            "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "darkblue", "tick0": 0, "dtick": 20},
                            "bar": {"color": "LawnGreen"},
                            "bgcolor": "white",
                            "steps": [
                                {"range": [0, 35], "color": "Red"},
                                {"range": [35, 65], "color": "Orange"},
                                {"range": [65, 100], "color": "Green"}
                            ],
                        }
                    )   
                )

            figP.update_layout(
                paper_bgcolor="white",
                font={
                    "color": "darkblue",
                    "family": "sans serif"
                },
                autosize=False,
                width=500,
                height=300,
                margin=dict(
                    l=50, r=50, b=0, t=0, pad=0
                ),
            )
            
            col1_cc.plotly_chart(figP, use_container_width=True)

        with col2_cc:
            st.markdown("**Client id:**")
            st.caption(data["clientId"])
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
            st.markdown("**Own car:**")
            st.caption(data["ownCar"])
            st.markdown("**Current credit:**")
            st.caption(data["credit"])