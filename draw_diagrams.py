import numpy as np
import pandas as pd
import plotly.graph_objects as go


def draw_health_distribution(sequences, health_fun):
    # https://towardsdatascience.com/create-binomial-distribution-graph-using-plotly-python-18eb92c2c78
    health_values = []
    for s in sequences:
        health_values.append(health_fun(s))

    data = build_health_freq_data_frame(health_values)

    fig = go.Figure(
        # Loading the data into the figure
        data=[go.Scatter(x=data['Health'], y=data['Frequency'],
                         mode="lines",
                         line=dict(width=2, color="blue"))],
        # Setting the layout of the graph
        layout=go.Layout(
            xaxis=dict(range=[min(health_values), max(health_values)], autorange=False),
            yaxis=dict(range=[data['Frequency'].min(), data['Frequency'].max()], autorange=False),
            title="Binomial Curve",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ))
    fig.show()


def build_health_freq_data_frame(health_values):
    # Creating X array for numbers between the maximum and minimum values of y and making it a dataframe
    x = np.arange(min(health_values), max(health_values))
    xx = pd.DataFrame(x)

    # Making y a dataframe and generating an empty array yy
    d = pd.DataFrame(health_values, columns=['Health'])
    yy = []

    # Calculating frequency of all numbers between maximum and minimum values
    for k in range(len(x)):
        yy.append(d[d['Health'] == x[k]].count()[0])

    # Making frequency data frame and concatenating it with the xx
    freq = pd.DataFrame(yy, columns=['Frequency'])
    data = pd.concat([xx, freq], axis=1)
    data.columns = ['Health', 'Frequency']
    return data
