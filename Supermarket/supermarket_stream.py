'''

Streamlit visualisation of supermarket data -> data from: https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales?resource=download

@Author: Hendrik Pieres

based on: https://www.youtube.com/watch?v=Sb0A9i6d320&ab_channel=CodingIsFun

'''

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import locale
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_toggle import st_toggle_switch as switch


st.set_page_config(page_title="Supermarket Sales Dash-Board", page_icon=":bar_chart:", layout="wide")
locale.setlocale(locale.LC_ALL, "de_DE")


@st.cache
def read_data(selected_file):
    return pd.read_csv(selected_file)


def start(selected_file):
    df = read_data(selected_file)   # get data
    st.title(":bar_chart: Sales Dashboard") # create title
    st.markdown("##")
    left, right = st.columns(2)
    left.metric(label="Total Sales", value=locale.format_string("€ %d", df["Total"].sum(), 1))
    with right:
        switch_explorer = switch(label="Enable DataFrame Explorer", key="switch_explorer", default_value=True)
    st.markdown("---")
    if switch_explorer:
        filtered_df = dataframe_explorer(df)
        st.dataframe(filtered_df)
    else:
        filtered_df = df

    st.sidebar.header("Filter Options")
    city = st.sidebar.multiselect("Select the city", options=filtered_df.City.unique(), default=filtered_df.City.unique())
    #product_line = st.sidebar.multiselect("Select product lines", options=filtered_df["Product line"].unique(), default=filtered_df["Product line"].unique())
    payment = st.sidebar.multiselect("Select the kind of payment", options=filtered_df["Payment"].unique(), default=filtered_df.Payment.unique())

    df_selection = filtered_df.query(
        "City == @city & Payment == @payment"
    )

    top = st.slider("How many products?", 1, 6, 6)
    sales_by_prod = df_selection.groupby(by="Product line").sum().sort_values(by="Total", ascending=False)[:top]

    pie_data = sales_by_prod["Total"].values.reshape((len(sales_by_prod),))
    pie_sales_by_prodh2 = px.pie(values=pie_data, names=sales_by_prod.index, title="<b>Sales by product line Top %d</b>" % top, template="plotly_white")
    pie_sales_by_prodh2.update_layout(title_x=0.5)
    bar_sales_by_prodh2 = px.bar(sales_by_prod, x="Total", y=sales_by_prod.index, orientation="h", title="<b> Sales by product line Top %d</b>" % top, template="plotly_white")
    bar_sales_by_prodh2.update_layout(title_x=0.5)
    
    left_column_chart, right_column_chart = st.columns(2)
    
    with left_column_chart:
        #st.metric(label="Sales %d - selected products" % display_year, value=locale.format_string("€ %d", sales_current_year, 1), delta="%.2f %%" % sales_development)
        st.plotly_chart(pie_sales_by_prodh2)
    with right_column_chart:
        #st.metric(label="Sales %d - selected products" % (display_year-1), value=locale.format_string("€ %d", sales_past_year, 1))
        st.plotly_chart(bar_sales_by_prodh2)



if __name__ == "__main__":
    selected_file = st.file_uploader("Select a data file", accept_multiple_files=False)
    if selected_file is not None:
        #try:
         #   start(selected_file)
        #except:
         #   st.error("Wrong file or wrong format")
        start(selected_file)
        