import streamlit as st
import requests
from PIL import Image
import plotly.graph_objects as go
import plotly.figure_factory as ff

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

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

config = {
    "displayModeBar": False,
    "displaylogo": False
}


########################################################
# Page information
########################################################
st_title = '<h1 style="color:#C80F2E; margin-bottom:0; padding: 1.25rem 0px 0rem;">Home Credit - Default Risk</h1>'
st_title_hr = '<hr style="background-color:#C80F2E; width:60%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)


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
    #response = fetch(session, f"http://fastapi:8008/api/clients")
    response = requests.get("http://fastapi:8008/api/clients").json()
    if response:
        return response["clientsId"]
    else:
        return "Error"

def client_details(id):
    # Getting client's details
    response = fetch(session, f"http://fastapi:8008/api/clients/{id}")
    if response:
        return response
    else:
        return "Error"

def client_prediction(id):
    # Getting client's prediction
    response = fetch(session, f"http://fastapi:8008/api/predictions/clients/{id}")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_ages():
    # Getting General statistics about ages
    response = fetch(session, f"http://fastapi:8008/api/statistics/ages")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_years_employed():
    # Getting General statistics about ages
    response = fetch(session, f"http://fastapi:8008/api/statistics/yearsEmployed")
    if response:
        return response
    else:
        return "Error"


########################################################
# Sidebar section
########################################################
sb = st.sidebar # defining the sidebar
sb.image(image)

sb.markdown("🛰️ **Navigation**")
page_names = ["🏠 Home", "⚙️ Client prediction"]
page = sb.radio("", page_names, index=0)
sb.write('<style>.css-1p2iens { margin-bottom: 0px !important; min-height: 0 !important;}</style>', unsafe_allow_html=True)

msg_sb = sb.info("In this section, you can **navigate** through the **Home page** where you'll find " \
                "information related with the project. At the same time, you can go to the **Client prediction page**, " \
                "where you can make predictions to know whether client will honor on the loan based on his information.")

if page == "🏠 Home":

    st.header("This is the header")
    st.subheader("This is the subheader")
    st.text("Esto es una prueba.")
    st.caption("This is a string that explains something above.")
    st.markdown('Streamlit is **_really_ cool**.')
    st.text("-------------FLAG-------------")

