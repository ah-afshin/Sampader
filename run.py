# import tests.db
# import tests.services
# import tests.JWToken

from api import create_app
from admin import admin_bp

app = create_app()
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    print("starting the app.")
    app.run(debug=True)
