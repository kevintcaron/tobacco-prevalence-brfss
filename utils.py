import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data(ttl=3600)
def get_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """
    DATA_FILENAME = r'data/2024-07-31_2018-2022 Prevalence Estimates - Dashboard.csv'
    df = pd.read_csv(DATA_FILENAME)

    return df

def get_figure_labels(selected_recipients,
                      recipient,
                      selected_tobs,
                      selected_tob,
                      selected_demo_names,
                      selected_demo_name):
    if (len(selected_recipients) > 1) and (len(selected_tobs) > 1) and len(selected_demo_names) > 1:
        label_style = f'{recipient} - {selected_tob} - {selected_demo_name}'
    elif (len(selected_recipients) > 1) and (len(selected_tobs) > 1) and len(selected_demo_names) == 1:
        label_style = f'{recipient} - {selected_tob}'
    elif (len(selected_recipients) > 1) and (len(selected_tobs) == 1) and len(selected_demo_names) > 1:
        label_style = f'{recipient} - {selected_demo_name}'
    elif (len(selected_recipients) == 1) and (len(selected_tobs) > 1) and len(selected_demo_names) > 1:
        label_style = f'{selected_tob} - {selected_demo_name}'
    elif (len(selected_recipients) == 1) and (len(selected_tobs) == 1) and len(selected_demo_names) > 1:
        label_style = f'{selected_demo_name}'
    elif (len(selected_recipients) == 1) and (len(selected_tobs) > 1) and len(selected_demo_names) == 1:
        label_style = f'{selected_tob}'
    elif (len(selected_recipients) > 1) and (len(selected_tobs) == 1) and len(selected_demo_names) == 1:
        label_style = f'{recipient}'
    elif (len(selected_recipients) == 1) and (len(selected_tobs) == 1) and len(selected_demo_names) == 1:
        label_style = f'{recipient} - {selected_tob} - {selected_demo_name}'
    else:
        label_style = f'Something Broke!'
    return label_style


def get_figure_title(selected_tobs):
    if len(selected_tobs) == 1:
        return f'{selected_tobs[0]} Tobacco Use Prevalence'
    elif len(selected_tobs) == 2:
        return f'{selected_tobs[0]} and {selected_tobs[1]} Tobacco Use Prevalence'
    elif len(selected_tobs) == 3:
        return f'{selected_tobs[0]}, {selected_tobs[1]}, and {selected_tobs[2]} Tobacco Use Prevalence'
    elif len(selected_tobs) == 4:
        return f'{selected_tobs[0]}, {selected_tobs[1]}, {selected_tobs[2]}, and {selected_tobs[3]} Tobacco Use Prevalence'
    else:
        return 'Something Broke'

def get_figure_subtitle(selected_recipients, selected_demo_names):
    if len(selected_recipients) == 1:
        locations = f'Location: {selected_recipients[0]}'
    elif len(selected_recipients) > 1:
        locations = f'Locations: {", ".join(selected_recipients)}'
    else:
        locations = f'Locations: {None}'

    if len(selected_demo_names) == 1:
        groups = f'By: {selected_demo_names[0]}'
    elif len(selected_demo_names) > 1:
        groups = f'By: {", ".join(selected_demo_names)}'
    else:
        groups = f'By: {None}'

    return f'{locations}; {groups}'