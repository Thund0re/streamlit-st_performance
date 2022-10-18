import streamlit as st 

import numpy as np

import pandas as pd

import altair as alt

import plotly.express as px  # interactive charts

import matplotlib

import matplotlib.pyplot as plt

import seaborn as sns

import os

from matplotlib.backends.backend_agg import RendererAgg



st.set_page_config(

    page_title="Real-Time Data Science Dashboard",

    page_icon="📊",

    layout="wide",

)





#Loading the data

@st.cache

def get_data():

     return pd.read_csv(os.path.join(os.getcwd(),'st_tradesignals.csv'))



df = get_data()

df.head()

# dashboard title

url = "https://signalstrader.com/portfolio-item"
st.write("[Back to SignalsTrader](%s)" % url)


st.title("Real-Time / Past Performance Signals Dashboard")



currency = st.multiselect(

    "Select Currency:",

    options=df["Currency"].unique(),

    default=df["Currency"].unique()

)



trade_type = st.multiselect(

    "Select Type:",

    options=df["TradeType"].unique(),

    default=df["TradeType"].unique()

)









####################  Filters  ###########################

df_selection = df.query(

    'Currency == @currency & TradeType == @trade_type'

)



total_pips = float(df_selection["Pips"].sum())







pips_by_currency = (

    df_selection.groupby(by=["Currency"]).sum()[["Pips"]].sort_values(by="Currency")

)







####################  Currency Bar Graph  ###########################

fig_total_pips = px.bar(

    pips_by_currency,

    y="Pips",

    x=pips_by_currency.index,

    orientation = "v",

    title = "Currency Wise Pips Split",

    color_discrete_sequence=["#ff4b4b"] ,

    template="plotly_white",



)



fig_total_pips.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)







####################  Pie Graph  ###########################

fig_total_pips_pie = px.pie(

    pips_by_currency,

    values="Pips",

    names = pips_by_currency.index,

    template="plotly_white",

    title = "Percentage Wise Pips Split in Pie",



)



fig_total_pips_pie.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)






####################  Monthly Pips Line  ###########################



fig_monthly_pips = px.line(

    df,

    y="Mpips",

    x="MnY",

    orientation = "h",

    title = "Monthly Pips",

    color_discrete_sequence=["#0086DC"] ,

    template="plotly_white"

)



fig_monthly_pips.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)









####################  YoY  ###########################



yoy = pd.read_csv(os.path.join(os.getcwd(),'YoY.csv'))





fig = px.bar(yoy, x="Year", y="Pips", title="Yearly Pips")







fig_yoy_pips = px.bar(

    yoy,

    y="Pips",

    x="Year",

    orientation = "h",

    title = "Yearly Pips",

    color_discrete_sequence=["#ff4b4b"] ,

    template="plotly_white"

)



fig_yoy_pips.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=False

)







#st.plotly_chart(fig_yoy_pips)





####################  Total Pips Line  ###########################

totalpips = pd.read_csv(os.path.join(os.getcwd(),'TotalP.csv'))



df1 = totalpips



fig_totalpips_pips_line = px.line(

    totalpips,

    y="Tpips",

    x="MnY",

    orientation = "h",

    title = "Total Pips",

    color_discrete_sequence=["#0086DC"] ,

    template="plotly_white"

)



fig_totalpips_pips_line.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)


#st.plotly_chart(fig_monthly_pips)






col1, col2 = st.columns(2)



with col1:

    st.plotly_chart(fig_total_pips)

with col2:

    st.plotly_chart(fig_total_pips_pie)




col3, col4, col5 = st.columns(3)

with col3:
    #st.plotly_chart(fig_total_pips_pie)
    st.plotly_chart(fig_monthly_pips)

with col4:

    st.plotly_chart(fig)


with col5:

    st.plotly_chart(fig_totalpips_pips_line)


#st.dataframe(pips_by_currency)

#st.dataframe(df)

#st.dataframe(monthlypips)

#st.dataframe(df2)



