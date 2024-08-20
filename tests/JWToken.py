from services import token_validate
from api.auth_routes import SECRET_KEY as KEY



print(token_validate(input(), KEY))
