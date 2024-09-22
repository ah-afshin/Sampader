from api import create_app
from admin import admin_bp
from configs import SESSION_KEY


app = create_app()
app.register_blueprint(admin_bp)
app.secret_key = SESSION_KEY

if __name__ == "__main__":
    app.run()
