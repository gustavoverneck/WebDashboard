from flask import Flask
import webview
from src.routes import main


def create_app():
    app = Flask(__name__)
    window = webview.create_window('WebDashboard', app, min_size=(1200, 800))

    # Importando e registrando o Blueprint
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app = create_app()
    #app.run(debug=False)
    webview.start()