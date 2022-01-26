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
st.title("Home Credit - Default Risk")
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




fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = 420,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed", 'font': {'size': 24}},
    delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': 'cyan'},
            {'range': [250, 400], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 490}}))

fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})





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

            import numpy as np
            #data2 = np.random.randn(10, 1)
            #col1_cc.line_chart(data2)
            # Plot!


            prediction = client_prediction(client_id)
            col1_cc.write(round(float(list(prediction["probability"].keys())[0]), 3) * 100)

            # fig2 = go.Figure()

            # fig2.add_trace(go.Indicator(
            #     value = float(list(prediction["probability"].keys())[0])*100,
            #     delta = {'reference': float(list(prediction["probability"].keys())[0])},
            #     gauge = {
            #         'axis': {'visible': False}},
            #     domain = {'row': 0, 'column': 0}))
            # fig2.update_layout(
            #     grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
            #     template = {'data' : {'indicator': [{
            #         'title': {'text': "Speed"},
            #         'mode' : "number+delta+gauge",
            #         'delta' : {'reference': float(list(prediction["probability"].keys())[0])}}]
            #         }
            #     }
            # )



            #col1_cc.plotly_chart(fig2, use_container_width=True)
            #col1_cc.plotly_chart(fig, use_container_width=True)



            plot_bgcolor = "#def"
            quadrant_colors = [plot_bgcolor, "#2bad4e", "#eff229", "#f25829"] 
            quadrant_text = ["", "<b>High</b>", "<b>Medium</b>", "<b>Low</b>"]

            n_quadrants = len(quadrant_colors) - 1

            current_value = round(float(list(prediction["probability"].keys())[0]), 3) * 100
            min_value = 0
            max_value = 100
            hand_length = np.sqrt(2) / 4
            hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

            fig3 = go.Figure(
                data=[
                    go.Pie(
                        values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                        rotation=90,
                        hole=0.5,
                        marker_colors=quadrant_colors,
                        text=quadrant_text,
                        textinfo="text",
                        hoverinfo="skip",
                    ),
                ],
                layout=go.Layout(
                    showlegend=False,
                    margin=dict(b=0,t=10,l=10,r=10),
                    width=380,
                    height=250,
                    paper_bgcolor=plot_bgcolor,
                    annotations=[
                        go.layout.Annotation(
                            text=f"<b>IOT sensot value:</b><br>{current_value} units",
                            x=0.5, xanchor="center", xref="paper",
                            y=0.25, yanchor="bottom", yref="paper",
                            showarrow=False,
                        )
                    ],
                    shapes=[
                        go.layout.Shape(
                            type="circle",
                            x0=0.48, x1=0.52,
                            y0=0.48, y1=0.52,
                            fillcolor="#333",
                            line_color="#333",
                        ),
                        go.layout.Shape(
                            type="line",
                            x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                            y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                            line=dict(color="#333", width=4)
                        )
                    ]
                )
            )

            col1_cc.plotly_chart(fig3, use_container_width=True)











        
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