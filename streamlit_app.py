# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# load data from path
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# Assuming we have saved our datasets as CSV files after analysis
# TODO change with migros_stores.csv file
MIGROS_STORES_CSV = './data/df_switzerland_aldi.csv'
# TODO change with pop_density.csv file
POP_DENSITY_CSV = './data/df_switzerland_lidl.csv'
# TODO change with competitors file
COMPETITORS_CSV = './data/df_switzerland_spar.csv'

def main():
    st.title('Migros Store Optimization Analysis')

    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Introduction', 'Migros Store Locations', 'Population Density Analysis', 'Competitor Analysis'])

    if page == 'Introduction':
        st.header('Project Overview')
        st.write("""
            This app presents our analysis for identifying optimal locations for new Migros stores in Switzerland.
            Navigate through the app to explore various aspects of our analysis, including population density, Migros store locations, and competitor analysis.
        """)

    elif page == 'Migros Store Locations':
        st.header('Migros Store Locations')
        migros_df = load_data(MIGROS_STORES_CSV)
        # fig = px.scatter_mapbox(migros_df, lat="latitude", lon="longitude", zoom=7, height=300,
        #                         mapbox_style="open-street-map")
        # st.plotly_chart(fig, use_container_width=True)

    elif page == 'Population Density Analysis':
        st.header('Population Density Analysis')
        pop_density_df = load_data(POP_DENSITY_CSV)
        # Example plot (adapt as needed)
        st.write("Population density visualization here. Use your analysis results to create a map or chart.")

    elif page == 'Competitor Analysis':
        st.header('Competitor Analysis')
        competitors_df = load_data(COMPETITORS_CSV)
        # Example plot (adapt as needed)
        st.write("Competitor store locations visualization here. Use your analysis results to create a map or chart.")

if __name__ == '__main__':
    main()