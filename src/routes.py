# routes

from flask import Blueprint, render_template, request, redirect, url_for
import os
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
from src.dashboardplots import sendDashboardPlots, treatData
import requests

df = None # Variável global para armazenar o DataFrame

# Criando um Blueprint chamado 'main'
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@main.route('/contato', methods=['GET'])
def contato():
    return render_template('contato.html')

@main.route('/submit', methods=['POST'])
def submit():
    global df
    file = request.files['file']
    
    df = treatData(file)
    
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard', methods=['GET'])
def dashboard():
    global df

    if df is None:
        return "Nenhum dado disponível. Faça o upload do arquivo primeiro!", 400

    graphs = sendDashboardPlots(df)
    return graphs

@main.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    google_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSe50UWDqY7JbJtV6IDEYyuSaQ5SrinJmtG6daXXdvB4jXpF5A/formResponse'
    form_data = {
        'entry.1691399787': name,
        'entry.1906101515': email,
        'entry.1535253285': message,
    }

    response = requests.post(google_form_url, data=form_data)

    if response.status_code == 200:
        return redirect(url_for('main.dashboard'))
    else:
        return "Falha ao enviar o formulário.", 500
