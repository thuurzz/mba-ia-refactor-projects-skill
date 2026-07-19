from waitress import serve

from src.app import create_app


app = create_app()


if __name__ == "__main__":
    serve(app, host=app.config["HOST"], port=app.config["PORT"])
