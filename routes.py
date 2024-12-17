# routes

from flask import Blueprint, render_template, request, redirect, url_for
import os
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
from dashboardplots import sendDashboardPlots

df = None # Variável global para armazenar o DataFrame

# Criando um Blueprint chamado 'main'
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/sobre')
def sobre():
    return render_template('sobre.html')

@main.route('/submit', methods=['POST'])
def submit():
    global df
    file = request.files['file']
    if file:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return 'Formato de arquivo não suportado!', 400
    else:
        return 'Nenhum arquivo enviado!', 400
    
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard', methods=['GET'])
def dashboard():
    global df

    if df is None:
        return "Nenhum dado disponível. Faça o upload do arquivo primeiro!", 400

    graphs = sendDashboardPlots(df)

    return graphs    # Enviando os gráficos para a página HTML
