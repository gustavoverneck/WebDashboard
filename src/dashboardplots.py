# dashboardplots.py

import os
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from PIL import Image
import plotly.graph_objects as go


def convert_to_json(fig):
        return fig.to_json()

def treatData(file):
    # Tratamento dos dados
    if file:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, sheet_name=2, skiprows=6, usecols="B:I")
            df = df.iloc[:-1]
        else:
            return 'Formato de arquivo não suportado!', 400
    else:
        return 'Nenhum arquivo enviado!', 400
    
    df.columns = [
    'Meses', 
    'SP_2022', 'SP_2023', 
    'ES_2022', 'ES_2023', 'ES_2024',
    'RJ_2022', 'RJ_2023'
    ]
    return df              


def sendDashboardPlots(df):
    if df is None:
        # Alterar o tamanho da fonte de todos os gráficos
        for fig in [fig_line, fig_bar, fig_logo, fig_total]:
            fig.update_layout(font=dict(size=18))
        return "Nenhum dado disponível. Faça o upload do arquivo primeiro!", 400

    ########################################################
    # Adicionar gráficos personalizados
    MESES = df.columns[0]
    print(df[df.columns[1]])
    df[df.columns[1]] = df[df.columns[1]].astype(float) # SP 2022 - 1
    df[df.columns[2]] = df[df.columns[2]].astype(float) # SP 2023 - 2
    df[df.columns[3]] = df[df.columns[3]].astype(float) # ES 2022 - 3
    df[df.columns[4]] = df[df.columns[4]].astype(float) # ES 2023 - 4
    df[df.columns[5]] = df[df.columns[5]].astype(float) # ES 2024 - 5
    df[df.columns[6]] = df[df.columns[6]].astype(float) # RJ 2022 - 6
    df[df.columns[7]] = df[df.columns[7]].astype(float) # RJ 2023 - 7

    ANO2022 = [df.columns[3], df.columns[6], df.columns[1]]
    ANO2023 = [df.columns[4], df.columns[7], df.columns[2]]
    ANO2024 = [df.columns[5]]

    nomes = ["ES", "RJ", "SP"]

# Gráfico de Orçamentos 2022
    fig_line = go.Figure()
    # Adiciona uma linha para cada ano no mesmo gráfico, inicialmente visível apenas 2022
    for i, column in enumerate(ANO2022):
        fig_line.add_trace(go.Scatter(x=df[MESES], y=df[column], mode='lines+markers', name=nomes[i], visible=True))
    for j, column in enumerate(ANO2023):
        fig_line.add_trace(go.Scatter(x=df[MESES], y=df[column], mode='lines+markers', name=nomes[j], visible=False))
    for k, column in enumerate(ANO2024):
        fig_line.add_trace(go.Scatter(x=df[MESES], y=df[column], mode='lines+markers', name=nomes[k], visible=False))
    
    fig_line.update_xaxes(tickvals=list(range(1, 13)))
    fig_line.update_xaxes(ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    # Adicionar Dropdown Menu
    fig_line.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(label="2022",
                         method="update",
                         args=[{"visible": [True] * len(ANO2022) + [False] * (len(ANO2023) + len(ANO2024))},
                               {"title": "Faturamento Mensal 2022"}]),

                    dict(label="2023",
                         method="update",
                         args=[{"visible": [False] * len(ANO2022) + [True] * len(ANO2023) + [False] * len(ANO2024)},
                               {"title": "Faturamento Mensal 2023"}]),

                    dict(label="2024",
                         method="update",
                         args=[{"visible": [False] * (len(ANO2022) + len(ANO2023)) + [True] * len(ANO2024)},
                               {"title": "Faturamento Mensal 2024"}]),
                ],
                direction="down",
                showactive=True,
                x=0.1,
                y=1.15,
                xanchor='left',
                yanchor='top'
            )
        ]
    )


    # Configuração do layout
    fig_line.update_layout(
        title="<b>Faturamento Mensal por Ano</b>",
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)",
        template="plotly",
    )

