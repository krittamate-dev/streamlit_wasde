import pandas as pd 
import streamlit as st
import os

# Load data  
path = 'data/'

### table structure
def pivot_info(report_title):
    # world 
    _world = ['World and U.S. Supply and Use for Cotton',
            'World and U.S. Supply and Use for Grains',
            'World and U.S. Supply and Use for Oilseeds',
            'World Coarse Grain Supply and Use', 'World Corn Supply and Use',
            'World Cotton Supply and Use',
            'World Rice Supply and Use  (Milled Basis)',
            'World Soybean Meal Supply and Use',
            'World Soybean Oil Supply and Use', 'World Soybean Supply and Use',
            'World Wheat Supply and Use']
    _byclass = ['U.S. Wheat by Class: Supply and Use']
    _us_supply_use = ['U.S. Cotton Supply and Use', 'U.S. Dairy Prices',
                    'U.S. Egg Supply and Use',
                    'U.S. Feed Grain and Corn Supply and Use', 
                    'U.S. Milk Supply and Use',
                    'U.S. Rice Supply and Use',
                    'U.S. Sorghum, Barley, and Oats Supply and Use',
                    'U.S. Sugar Supply and Use',
                    'U.S. Wheat Supply and Use','U.S. Soybeans and Products Supply and Use (Domestic Measure)']
    if report_title == 'U.S. Meats Supply and Use':
        pivot_options = {
                            "Pivot Columns": ['Attribute'],
                            "Pivot Indexes": ['Commodity', 'MarketYear', 'ProjEstFlag'],
                            "Pivot Values": ['Value'],
                            "Pivot Drop": ['WasdeNumber','ReportDate', 'ReportTitle', 'Region']
                        }
        return pivot_options  

    if report_title in ['U.S. Quarterly Animal Product Production', 'U.S. Quarterly Prices for Animal Products',]:
        pivot_options = {
                            "Pivot Columns": ['Commodity'],
                            "Pivot Indexes": ['MarketYear', 'AnnualQuarterFlag', 'ProjEstFlag'],
                            "Pivot Values": ['Value'],
                            "Pivot Drop": ['WasdeNumber','ReportDate', 'ReportTitle', 'ForecastYear', 'ForecastMonth']
                        }
        return pivot_options 
    if report_title in _world:
        pivot_options = {
                            "Pivot Columns": ['Attribute'],
                            "Pivot Indexes": ['MarketYear','ProjEstFlag', 'Region'],
                            "Pivot Values": ['Value'],
                            "Pivot Drop": ['WasdeNumber','ReportDate', 'ReportTitle', 'Commodity', 'AnnualQuarterFlag', 'ForecastYear', 'ForecastMonth']
                        }
        return pivot_options
    if report_title in _byclass:
        pivot_options = {
                            "Pivot Columns": ['Commodity'],
                            "Pivot Indexes": ['MarketYear', 'ProjEstFlag', 'Attribute'],
                            "Pivot Values": ['Value'],
                            "Pivot Drop": ['WasdeNumber','ReportDate', 'ReportTitle', 'Region']
                        }
        return pivot_options
    if report_title in _us_supply_use:
        pivot_options = {
                            "Pivot Columns": ['MarketYear'],
                            "Pivot Indexes": ['Commodity', 'Attribute'],
                            "Pivot Values": ['Value'],
                            "Pivot Drop": ['WasdeNumber','ReportDate', 'ReportTitle', 'Region']
                        }
        return pivot_options
    else:
        pivot_options = {
                            "Pivot Columns": [],
                            "Pivot Indexes": [],
                            "Pivot Values": [],
                            "Pivot Drop": []
                        }
        return pivot_options


@st.cache_data
def load_data(path):
    wasde_files = os.listdir(f"{path}")
    wasde_files = [file for file in wasde_files if '.csv' in file]
    return wasde_files

wasde_files = load_data(path)

st.markdown("### 1. Select file")
filename = st.selectbox('Select a WASDE file', wasde_files)

if filename:
    df = pd.read_csv(f"{path}{filename}")
    st.write(df.head(5))

    @st.cache_data
    def load_cols(df):
        return df.columns.tolist() if df is not None else []

    all_cols = load_cols(df)

    st.markdown("### 2. Pivot info")

    report_titles = df["ReportTitle"].unique().tolist()
    report_title = st.selectbox("Select Report Title", report_titles)

    pivot_options = pivot_info(report_title)

    for key in pivot_options:
        pivot_options[key] = st.multiselect(key, all_cols, pivot_options[key])

    pivot_cols = pivot_options["Pivot Columns"]
    pivot_indexs = pivot_options["Pivot Indexes"]
    pivot_values = pivot_options["Pivot Values"]
    pivot_drop = pivot_options["Pivot Drop"]

    _wasde = df[df['ReportTitle'] == report_title]

    st.markdown("### 3. Pivot Table")
    st.markdown(f"{report_title}")
    try:
        pivot_df = pd.pivot(
            _wasde.drop(columns=pivot_drop),
            columns=pivot_cols,
            index=pivot_indexs,
            values=pivot_values
        )
        st.write(pivot_df)
    except:
        st.warning("กรุณาเลือกคอลัมน์สำหรับ Pivot Table ให้ครบถ้วน")

