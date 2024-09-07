# db statics
UPLOADS_PATH = "F://Sampader/uploads"
DATABASE_URI = "sqlite:///database/data.db"

# maximum length of database fields
MAX_USERNAME_LEN = 40
MAX_NAME_LEN = 80
MAX_EMAIL_LEN = 80
MAX_BIO_LEN = 200
MAX_PASSWORD_LEN = 80
MAX_POST_LEN = 300

# lists of valid values
school_and_class = ["101", "102", "103", "104", "201", "202", "203", "204", "301", "302", "303", "304",]
verified = [
    "f", # f not verified
    "o", # o official verifiction
    "a", # a verified as admin
    "s", # s verified as council
    "c", # c verified as celebrity
]
notification_type = [
    "l", # like
    "c", # comment
    "f", # follow
]
