from flask import Flask
from routes import df

def create_app():
    app = Flask(__name__)

    # Importando e registrando o Blueprint
    from routes import main
    app.register_blueprint(main)

    return app


app = create_app()

app.run(debug=True)