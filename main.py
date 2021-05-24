from flask import Flask, render_template, url_for, request, abort, Response
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
from collections import defaultdict
from datetime import datetime

import os


app = Flask(__name__)
UPLOAD_FOLDER = "static/uploaded_files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usr_login_password.db"
db = SQLAlchemy(app)


class UserLoginPassword(db.Model):
    """ {} """
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date_ = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return "<UserLoginPassword %r>" % self.user_id


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password"),
    3: User(3, "admin", "admin")
}


# create dict for users checks
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))


# for reload css (crtl+shift+r)
def get_files_from_src_folder():
    import os
    path = os.getcwd()+"/static/src"
    HTML_CODE = """ """
    for filename in os.listdir(path):
        fn = f"<p><a href='static/src/{filename}' download='{filename}' style='font-size: 35px; color: red'>Скачать {filename}</a></p>\n"
        HTML_CODE += fn
    return HTML_CODE

def get_files_from_upload_folder():
    import os
    path = os.getcwd()+"/static/uploaded_files"
    HTML_CODE = """ """
    for filename in os.listdir(path):
        fn = f"<p><a href='static/uploaded_files/{filename}' download='{filename}' style='font-size: 35px; color: red'>Скачать {filename}</a></p>\n"
        HTML_CODE += fn
    return HTML_CODE


@app.route("/")
@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/home")
@login_required
def home_page():
    return render_template("home.html")


@app.route("/user/<string:name>/<int:id>")
def user_page(name, id):
    return "__user__" + name + " " + str(id)


@app.route("/download")
@login_required
def download_page():
    link_to_src_file = get_files_from_src_folder()
    link_to_upload_file = get_files_from_upload_folder()
    main_page = """
        <title>local_server</title>\n
        <h1 style="color: #999999">-->Main page <a href="main"><span>/main</span></a></h1\>\n
        """
    download_code = """
    <h1 style="color: #20f">-->Download<--</h1>\n
    """ + link_to_src_file
    upload_code = """
    <h1 style="color: #20f">-->Uploaded<--</h1>\n
    """ + link_to_upload_file
    return "<div>" + main_page + download_code + upload_code + "</div>"


@app.route("/upload", methods = ["GET", "POST"])
@login_required
def upload_page():
    if request.method == "POST":
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return render_template("upload.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # Проверка пользователя
        if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
            # Войти, если пользователь существует
            login_user(users.get(user_check[request.form["username"]]["id"]))
            return render_template("redirect_authorized_user.html")
            #Response("""
            #login success!<br/>
            #<a href="/main">Go to main</a><br/>
            #<a href="/logout">logout</a>
            #""")
        else:
            return abort(401)
    else:
        return render_template("login.html")
        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("logout.html")
    #Response("""
    #logout success!<br />
    #<a href="/login/">login</a>
    #""")


if __name__ == "__main__":
    #app.run(host="192.168.1.6", port="1111", debug=True)
    app.run(host="192.168.43.157", port="5555", debug=False)
