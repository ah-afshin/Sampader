from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    request
)
import json, jwt
from datetime import (
    datetime,
    timedelta
)
import sqlite3 as sql
import services as srv


admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates')
ROOT_PATH = "F://Sampader/admin"
DB_PATH = "F://Sampader/database/data.db"
KEY = "cthc-mowz"


def sessionverified(session:dict):
    try:
        now = datetime.now().strftime("%Y%m%d%H%M")
        data = jwt.decode(session['admin'], KEY, algorithms=["HS256"])
        if datetime.strptime(data["ex"], "%Y%m%d%H%M") > datetime.strptime(now, "%Y%m%d%H%M"):
            return True, data["id"]
        return False, (now, data["ex"])
    except:
        return False, "b"
def new_admin(username, password):
    adminData = json.loads(
        open(f"{ROOT_PATH}/data.json", encoding="utf-8").read()
    )
    adminActivityData = json.loads(
        open(f"{ROOT_PATH}/activity.json", encoding="utf-8").read()
    )
    newAdminId = str(len(adminData) + 1)
    adminData[newAdminId] = {
        "username": username,
        # "password": bcrypt.hashpw(password.encode("utf-8")).decode("utf-8")
        "password": password
    }
    adminActivityData[username] = {}
    with open(f"{ROOT_PATH}/data.json", "w", encoding="utf-8") as f:
        json.dump(adminData, f, ensure_ascii=False, indent=4)
    with open(f"{ROOT_PATH}/activity.json", "w", encoding="utf-8") as f:
        json.dump(adminActivityData, f, ensure_ascii=False, indent=4)

def new_activity(username, data):
    adminActivityData = json.loads(
        open(f"{ROOT_PATH}/activity.json", encoding="utf-8").read()
    )
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d-%H:%M:%S")
    adminActivityData[username][now_str] = data
    with open(f"{ROOT_PATH}/activity.json", "w", encoding="utf-8") as f:
        json.dump(adminActivityData, f, ensure_ascii=False, indent=4)


@admin_bp.route('/admin')
def home():
    s, a = sessionverified(session)
    if s:
        return render_template('index.html')
    return redirect('/admin/login')

@admin_bp.route('/admin/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        userData = json.loads(open(f"{ROOT_PATH}/data.json", encoding="utf-8").read())
        pass_word = ""
        for userId in userData:
            if userData[userId]["username"] == username:
                pass_word = userData[userId]["password"]
        if pass_word == password:
            date = datetime.now()+timedelta(minutes=30)
            data = {
                "id": username,
                "ex": date.strftime("%Y%m%d%H%M")
            }
            session['admin'] = jwt.encode(data, KEY, algorithm="HS256")
            return redirect('/admin')
        return render_template("login.html")
    else:
        return render_template("login.html")

@admin_bp.route('/admin/verify', methods=["GET", "POST"])
def verify():
    s, a = sessionverified(session)
    if s:
        if request.method=="POST":
            username = request.form["username"]
            userid = srv.get_user_by_username(username).userID
            mode = request.form["mode"]
            if srv.verify(userid, mode):
                new_activity(a ,f"user <{userid}> verified as {mode}.")
                return render_template('done.html', data=f"user <{userid}> verified as {mode}.")
            return render_template("verify.html")
        return render_template("verify.html")
    return redirect('/admin/login')

@admin_bp.route('/admin/query', methods=["GET", "POST"])
def set_query():
    s, a = sessionverified(session)
    if s:
        if request.method=="POST":
            q = request.form['q']
            con = sql.connect(DB_PATH)
            cur = con.cursor()
            cur.execute(q)
            con.commit()
            con.close()
            new_activity(a, q)
            return render_template('done.html', data=q)
        return render_template("get_query.html")
    return redirect('/admin/login')

@admin_bp.route('/admin/select', methods=["GET", "POST"])
def get_query():
    s, a = sessionverified(session)
    if s:
        if request.method=="POST":
            q = request.form['q']
            con = sql.connect(DB_PATH)
            cur = con.cursor()
            cur.execute(q)
            data = cur.fetchall()
            con.close()
            new_activity(a, q)
            return render_template('report.html', data=data)
        return render_template("get_query.html")
    return redirect('/admin/login')

@admin_bp.route('/admin/new', methods=["GET", "POST"])
def add_new_admin():
    s, a = sessionverified(session)
    if s:
        if request.method=="POST":
            username = request.form['username']
            password = request.form['password']
            new_admin(username, password)
            new_activity(a, f"new admin <{username}>.")
            return render_template('done.html', data=f"new admin <{username}>.")
        return render_template("new_admin.html")
    return redirect('/admin/login')
