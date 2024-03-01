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

def load_dict(path):
    with open(path) as response:
        dict = json.load(response)
        return dict

# Assuming we have saved our datasets as CSV files after analysis
MIGROS_STORES_CSV = './data/df_switzerland_migros.csv'
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
        df = load_data('./data/df_switzerland_denner.csv')
        df1 = df.copy()
        cantons = load_dict(".data/georef-switzerland-kanton@public.geojson")
        cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                        'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                        'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                        'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                        'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}
        denner_per_canton = df1.groupby('Canton').size().reset_index(name='count')
                # mapping denners per canton
        fig = px.choropleth_mapbox(
            denner_per_canton,
            color="count",
            geojson=cantons,
            locations="Canton",
            featureidkey="properties.kan_name",
            center={"lat": 46.8, "lon": 8.3},
            mapbox_style="open-street-map",
            zoom=6.3,
            opacity=0.8,
            width=900,
            height=500,
            labels={"Canton":"Canton",
                    "count":"Number of Denners"},
            title="<b>Denners per Canton</b>",
            color_continuous_scale="Cividis",
        )
        fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                          font={"family":"Sans",
                                "color":"maroon"},
                          hoverlabel={"bgcolor":"white",
                                      "font_size":12,
                                      "font_family":"Helvetica"},
                          title={"font_size":20,
                                 "xanchor":"left", "x":0.01,
                                 "yanchor":"bottom", "y":0.95}
                          )

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