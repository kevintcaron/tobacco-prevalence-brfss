import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

import utils

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Tobacco Use-Prevalence Dashboard',
    page_icon=':no_smoking:',
    layout='wide')

df = utils.get_data()
colors = px.colors.qualitative.Safe
min_value = df['Year'].min()
max_value = df['Year'].max()

st.markdown('''
# NTCP Evaluation: Tobacco Use-Prevalence Dashboard
This tool was created to support the evaluation of the National Tobacco Control Program (NTCP). Health scientists are 
encoraged to use the interactive widgets below to browse prevalence data from the [Behavioral Risk Factor Surveillance 
System](https://www.cdc.gov/brfss/index.html). 
''')

colA, colB, colC, colD = st.columns([5, 1, 13, 1])
with colA:
    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    recipients = df['Recipient'].unique()

    selected_recipients = st.multiselect('Select geographic locations',
                                         options=recipients,
                                         default=['United States'])

    selected_tobs = st.multiselect('Select tobacco-use categories',
                                   options=['Smoking', 'Smokeless', 'Ecig', 'Any'],
                                   default=['Smoking'])

    selected_demo_names = st.multiselect('Select demographic groups',
                                         options=df['Demographic_Name'].unique(),
                                         default=['Total Population'])

    # Filter the data
    filtered_df = df[
        (df['Recipient'].isin(selected_recipients))
        & (df['Year'] <= to_year)
        & (from_year <= df['Year'])
        & (df['Demographic_Name'].isin(selected_demo_names))
        ]

with colC:
    fig = go.Figure()
    i = 0
    for recipient in selected_recipients:
        graph_df = filtered_df[filtered_df['Recipient'] == recipient]
        for selected_tob in selected_tobs:
            for selected_demo_name in selected_demo_names:
                graph_df2 = graph_df[graph_df['Demographic_Name'] == selected_demo_name]
                label_style = utils.get_figure_labels(selected_recipients, recipient, selected_tobs,
                                                      selected_tob, selected_demo_names, selected_demo_name)
                fig.add_trace(go.Scatter(
                    x=graph_df2['Year'],
                    y=graph_df2[f'{selected_tob}_V'],
                    mode='lines+markers',
                    name=label_style,
                    line=dict(color=colors[i % len(colors)]),  # Use colors from the defined palette
                    marker=dict(color=colors[i % len(colors)], size=8),
                    error_y=dict(
                        type='data',
                        array=graph_df2[f'{selected_tob}_U'] - graph_df2[f'{selected_tob}_V'],
                        arrayminus=graph_df2[f'{selected_tob}_V'] - graph_df2[f'{selected_tob}_L']
                    )
                ))
                i += 1
    tickvals = filtered_df['Year'].unique()
    ticktext = [str(int(year)) for year in tickvals]

    title_info = utils.get_figure_title(selected_tobs)
    subtitle_info = utils.get_figure_subtitle(selected_recipients, selected_demo_names)
    title = f'          {title_info} — BRFSS {from_year} to {to_year}'
    subtitle = f'          {subtitle_info}'

    # Add title and axis labels
    fig.update_layout(
        title={
            'text': f"<span style='font-size:18px;font-weight: bold;'>{title}<br>"
                    f"<span style='font-size:18px;font-weight: normal;'>{subtitle}</span>",
            'xanchor': 'left',
            'yanchor': 'top'
        },
        xaxis_title='Year',
        yaxis_title='Prevalence',
        height=500,
        # width=800,
        xaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,
            tickformat='.0f'
        ),
        yaxis=dict(rangemode='tozero')
    )

    st.plotly_chart(fig)
