import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

import utils

def basic_widgets(df,from_year, to_year, recipients):
    selected_recipient = st.selectbox('Select geographic locations',
                                      options=recipients,
                                      index=0)

    selected_tob = st.selectbox('Select tobacco indicator',
                                options=['Current Cigarette',
                                         'Current Smokeless',
                                         'Current E-cigarette',
                                         'Current Any Tobacco Product',
                                         'Past-Year Quit Attempt'],
                                index=0)

    selected_demo_name = st.selectbox('Select demographic group',
                                      options=df['Demographic_Group'].unique(),
                                      index=0)

    # Filter the data
    filtered_df = df[
        (df['Recipient'] == selected_recipient)
        & (df['Year'] <= to_year)
        & (from_year <= df['Year'])
        & (df['Demographic_Group'] == selected_demo_name)
        ]

    return selected_recipient, selected_tob, selected_demo_name, filtered_df


def multiselect_widgets(df,from_year, to_year, recipients):
    selected_recipients = st.multiselect('Select geographic locations',
                                         options=recipients,
                                         default=['United States (median)'])

    selected_tobs = st.multiselect('Select tobacco-use categories',
                                   options=['Current Cigarette', 'Current Smokeless', 'Current E-cigarette', 'Current Any Tobacco Product'],
                                   default=['Current Cigarette'])

    selected_demo_names = st.multiselect('Select demographic groups',
                                         options=df['Demographic'].unique(),
                                         default=['Total Population'])

    # Filter the data
    filtered_df = df[
        (df['Recipient'].isin(selected_recipients))
        & (df['Year'] <= to_year)
        & (from_year <= df['Year'])
        & (df['Demographic'].isin(selected_demo_names))
        ]

    return selected_recipients, selected_tobs, selected_demo_names, filtered_df


def multiselect_plot(selected_recipients, selected_tobs, selected_demo_names, filtered_df, colors, from_year, to_year):
    fig = go.Figure()
    i = 0
    for recipient in selected_recipients:
        graph_df = filtered_df[filtered_df['Recipient'] == recipient]
        for selected_tob in selected_tobs:
            for selected_demo_name in selected_demo_names:
                graph_df2 = graph_df[graph_df['Demographic'] == selected_demo_name]
                label_style = utils.get_figure_labels(selected_recipients, recipient, selected_tobs,
                                                      selected_tob, selected_demo_names, selected_demo_name)
                fig.add_trace(go.Scatter(
                    x=graph_df2['Year'],
                    y=graph_df2[f'{selected_tob}_V'],
                    mode='lines+markers',
                    name=label_style,
                    line=dict(color=colors[i % len(colors)]),
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
        xaxis_title={
            'text': 'Year',
            'font': {'color': '#444444',
                     'size': 16},
        },
        yaxis_title={
            'text': 'Prevalence',
            'font': {'color': '#444444',
                     'size': 16},
        },
        # height=500,
        # width=800,
        xaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,
            tickformat='.0f',
            tickfont=dict(
                color='#444444',
                size=14)
        ),
        yaxis=dict(
            rangemode='tozero',
            tickfont=dict(
                color='#444444',
                size=14)
        )
    )

    fig.update_layout(
        legend={
            "font": {
                "family": "verdana",
                "size": 12,
            }}
    )

    name = f'{title_info} — BRFSS {from_year} to {to_year}: {subtitle_info}'

    return fig, name

def basic_plot(selected_recipient, selected_tob, selected_demo_name, filtered_df, colors, from_year, to_year):
    fig = go.Figure()

    i = 0
    for demo_name in filtered_df['Demographic'].unique():
        df_demo = filtered_df[filtered_df['Demographic'] == demo_name]

        fig.add_trace(go.Scatter(
            x=df_demo['Year'],
            y=df_demo[f'{selected_tob}_V'],
            mode='lines+markers',
            line=dict(color=colors[i % len(colors)]),
            marker=dict(color=colors[i % len(colors)], size=8),
            name=demo_name,
            error_y=dict(
                type='data',
                array=df_demo[f'{selected_tob}_U'] - df_demo[f'{selected_tob}_V'],
                arrayminus=df_demo[f'{selected_tob}_V'] - df_demo[f'{selected_tob}_L']
            )
        ))
        i += 1
    tickvals = filtered_df['Year'].unique()
    ticktext = [str(int(year)) for year in tickvals]

    title_info = utils.get_figure_title([selected_tob])
    subtitle_info = utils.get_figure_subtitle([selected_recipient], [selected_demo_name])
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
        xaxis_title={
            'text': 'Year',
            'font': {'color': '#444444',
                     'size': 16},
        },
        yaxis_title={
            'text': 'Prevalence',
            'font': {'color': '#444444',
                     'size': 16},
        },
        # height=500,
        # width=800,
        xaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,
            tickformat='.0f',
            tickfont=dict(
                color='#444444',
                size=14)
        ),
        yaxis=dict(
            rangemode='tozero',
            tickfont=dict(
                color='#444444',
                size=14)
        )
    )

    fig.update_layout(
        legend={
            "font": {
                "family": "verdana",
                "size": 12,
                "color": '#444444'
            }}
    )

    # fig.update_layout(
    #     legend=dict(
    #         yanchor="top",
    #         y=0.99,
    #         xanchor='right',
    #         x=0.99,
    #         bgcolor='rgba(255,255,255,0.5)'
    #     )
    # )

    name = f'{title_info} — BRFSS {from_year} to {to_year}: {subtitle_info}'

    return fig, name
