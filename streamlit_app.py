import streamlit as st 

import pandas as pd

import plotly.express as px  # interactive charts

import os


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


# Back to website link from streamlit app
url = "https://signalstrader.com/portfolio-item"
st.write("[Back to SignalsTrader](%s)" % url)

# dashboard title
st.title("Real-Time / Past Performance Signals Dashboard")

#Added sidebar
with st.sidebar:
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



fig_monthly_pips = px.scatter(x=df.loc[:,"MnY"], y=df.loc[:,"Mpips"], title="Monthly Pips")


fig_monthly_pips.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)




####################  YoY Bar ###########################


yoy = df[["YYear","YPips"]]

fig_yoy = px.bar(yoy, x="YYear", y="YPips", title="Yearly Pips (YoY)")


fig_yoy_pips = px.bar(

    yoy,

    y="YPips",

    x="YYear",

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




####################  Total Pips Line  ###########################



fig_totalpips_pips_line = px.line(df, x="MnY", y="Tpips", title='Total Pips (MoM)')


fig_totalpips_pips_line.update_layout(

    plot_bgcolor="rgba(0,0,0,0)",

    xaxis=(dict(showgrid=False)),

    autosize=True

)


##################### Display Charts ##########################

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(fig_total_pips)

with col2:

    st.plotly_chart(fig_total_pips_pie)



col3, col4, col5 = st.columns(3)

with col3:
    st.plotly_chart(fig_monthly_pips)

with col4:

    st.plotly_chart(fig_yoy)


with col5:

    st.plotly_chart(fig_totalpips_pips_line)


##################### Show Dataframe Actual Data Read from CSV ##########################

#st.dataframe(pips_by_currency)

#st.dataframe(df)

#st.dataframe(monthlypips)

#st.dataframe(df2)



