from flask import Flask

from .routes import bp as main_bp


def create_app(config: dict | None = None) -> Flask:
    """Create and configure the Flask application.

    Registers blueprints from `app.routes`.
    """
    app = Flask(__name__)

    if config:
        app.config.update(config)

    # register routes defined in app/routes.py
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    # Allow running this module directly for quick manual tests
    create_app().run(debug=True, host="127.0.0.1", port=5000)
