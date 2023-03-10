# Importing the required libraries

import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
from matplotlib import cm, colors
from scipy.stats import mannwhitneyu, wilcoxon
from scipy.stats import pearsonr,spearmanr
cwd = os.getcwd()
db_folder=cwd+"/database/"

import json as js

#Loading the dataset
data_komune_code = pd.read_csv(db_folder+ 'Komune_Kode.csv',encoding='latin-1')
data_arsvekt_per_user = pd.read_csv(db_folder+ 'Årsvekt_per_user.csv',encoding='latin-1',index_col=0)
data_education = pd.read_csv(db_folder+ 'education_level.csv', encoding='latin-1', index_col='komnr')
data_ed_percentage = pd.read_csv(db_folder+ 'education_percentage.csv', encoding='latin-1', index_col='komnr')
data_educationH= pd.read_csv(db_folder+ 'education_High.csv', encoding='latin-1', index_col='komnr')
data_educationL = pd.read_csv(db_folder+ 'education_Low.csv', encoding='latin-1', index_col='komnr')
data_users_very_sick = pd.read_csv(db_folder+ 'users_very_sick.csv',encoding='utf-8',index_col='komnr')
data_users_medium_to_very_sick = pd.read_csv(db_folder+ 'users_medium_to_very_sick.csv',encoding='utf-8',index_col='komnr')

#data_users_very_sick.index=data_users_very_sick.index.map(int)
data_earnering=pd.read_csv(db_folder+ 'earnering.csv',encoding='utf-8')
data_befolkning_69 = pd.read_csv(db_folder+ 'befolkning_69.csv',encoding='latin-1',index_col='komnr')
data_heltid = pd.read_csv(db_folder+ 'heltid.csv',encoding='latin-1',index_col=0)
data_årsvekt = pd.read_csv(db_folder+ 'årsvekt.csv',encoding='utf-8',index_col=0)
data_lonn = pd.read_csv(db_folder+ 'lonn.csv',encoding='latin-1',index_col=0)
# data_lonn.index = data_lonn.index.map(str)
data_plass_list = pd.read_csv(db_folder+ 'plass_list.csv',encoding='latin-1',index_col=0)
data_stilstor = pd.read_csv(db_folder+ 'stilstor.csv',encoding='latin-1',index_col=0)

data_timar_i_uke = pd.read_csv(db_folder+ 'timar_i_uka.csv',encoding='latin-1',index_col='komnr')
data_timar_i_uke.index = data_timar_i_uke.index.map(int)
data_timar_i_uke_67plus = pd.read_csv(db_folder+ 'timar_i_uka_67plus.csv',encoding='latin-1',index_col='komnr')
data_timar_i_uke_67plus.index = data_timar_i_uke_67plus.index.map(int)

data_timar_alle_hjemmetjenester=pd.read_csv(db_folder+ 'timar_i_uka_all_institution.csv',encoding='latin-1',index_col='komnr')
data_timar_alle_hjemmetjenester.index = data_timar_alle_hjemmetjenester.index.map(int)


data_users = pd.read_csv(db_folder+ 'users.csv',encoding='latin-1',index_col='komnr')
data_users_over_67 = pd.read_csv(db_folder+ 'users_over_67.csv',encoding='latin-1',index_col=0)
data_vakter = pd.read_csv(db_folder+ 'vakter.csv',encoding='latin-1',index_col='komnr')
data_kostra = pd.read_csv(db_folder+ 'kostra_group.csv',encoding='latin-1', index_col='komnr')
data_kpr = pd.read_csv(db_folder+ 'kpr.csv',encoding='utf-8')

# data_kostra.index = data_kostra.index.map(str)
data_all_ncr = pd.read_csv(db_folder+ 'all_ncr.csv',encoding='latin-1',index_col=0)
data_all_ncr=data_all_ncr.apply(pd.to_numeric, errors='coerce')
#data_all_ncr["komnr"]=data_all_ncr["komnr"].astype(str)
data_all_ncr=data_all_ncr.groupby(by=['komnr'], axis=0, level=None, as_index=True, sort=False,dropna=True).sum(min_count=1)
data_all_ncr.index = data_all_ncr.index.map(int)
#data_all_ncr.index = data_all_ncr.index.map(str)

