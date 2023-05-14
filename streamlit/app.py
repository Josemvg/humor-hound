import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import streamlit as st
import hydralit_components as hc

st.set_page_config(page_title="Humor Hound",
                   page_icon=":dog:",
                   layout="centered")

st.title('Humor Hound :dog: :mag:')
st.markdown("""
            Welcome to Humor Hound! A Deep Learning model that helps identify
            whether a news' headline is sarcastic or not!
            """)

# fastapi endpoint
url = 'http://127.0.0.1:8000'
endpoint = '/predict'

@st.cache_data(show_spinner="Analyzing headline...")
def process(user_input: str, server_url: str):
    m = MultipartEncoder(
        fields={'user_input': user_input}
        )
    
    r = requests.post(server_url,
                      data=m,
                      params=m.fields,
                      headers={"Content-type": m.content_type},
                      timeout=8000)

    return r.json()

with st.container():  
    headline = st.text_input(label="Write your headline here!")

    theme_sarcastic = {'bgcolor': '#F3BFFF','title_color': 'purple','progress_color': 'purple','content_color': 'purple','icon_color': 'purple', 'icon': 'fa fa-exclamation-circle'}
    theme_normal = {'bgcolor': '#CDD7FF','title_color': '#0020A2','content_color': '#0020A2','progress_color': '#0020A2','icon_color': '#0020A2', 'icon': 'fa fa-check-circle'}

    if st.button('Get prediction'):

        if not headline:
            st.markdown('<p class="subtitle"<Please write a headline!</p>', unsafe_allow_html=True)
        else:
            response = process(user_input=headline, server_url=url+endpoint)
            prediction = float(response["prediction"])
            
            if prediction <= 0.5:
                theme = theme_normal
                message = "Normal headline"
                    
            else:
                theme = theme_sarcastic
                message = "Sarcastic!"
                
            hc.info_card(title='Prediction',
                         content=message,
                         theme_override=theme,
                         bar_value=prediction*100)