# import tests.db
# import tests.services
# import tests.JWToken
# import tests.image_service
# import tests.post_creator
# import tests.admin_creator

from api import create_app
from admin import admin_bp, KEY

app = create_app()
app.register_blueprint(admin_bp)
app.secret_key = KEY

if __name__ == "__main__":
    print("starting the app.")
    app.run(debug=True)