#data_all_ncr.set_index('komnr',drop=True, append=False, inplace=True, verify_integrity=True)

data_med_ncr = pd.read_csv(db_folder+ 'med_NCR.csv',encoding='latin-1',index_col=0)
data_med_ncr=data_med_ncr.apply(pd.to_numeric, errors='coerce')
data_med_ncr.index = data_med_ncr.index.map(int)
#data_med_ncr.index = data_med_ncr.index.map(str)

data_med_ncr=data_med_ncr.groupby(by=['komnr'], axis=0, level=None, as_index=True, sort=False,dropna=True).sum(min_count=1)#.set_index('komnr',drop=True, append=False, inplace=True, verify_integrity=True)
##extrection earnering data:
earnering=data_earnering.query("Måltall== 'Andel av vurderte som har risiko for underernæring (hjemmeboende 67 år og eldre)' ")
      
risiko_earnering=earnering.pivot(index="komnr", columns="Tidsperiode", values="Verdi")
risiko_earnering.columns=risiko_earnering.columns.astype(str)
##
list_variables={ "All_ncr":data_all_ncr.divide(data_users),#*100,
"Med_ncr":data_med_ncr.divide(data_users),#(data_med_ncr.divide(data_users)).multiply(100),
"Users_total":data_users,
"Education_Ratio_(H/L)":data_education,
"%_High_educated_nurses":data_ed_percentage,
"Education_High":data_educationH.divide(data_users),
"Education_Low":data_educationL.divide(data_users),
"Stillingsstørrelse":data_stilstor,
"Timer_i_uka":data_timar_i_uke,
"Timer_ i_uka_67+":data_timar_i_uke_67plus,
"Timer alle hjemmetjenester":data_timar_alle_hjemmetjenester,
"Åarsvekt_per_user":data_arsvekt_per_user,
"heltid":data_heltid,
"Vakter":data_vakter.divide(data_users).dropna(axis=1, how="all"),
"Lonn":data_lonn.divide(data_users).dropna(axis=1, how="all"),
"User_over_67":data_users_over_67.divide(data_users),
"Plass_avaiable": data_plass_list ,
"Users_very_sick": data_users_very_sick,
"Users medium to very sick": data_users_medium_to_very_sick.divide(data_users),
"Risiko for underernæring":risiko_earnering
}
if 'variables' not in st.session_state:
    st.session_state['variables'] = list_variables
if 'kom_kode' not in st.session_state:
    st.session_state['kom_kode'] = data_komune_code
if 'kostra' not in st.session_state:
    st.session_state['kostra'] = data_kostra
#st.write(data_users_medium_to_very_sick.divide(data_users))

