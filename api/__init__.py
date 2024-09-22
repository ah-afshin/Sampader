from flask import Flask
from database import shutdown_session
from extensions import limiter


def create_app():
    # app = Flask(__name__)
    app = Flask("Sampader")

    # import APIs
    from .user_routes import user_bp
    from .post_routes import post_bp
    from .auth_routes import auth_bp
    from .home_routes import home_bp

    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    # Register the teardown function to clean up the session
    @app.teardown_appcontext
    def shutdown_session_on_teardown(exception=None):
        shutdown_session()

    # Initialize the limiter with the app
    limiter.init_app(app)
    return app
