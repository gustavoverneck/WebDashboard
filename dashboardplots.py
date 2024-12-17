# dashboardplots.py

import os
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder


def convert_to_json(fig):
        return fig.to_json()

def sendDashboardPlots(df):
    if df is None:
        return "Nenhum dado disponível. Faça o upload do arquivo primeiro!", 400

    ########################################################
    # Adicionar gráficos personalizados
    
    # Gráfico de barras
    fig_bar = px.bar(df, x=df.columns[1], y=df.columns[2], title='Gráfico de Barras')
    graph_json1 = convert_to_json(fig_bar)

    # Gráfico de linhas
    fig_line = px.line(df, x=df.columns[1], y=df.columns[2], title='Gráfico de Linhas')
    graph_json2 = convert_to_json(fig_line)

    # Gráfico de dispersão
    fig_scatter = px.scatter(df, x=df.columns[1], y=df.columns[2], title='Gráfico de Dispersão')
    graph_json3 = convert_to_json(fig_scatter)

    # Gráfico de pizza
    fig_pie = px.pie(df, values=df.columns[2], names=df.columns[1], title='Gráfico de Pizza')
    graph_json4 = convert_to_json(fig_pie)

    ########################################################
    
    # Passando o JSON para o HTML -> Adicione todos os gráficos que desejar
    return render_template('dashboard.html', graph1=graph_json1, graph2=graph_json2, graph3=graph_json3, graph4=graph_json4)