def plot_graph_kommune(dataframe_kom,dataframe_mean_kostra,kom_name,year,y_label):
    dataframe_mean_kostra=dataframe_mean_kostra.replace(np.inf, np.nan)
    df_plot = pd.DataFrame({kom_name:dataframe_kom,'kostra_mean':dataframe_mean_kostra.mean(axis=0)
    ,'Year':  list(year)
    })
    band_plot = dataframe_mean_kostra.melt( value_vars=year, var_name="Year", value_name=y_label, col_level=None, ignore_index=True)    
    df_plot_kom_meankostra = df_plot.melt('Year', var_name='name', value_name=y_label)
    line = alt.Chart(df_plot_kom_meankostra).mark_line().encode(
    alt.X('Year',scale=alt.Scale(zero=False)),
    alt.Y(y_label,scale=alt.Scale(zero=False)),
    # ,color=alt.Color("name:N")
    color= alt.Color('name',
                   scale=alt.Scale(
            domain=['kostra_mean', kom_name],
            range=['red', 'green'])))
    band = alt.Chart(band_plot).mark_errorband(extent='ci', color='red'
    ).encode(
    x='Year',
    y= y_label,
    #color= "steelblue"
    )
    chart=alt.layer(band ,line).properties(
        height=250, width= 310
        ,autosize = 'pad'
      #   title=stock_title
    ).configure_title(
        fontSize=16
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    return chart#line, band 


years_list=["2018","2019","2020"]
from PIL import Image

icons = []
icons.extend([Image.open('psychotherapy-fill.png')])
icons.extend([Image.open('bxs-time-five.png')])
icons.extend([Image.open('nutrition.png')])

face=[]
face.extend([Image.open('sad.png')])
face.extend([Image.open('face.png')])
face.extend([Image.open('happy.png')])

face_inverted=[]
face_inverted.extend([Image.open('happy.png')])
face_inverted.extend([Image.open('face.png')])
face_inverted.extend([Image.open('sad.png')])

arrow_normal=[]
arrow_normal.extend([Image.open('down.png')])
arrow_normal.extend([Image.open('flat.png')])
arrow_normal.extend([Image.open('up.png')])

arrow_inverted=[]
arrow_inverted.extend([Image.open('down_good.png')])
arrow_inverted.extend([Image.open('flat.png')])
arrow_inverted.extend([Image.open('up_bad.png')])

def main():
    

    #with st.sidebar:   

    # ------------------------------------------------------------------------
    # Koumne dropdown list 
    komune_name = st.selectbox('Select the komune name',options= [gruppetekst for gruppekode,gruppetekst in zip(data_komune_code['GRUPPEKODE'].unique(),data_komune_code['GRUPPETEKST'].unique())])     
    query_komune_name = data_komune_code.query("GRUPPETEKST == @komune_name")  
    komune_code = query_komune_name['GRUPPEKODE'].iloc[0]     
    kom_gruppe = data_kostra.loc[int(komune_code)]['kostragr']
    list_kom_kostra = list(data_kostra.query('kostragr == @kom_gruppe').index)
    list_komune_kostra = [str(w) for w in list_kom_kostra]          
    options = ["Users medium to very sick","Timer alle hjemmetjenester","Risiko for underernæring"]
    
    if not options:
        options = list_variables  
    for i,values in  enumerate(options):        
        text1=values
        text2="Trend in the last 3 years"
        text3="Comperaed to National Statistic"

        if(values in ["Users medium to very sick","risiko for underernæring"]):
            arrow_temp=arrow_inverted
            up_or_down=face_inverted
        else:
            arrow_temp=arrow_normal
            up_or_down=face
        data = list_variables[values]
        data.columns=data.columns.astype(str)
        data=data[years_list]
        try:
            dataset = data.loc[int(komune_code)]
            #mean_education=data_education.loc[list_komune_kostra].median(axis = 0)
            National_75th=data.quantile(q=0.75,axis = 0)
            National_25th=data.quantile(q=0.25,axis = 0)
            dataset=dataset.loc[years_list]
            #line_plot=plot_graph_kommune(dataset,kostra_mean,komune_name,dataset.index, values)  
            
            c=[]

            c.extend([st.container()])
            with c[-1]:
                cols=st.columns(3)    
                with cols[0]:
                    st.title(text1)
                    st.image(icons[i],use_column_width='always')

                with cols[1]:
                    st.title(text2)            
                    #diff=dataset.diff(periods=1 )
                    diff=dataset.pct_change(periods=1 ).sum()
                    if(diff>0.02):
                        st.image(arrow_temp[2] ,use_column_width='always')
                    else:
                        if(diff<-0.02):
                            st.image(arrow_temp[0],use_column_width='always')
                        else:
                            st.image(arrow_temp[1],use_column_width='always')

                with cols[2]:
                    st.title(text3)            
                    if(dataset[-1]>National_25th[-1]):
                        if(dataset[-1]>National_75th[-1]):
                            st.image(up_or_down[2],use_column_width='always')
                        else:
                            st.image(up_or_down[1],use_column_width='always')
                    else:
                        st.image(up_or_down[1],use_column_width='always')

        except Exception as error:
                st.write("We miss some index value for this kom", komune_code, "Place Name :"+ komune_name,"->" + values)
                st.write(error.args)
    
    
    


    return


    
main()

