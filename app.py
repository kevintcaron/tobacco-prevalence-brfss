import streamlit as st

import utils
import components


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Tobacco Use-Prevalence Dashboard',
    page_icon=':no_smoking:',
    layout='wide')

df = utils.get_data(r'data/2024-09-13_2018-2023 NTCP Evaluation Estimates - Dashboard.csv')
# colors = px.colors.qualitative.Safe

# Tol colors (12)
# https://davidmathlogic.com/colorblind/
colors = [
  "rgb(51, 34, 136)",
  "rgb(17, 119, 51)",
  "rgb(182, 160, 111)",
  "rgb(136, 204, 238)",
  "rgb(204, 102, 119)",
  "rgb(170, 68, 153)",
  "rgb(136, 34, 85)",
  "rgb(57, 183, 209)",
  "rgb(68, 170, 153)",
  "rgb(127, 36, 137)",
  "rgb(95, 207, 40)",
  "rgb(221, 204, 119)"
]

min_value = df['Year'].min()
max_value = df['Year'].max()
recipients = df['Recipient'].unique()

st.markdown('''
# NTCP Evaluation Outcomes Dashboard
This tool was created to support the evaluation of the National Tobacco Control Program (NTCP). Health scientists are 
encouraged to use the interactive widgets below to browse tobacco use-prevalence and quit attempts data from the [Behavioral Risk Factor Surveillance 
System](https://www.cdc.gov/brfss/index.html). 
''')

colA, colB = st.columns([1, 3])
with colA:

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    multiselect_on = st.toggle("Enable Multiple Selections")

    if multiselect_on:
        selected_recipients, selected_tobs, selected_demo_names, filtered_df = components.multiselect_widgets(df, from_year, to_year, recipients)
    else:
        selected_recipient, selected_tob, selected_demo_name, filtered_df = components.basic_widgets(df, from_year, to_year, recipients)
with colB:
    if multiselect_on:
        fig, name = components.multiselect_plot(selected_recipients, selected_tobs, selected_demo_names, filtered_df, colors, from_year, to_year)
    else:
        fig, name = components.basic_plot(selected_recipient, selected_tob, selected_demo_name, filtered_df, colors, from_year, to_year)

    st.plotly_chart(fig)

