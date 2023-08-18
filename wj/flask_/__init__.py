from flask import Flask
from Wav2Lip.inference import load_model


def create_app():
    app = Flask(__name__)

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='0.0.0.0', port=5000)