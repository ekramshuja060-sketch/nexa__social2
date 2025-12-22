import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# مدل User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(200), default="https://picsum.photos/100")

# مدل Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# نمونه داده‌ها
users = [
    {"username": "ekram", "bio": "عاشق برنامه‌نویسی 🚀", "profile_image": "https://picsum.photos/100/100"},
    {"username": "shuja", "bio": "دوستدار سفر و عکاسی 😎", "profile_image": "https://picsum.photos/101/100"}
]

posts = [
    {"id": 1, "user": "ekram", "content": "سلام دنیا! این اولین پستم هست 🚀", "image_url": "https://picsum.photos/500/300", "likes": 10, "comments": 2},
    {"id": 2, "user": "shuja", "content": "یک روز عالی در کنار دوستان 😎", "image_url": "https://picsum.photos/500/301", "likes": 7, "comments": 1}
]

# روت اصلی
@app.route("/")
def home():
    return render_template("home.html", posts=posts)

# ایجاد پست جدید
@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        username = request.form.get("username")
        content = request.form.get("content")
        image_url = request.form.get("image_url")
        if username and content:
            post_id = max([p["id"] for p in posts] + [0]) + 1
            posts.append({
                "id": post_id,
                "user": username,
                "content": content,
                "image_url": image_url,
                "likes": 0,
                "comments": 0
            })
            return redirect(url_for("home"))
    return render_template("new_post.html", users=users)

# لایک پست
@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break
    return redirect(url_for("home"))

# کامنت پست
@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    comment_text = request.form.get("comment")
    for post in posts:
        if post["id"] == post_id and comment_text:
            post["comments"] += 1
            break
    return redirect(url_for("home"))

# پروفایل کاربر
@app.route("/profile/<username>")
def profile(username):
    user_info = next((u for u in users if u["username"] == username), None)
    user_posts = [post for post in posts if post["user"] == username]
    return render_template("profile.html", user=user_info, posts=user_posts)

# ساخت دیتابیس
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
# ویرایش پست
@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return redirect(url_for("home"))

    if request.method == "POST":
        content = request.form.get("content")
        file = request.files.get("image_file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            post["image_url"] = url_for("static", filename=f"uploads/{filename}")

        if content:
            post["content"] = content

        return redirect(url_for("home"))

    return render_template("edit_post.html", post=post)

# حذف پست
@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return redirect(url_for("home"))
