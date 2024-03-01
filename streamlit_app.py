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

POP_DENSITY_CSV = './data/pop_denn.csv'

PROJECTION_CSV = './data/per_change.csv'

PROJECTION_PER_CANTON_CSV = './data/projection_per_kanton_2050_base.csv'

st.title('Migros Store Optimization Analysis')

df = load_data('./data/df_switzerland_denner.csv')
df1 = df.copy()
cantons = load_dict("./data/georef-switzerland-kanton@public.geojson")

st.header('Project Overview')
st.write("""
    This app presents our analysis for identifying optimal locations for new Migros stores in Switzerland.
    Navigate through the app to explore various aspects of our analysis, including population density, Migros store locations, and competitor analysis.
""")

st.header('Migros Store Locations')

st.header('Projection per canton Analysis')

df_base = load_data(PROJECTION_PER_CANTON_CSV)
df_high = pd.read_csv('./data/projection_per_kanton_2050_high.csv')
df_low = pd.read_csv('./data/projection_per_kanton_2050_low.csv')
# give a name to the 1st column with the canton names: Entity
df_base = df_base.rename(columns={df_base.columns[0]: 'Entity'})
df_low = df_low.rename(columns={df_low.columns[0]: 'Entity'})
df_high = df_high.rename(columns={df_high.columns[0]: 'Entity'})


