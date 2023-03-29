from pyjstat import pyjstat
import requests
import json, os
import pandas as pd
import streamlit as st

cwd = os.getcwd()
json_query_folder=cwd+"/json_query/"

def import_json(file):
    f=open(file)
    data = json.load(f)
    data.keys()
    resultat = requests.post(data['postUrl'], json = data['queryObj'])
    # Result only gives http status code - 200 if OK. Body is in result.text
    print(resultat)
    dataset = pyjstat.Dataset.read(resultat.text)
    df = dataset.write('dataframe')
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
    df=import_json(hele_folder+file_name)
    name=file_name[:-5]
    dataframe_hjemme[name] = df

for file_name in os.listdir(sykehjem_folder):
    df=import_json(hele_folder+file_name)
    name=file_name[:-5]
    dataframe_sykehjem[name] = df



#list_variables_hele={ "All_ncr":dataframe_hele[],
#}
#list_variables_hjemme={ "All_ncr":dataframe_hjemme[],
#}
#list_variables_sykehjem={ "All_ncr":dataframe_sykehjem[],
#}
if 'variables' not in st.session_state:
    st.session_state['variables_hele'] = dataframe_hele
    st.session_state['variables_hjem'] = dataframe_hjemme
    st.session_state['variables_sykehjem'] = dataframe_sykehjem


