import streamlit as st
from pyjstat import pyjstat
import requests
import json, os
import pandas as pd
import streamlit as st
cwd = os.getcwd()
json_query_folder=cwd+"/json_query/"
db_folder=cwd+"/database/"
data_kostra = pd.read_csv(db_folder+ 'kostra_group.csv',encoding='latin-1', index_col='komnr')

def scrollable_iframe(url, width=700, height=900):
    scrolling_html = f'<iframe src="{url}" width="{width}" height="{height}" style="border:none;"></iframe>'
    return st.markdown(scrolling_html, unsafe_allow_html=True)

def import_json(file):
    f=open(file)
    data = json.load(f)
    data.keys()
    resultat = requests.post(data['postUrl'], json = data['queryObj'])
    # Result only gives http status code - 200 if OK. Body is in result.text
    print(resultat)
    dataset = pyjstat.Dataset.read(resultat.text)
    df_kode=dataset.write('dataframe',naming="id")
    df = dataset.write('dataframe')
    df["kode"]=df_kode.iloc[:,0]
    return df

hele_folder=json_query_folder+"hele/"
hjemme_folder=json_query_folder+"hjemme/"
sykehjem_folder=json_query_folder+"sykehjem/"

dataframe_hele = {} 
dataframe_hjemme = {} 
dataframe_sykehjem = {} 

for file_name in os.listdir(hele_folder):
    df=import_json(hele_folder+file_name)
    name=file_name[:-5]
    dataframe_hele[name] = df

for file_name in os.listdir(hjemme_folder):
    df=import_json(hjemme_folder+file_name)
    name=file_name[:-5]
    dataframe_hjemme[name] = df

for file_name in os.listdir(sykehjem_folder):
    df=import_json(sykehjem_folder+file_name)
    name=file_name[:-5]
    dataframe_sykehjem[name] = df

if 'variables' not in st.session_state:
    st.session_state['variables_hele'] = dataframe_hele
    st.session_state['variables_hjemme'] = dataframe_hjemme
    st.session_state['variables_sykehjem'] = dataframe_sykehjem
    st.session_state['data_kostra']=data_kostra
#if 'kostra' not in st.session_state:
#    st.session_state['kostra'] = data_kostra
#st.write(data_users_medium_to_very_sick.divide(data_users))

webpage_url = "https://www.nrk.no/dokumentar/xl/underernaerte-lilly-_90_-gikk-hele-dager-uten-a-fa-mat-av-hjemmetjenesten-1.16211305#authors--expand"
st.set_page_config( page_icon=':hospital:',layout="wide")
st.title('Norwegian Municipalities Health System Dashboard')
title_container = st.container()
with title_container:
    # Define the column layout
    col1, col2 = st.columns(2)

    # Add the webpage to the first column
    with col2:
        st.write(f"This work was inspired by {webpage_url}")
        #st.components.v1.iframe(webpage_url, width=800, height=600)
        scrollable_iframe(webpage_url)

    # Add some other content to the second column
    with col1:
        # Set up the app header
        
        st.write('Welcome to the Norwegian Municipalities Health System Dashboard! This dashboard is designed to help you explore data on the health systems of Norwegian municipalities, with particular focus on Elderlycare.')

        # Add a picture of Norway
        st.image('main.png', use_column_width=True)

        # Add some description
        st.write('The picture above is generated by a stable diffusion model. This Dashboard aims to combine AI and Investigative journalism to help improve the quality of norwegian healthcare system. Have fun exploring!')