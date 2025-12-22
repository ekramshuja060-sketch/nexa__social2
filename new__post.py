@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        username = request.form.get("username")
        content = request.form.get("content")
        file = request.files.get("image_file")
        image_url = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_url = url_for("static", filename=f"uploads/{filename}")

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
