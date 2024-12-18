from flask import Flask
import webbrowser
from src.routes import main


def create_app():
    app = Flask(__name__)

    # Importando e registrando o Blueprint
    app.register_blueprint(main)

    return app

# Função para abrir o navegador automaticamente
def open_browser(adress='http://127.0.0.1:5000'):
    webbrowser.open_new(adress)


if __name__ == '__main__':
    app = create_app()
    open_browser()
    app.run(debug=False)