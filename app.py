# Import libraries 
import streamlit as st
import pandas as pd
import plotly.express as px


# Importing the data
df = pd.read_csv("vehicles.csv")


#Creating the Data Viewer using Streamlit
st.header('Data viewer') 
st.dataframe(df)
     
    
     
                     
#Formatting the data to create Chart of Vehicle Types by Year using Streamlit                 
df_type = df[(df['type'].notnull()) & (
    df['model_year'].notnull()) & (df['model_year'] >= 1995)]
df_type_model = df_type.groupby(['type', 'model_year'])['type'].count(
).sort_values(ascending=False).reset_index(name='count')

#Creating a stacked Bar Chart of Vehicle Types by Year using Streamlit
st.header('Vehicle Types by Year')
fig = px.bar(df_type_model, x='model_year', y='count', hover_data=['type', 'model_year'],
             labels={'count': 'Number of Vehicles'},
             color='type', height=400, color_discrete_sequence=px.colors.sequential.Darkmint, template="plotly")
fig.update_layout(xaxis=dict(tickangle=270, tickmode='linear'), width=1100)

#Display figure with Streamlit
st.write(fig)



#Formatting the data to create Chart of Price vs Price vs Model Year vs Transmission Type using Streamlit                 
df_price_model = df[(df['price'].notnull()) & (
    df['price'] < 100000) & (df['model_year'].notnull()) & (df['model_year'] >= 1995) & (df['model_year'] > 1950)
    & (df['days_listed'].notnull()) & (df['odometer'].notnull())]
df_price_model = df_price_model[[
    'price', 'model_year', 'transmission', 'days_listed', 'odometer']]

#Creating a scatter Chart of Price vs Model Year vs Days Listed vs Odometer using Streamlit
st.header('Price vs Model Year vs Days Listed vs Odometer')
fig = px.scatter_matrix(df_price_model, color_discrete_sequence=px.colors.sequential.Darkmint, dimensions=[
                        "price", "model_year", "days_listed", "odometer"], color="transmission", template="plotly")

fig.update_traces(diagonal_visible=False)
fig.update_layout(dragmode='select', width=1100, height=500)

#Display figure with Streamlit
st.write(fig)


#Checkbox 
st.header('Compare Price Distribution by Model')
df_model_model = df[(df['model'].notnull()) & (
    df['price'].notnull())] 
df_model_model = sorted(df['model'].unique())


model_1 = st.selectbox('Select model 1',
                              df_model_model, index=df_model_model.index('bmw x5'))

model_2 = st.selectbox('Select model 2',
                              df_model_model, index=df_model_model.index('ford f-150'))
mask_filter = (df['model'] == model_1) | (df['model'] == model_2)
df_model_model_new = df[mask_filter]

normalize = st.checkbox('Normalize histogram', value=True, key='normalize_checkbox')
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
fig = px.histogram(df_model_model_new,
                      x='price',
                      nbins=30,
                      color='model',
                      histnorm=histnorm,
                      barmode='overlay')

st.write(fig)