# Gráfico Faturamento anual por estado
    df_annual = df.groupby(df.columns[0]).sum().reset_index()
    df_annual_sum = df_annual.sum(axis=0)[1:].values

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(x=nomes, y=[df[ANO2022[0]].sum(), df[ANO2022[1]].sum(), df[ANO2022[2]].sum()], name='2022', text=[f'<b>{val/1e6:.2f}M</b>' for val in [df[ANO2022[0]].sum(), df[ANO2022[1]].sum(), df[ANO2022[2]].sum()]], textposition='auto'))
    fig_bar.add_trace(go.Bar(x=nomes, y=[df[ANO2023[0]].sum(), df[ANO2023[1]].sum(), df[ANO2023[2]].sum()], name='2023', text=[f'<b>{val/1e6:.2f}M</b>' for val in [df[ANO2023[0]].sum(), df[ANO2023[1]].sum(), df[ANO2023[2]].sum()]], textposition='auto'))
    fig_bar.add_trace(go.Bar(x=nomes, y=[df[ANO2024[0]].sum()], name='2024', text=[f'<b>{val/1e6:.2f}M</b>' for val in [df[ANO2024[0]].sum()]], textposition='auto'))

    fig_bar.update_layout(
        title="<b>Faturamento Anual por Estado</b>",
        xaxis_title="Estado",
        yaxis_title="Orçamento Anual (R$)",
        barmode='group',
        template="plotly",
    )


    # Gráfico 3 com logo da Blu
    fig_logo = go.Figure()

    # Adicionar imagem ao gráfico
    fig_logo.add_layout_image(
        dict(
            source=Image.open('static/Blu.png'),
            xref="paper", yref="paper",
            x=0.5, y=0.7,
            sizex=0.7, sizey=0.7,
            xanchor="center", yanchor="middle"
        )
    )

    fig_logo.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly",
        paper_bgcolor='white',  # Define o fundo como branco
        plot_bgcolor='white'    # Define o fundo do gráfico como branco
    )


# Quadro com valor de faturamento anual total
    fig_total = go.Figure()
    fig_total.add_trace(go.Indicator(
        mode="number",
        value=df[ANO2022].sum().sum(),
        title={"text": "<b>2022</b>", "font": {"size": 32, "color": "rgb(99, 110, 250)"}},
        number={"font": {"size": 38, "weight": "bold"}},
        domain={'row': 0, 'column': 0}
    ))
    fig_total.add_trace(go.Indicator(
        mode="number",
        value=df[ANO2023].sum().sum(),
        title={"text": "<b>2023</b>", "font": {"size": 32, "color": "rgb(239, 85, 59)"}},
        number={"font": {"size": 38, "weight": "bold"}},
        domain={'row': 0, 'column': 1}
    ))
    fig_total.add_trace(go.Indicator(
        mode="number",
        value=df[ANO2024].sum().sum(),
        title={"text": "<b>2024</b>", "font": {"size": 32, "color": "rgb(0, 204, 150)"}},
        number={"font": {"size": 38, "weight": "bold"}},
        domain={'row': 0, 'column': 2}
    )) 

    fig_total.update_layout(
        title="<b>Faturamento Anual Total (em reais)</b>",
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        template="plotly"
    )

# Configuração do layout

    # Alterar o tamanho da fonte
    fig_line.update_layout(font=dict(size=18))
    fig_bar.update_layout(font=dict(size=18))
    fig_total.update_layout(font=dict(size=18))

    # Converter o gráfico para JSON
    graph_json1 = convert_to_json(fig_line)
    graph_json2 = convert_to_json(fig_bar)
    graph_json3 = convert_to_json(fig_logo)
    graph_json4 = convert_to_json(fig_total)

    ########################################################
    
    # Passando o JSON para o HTML -> Adicione todos os gráficos que desejar

    return render_template('dashboard.html', graph1=graph_json1, graph2=graph_json2, graph3=graph_json3, graph4=graph_json4)