import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ======================
# تنظیمات اولیه
# ======================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# ======================
# ابزارها
# ======================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ======================
# مدل‌ها
# ======================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(200), default="https://picsum.photos/100")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ======================
# داده تست
# ======================
users = [
    {"username": "ekram", "bio": "عاشق برنامه‌نویسی 🚀"},
    {"username": "shuja", "bio": "دوستدار سفر 😎"}
]

posts = []

# ======================
# روت‌ها
# ======================
@app.route("/")
def home():
    return render_template("home.html", posts=posts)

@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        user = request.form["user"]
        content = request.form["content"]
        file = request.files.get("image")

        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_url = f"/static/uploads/{filename}"

        posts.append({
            "id": len(posts) + 1,
            "user": user,
            "content": content,
            "image_url": image_url,
            "likes": 0
        })
        return redirect(url_for("home"))

    return render_template("new_post.html", users=users)

@app.route("/like/<int:id>")
def like(id):
    for p in posts:
        if p["id"] == id:
            p["likes"] += 1
    return redirect(url_for("home"))

# ======================
# اجرا
# ======================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