fig = go.Figure()
fig.add_trace(go.Scatter(x=df_low.columns[1:], y=df_low[df_low['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='Low', fillcolor='blue'))
fig.add_trace(go.Scatter(x=df_base.columns[1:], y=df_base[df_base['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='Base', fillcolor='green'))
fig.add_trace(go.Scatter(x=df_high.columns[1:], y=df_high[df_high['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='High', fillcolor='orange'))
fig.update_layout(title='Swiss population projection 2050 (low, base and high scenarios)', xaxis_title='Year', yaxis_title='Population')

st.plotly_chart(fig)

st.write("""
             plot the low, base and high scenarios for Switzerland (no summation)
 show low on blue, base on green and high on orange
 y axis ticks in tenths of millions
 add a shaded area between low and high scenarios
        """)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_low.columns[1:], y=df_low[df_low['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='Low',  line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df_base.columns[1:], y=df_base[df_base['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='Base',  line=dict(color='green') ))
fig.add_trace(go.Scatter(x=df_high.columns[1:], y=df_high[df_high['Entity']=='Schweiz'].values[0][1:], mode='lines+markers', name='High',  line=dict(color='orange') ))
#fig.add_trace(go.Scatter(x=df_high.columns[1:], y=df_high[df_high['Entity']=='Schweiz'].values[0][1:], mode='lines', fill='tonexty', line=dict(color='orange', width=0)))
fig.add_trace(go.Scatter(x=df_low.columns[1:], y=df_low[df_low['Entity']=='Schweiz'].values[0][1:], mode='lines', fill='tonexty', name='Range', line=dict(color='blue', width=0)))
fig.update_layout(title='Swiss population projection 2050 (low, base and high scenarios)', xaxis_title='Year', yaxis_title='Population')

st.plotly_chart(fig)

st.header('Population Density Analysis')
population = load_data(POP_DENSITY_CSV)
st.write("Population density visualization")
if st.checkbox("Show Population density Dataframe"):
    st.subheader("This is the dataset with the Population density")
    st.dataframe(population)

# Population plot (adapt as needed)
fig = px.choropleth_mapbox(
    population,
    color='2022',
    color_continuous_scale='viridis',
    geojson=cantons,
    locations="canton",
    featureidkey="properties.kan_name",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=900,
    height=500,
    labels={"canton":"Canton",
            "2022":"population in 2022"},
    title="<b>Population density and Denners</b>"

)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Helvetica",
                        "color":"maroon"},
                  hoverlabel={"bgcolor":"white",
                              "font_size":12,
                              "font_family":"Helvetica"},
                  title={"font_size":20,
                         "xanchor":"left", "x":0.01,
                         "yanchor":"bottom", "y":0.95}
                  )

fig2 = px.scatter_mapbox(df1, lat="Latitude", lon="Longitude",
                         size_max=15,  # Color the dots based on a column
                         color_discrete_sequence=["red"], # Choose a color scale
                         center={"lat": 46.8, "lon": 8.3},
                         mapbox_style="open-street-map",
                         zoom=6.3,
                         opacity=0.8,
                         width=900,
                         height=500)
trace0 = fig2 # the second map from the previous code
fig.add_trace(trace0.data[0])
trace0.layout.update(showlegend=False)
st.plotly_chart(fig)


projection = load_data(PROJECTION_CSV)

viz1 = projection[['Canton','per_change_10y', 'per_change_20y']]
viz1 = viz1.sort_values(by='per_change_20y', ascending=False)

# Column chart for the 10 and 20 years population projection
fig = go.Figure()
fig.add_trace(go.Bar(x=viz1['Canton'],
                     y=viz1['per_change_10y'],
                     name='% growth of population in 10 years',
                     marker_color='rgb(55, 83, 109)'
                     ))
fig.add_trace(go.Bar(x=viz1['Canton'],
                     y=viz1['per_change_20y'],
                     name='% growth of population in 20 years',
                     marker_color='rgb(26, 118, 255)'
                     ))

fig.update_layout(
    title='Comparison of the % change in the growth of the population by canton',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='% change',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1,
    width=900, # Set the width of the figure
    height=600 # gap between bars of the same location coordinate.
)

fig.update_layout(
    legend=dict(
        x=1,
        y=1,
        xanchor='right',  # Anchors the legend to the right
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)'  # Anchors the legend to the bottom
    )
)
st.plotly_chart(fig)

st.header('Competitor Analysis')

if st.checkbox("Show Competitor Analysis Dataframe"):
    st.subheader("This is the dataset with the Denners per Canton:")
    denner_per_canton = df1.groupby('Canton').size().reset_index(name='count')
    st.dataframe(denner_per_canton)
st.header('Denners per Canton')
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
st.plotly_chart(fig)
st.write("""
            Denners in Switzerland
        """)
rating_per_canton = df1.groupby('Canton')['Rating'].agg('mean').reset_index(name='mean_rating')
sorted_rating = rating_per_canton.sort_values(by='mean_rating', ascending=False)
fig = px.scatter_mapbox(df1, lat="Latitude", lon="Longitude", center={"lat": 46.8, "lon": 8.3},
                        mapbox_style="open-street-map",
                        zoom=6.3,
                        opacity=0.8,
                        width=900,
                        height=500,
                        title="Denners in Switzerland")

st.plotly_chart(fig)


df_switzerland_competitors=load_data("./data/df_switzerland_competitors.csv")

fig = px.scatter_mapbox(df_switzerland_competitors,
                        lat="Latitude",
                        lon="Longitude",
                        size_max=15,  # Color the dots based on a column
                        color_discrete_sequence=["blue"],  # Choose a color scale
                        center={"lat": 46.8, "lon": 8.3},
                        mapbox_style="open-street-map",
                        zoom=6.3,
                        opacity=0.8,
                        width=900,
                        height=500,
                        hover_data=["Canton", "Brand"])  # Specify the correct column names for hover data

fig.update_layout(title="Competitors in Switzerland (ALDI, COOP, LIDL, SPAR, VOLG)")

st.plotly_chart(fig)


brand_count_per_canton = df_switzerland_competitors.groupby(['Canton', 'Brand']).size().reset_index(name='Count')
total_shops_per_canton = brand_count_per_canton.groupby('Canton')['Count'].sum().reset_index(name='Total Competitor Shops')

st.dataframe(data=total_shops_per_canton)

total_shops_per_canton = total_shops_per_canton.sort_values(by='Total Competitor Shops', ascending=False)

fig = px.bar(total_shops_per_canton,
             x='Canton',
             y='Total Competitor Shops',
             title='Total Competitor Shops per Canton',
             labels={'Total Competitor Shops': 'Number of Competitor Shops'},
             color='Canton')  # Optional: Color the bars differently based on canton

st.plotly_chart(fig)