else:

    client_selection_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🔎 Client selection</h3>'
    st.markdown(client_selection_title, unsafe_allow_html=True)

    client_container_selection = st.container()
    #col1_cs, col2_cs = client_container_selection.columns([1, 2])
    col1_cs, col2_cs, col3_cs = client_container_selection.columns([1, 1, 2])

    with col1_cs:

        client_selection_form = st.form(key="client_selection")
        client_id = client_selection_form.selectbox(
            "Client Id list", client()
        )
        
        result = client_selection_form.form_submit_button(label="Results")
    
    with col2_cs:

        msg_client_selection = st.info("Select a client to **obtain** " \
                                "information related to **probability** of a client **honoring on the loan**. " \
                                "In addition, you can analyze client information against the general data. ")

    with col3_cs:

        st.text(" ")

    if result:
    
        data = client_details(client_id)
        client_container_prediction, container_general_statistics = (st.container() for i in range(2))

        with client_container_prediction:

            client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📋 Client information</h3>'
            st.markdown(client_information_title, unsafe_allow_html=True)

            prediction = client_prediction(client_id)
            prediction_value = round(float(list(prediction["probability"].keys())[0]), 3) * 100

            if prediction["repay"] == "Yes":
                st.success("Based on the client's information, the credit application is **accepted!**")
            else:
                if prediction_value > 50:
                    st.warning("It is necessary to **analyze more in details** the client's information to accept the credit")
                else:
                    st.error("Based on the client's information, the credit application is ** not accepted!**")

            col1_cp, col2_cp, col3_cp, col4_cp = client_container_prediction.columns([2, 1, 1, 1])

            with col1_cp:
                
                figP = go.Figure(
                        go.Indicator(
                            mode = "gauge+number",
                            value = prediction_value,
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
                    annotations=[
                        go.layout.Annotation(
                            text=f"<b>Probability that the client will pay his loan</b>",
                            x=0.5, xanchor="center", xref="paper",
                            y=0, yanchor="bottom", yref="paper",
                            showarrow=False,
                        )
                    ]
                )
                
                col1_cp.plotly_chart(figP, config=config, use_container_width=True)

                
            with col2_cp:
                st.caption("&nbsp;")
                st.markdown("**Client id:**")
                st.caption(data["clientId"])
                st.markdown("**Children:**")
                st.caption(data["children"])
                st.markdown("**Years employed:**")
                st.caption(data["yearsEmployed"])

            with col3_cp:
                st.caption("&nbsp;")
                st.markdown("**Gender:**")
                st.caption(data["gender"])
                st.markdown("**Own realty:**")
                st.caption(data["ownRealty"])
                st.markdown("**Total income:**")
                total_income = "$ {:,.2f}".format(data["totalIncome"])
                st.caption(total_income)

            with col4_cp:
                st.caption("&nbsp;")
                st.markdown("**Age:**")
                st.caption(data["age"])
                st.markdown("**Own car:**")
                st.caption(data["ownCar"])
                st.markdown("**Current credit:**")
                current_credit = "$ {:,.2f}".format(data["credit"])
                st.caption(current_credit)

        with container_general_statistics:

            client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📊 General statistics</h3>'
            st.markdown(client_information_title, unsafe_allow_html=True)

            st.info("Below, you can see some general statistics about clients who " \
                    "repaid and do not repaid the loan")
            


            col1_gs, col2_gs = container_general_statistics.columns(2)

            group_labels = ["Repaid", "Not repaid"]
            colors=["Green", "Red"]

            with col1_gs:

                ages = statistical_ages()
                ages_repaid = ages["ages_repaid"]
                ages_not_repaid = ages["ages_not_repaid"]
                ages_repaid_list = [int(key) for key, val in ages_repaid.items() for _ in range(val)]
                ages_not_repaid_list = [int(key) for key, val in ages_not_repaid.items() for _ in range(val)]

                fig_ages = ff.create_distplot([ages_repaid_list, ages_not_repaid_list], 
                                            group_labels, show_hist=False, show_rug=False, 
                                            colors=colors)
                fig_ages.update_layout(
                    paper_bgcolor="white",
                    font={
                        "family": "sans serif"
                    },
                    autosize=False,
                    width=500,
                    height=360,
                    margin=dict(
                        l=50, r=50, b=0, t=20, pad=0
                    ),
                    title={
                        "text" : "Client's age vs Current clients",
                        "y" : 1,
                        "x" : 0.45,
                        "xanchor" : "center",
                        "yanchor" : "top"
                    },
                    xaxis_title="Ages",
                    yaxis_title="Density",
                    legend={
                        "traceorder" : "normal"
                    }
                )
                fig_ages.add_vline(x=data["age"], line_width=3,
                                line_dash="dash", line_color="green", annotation_text="Client's age")

                col1_gs.plotly_chart(fig_ages, config=config, use_container_width=True)

            
            with col2_gs:
                
                years_employed = statistical_years_employed()
                years_employed_repaid = years_employed["years_employed_repaid"]
                years_employed_not_repaid = years_employed["years_employed_not_repaid"]
                years_employed_repaid_list = [int(key) for key, val in years_employed_repaid.items() for _ in range(val)]
                years_employed_not_repaid_list = [int(key) for key, val in years_employed_not_repaid.items() for _ in range(val)]

                fig_years_worked = ff.create_distplot([years_employed_repaid_list, years_employed_not_repaid_list], 
                                            group_labels, show_hist=False, show_rug=False, 
                                            colors=colors)

                fig_years_worked.update_layout(
                    paper_bgcolor="white",
                    font={
                        "family": "sans serif"
                    },
                    autosize=False,
                    width=500,
                    height=360,
                    margin=dict(
                        l=50, r=50, b=0, t=20, pad=0
                    ),
                    title={
                        "text" : "Years employed by the client vs Current clients",
                        "y" : 1,
                        "x" : 0.45,
                        "xanchor" : "center",
                        "yanchor" : "top"
                    },
                    xaxis_title="Ages",
                    yaxis_title="Density",
                    legend={
                        "traceorder" : "normal"
                    }
                )
                fig_years_worked.add_vline(x=data["yearsEmployed"], line_width=3,
                                line_dash="dash", line_color="green", annotation_text="Years employed by the client")

                col2_gs.plotly_chart(fig_years_worked, config=config, use_container_width=True)
