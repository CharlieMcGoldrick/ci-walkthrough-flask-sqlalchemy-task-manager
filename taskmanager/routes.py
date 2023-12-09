from flask import render_template, request, redirect, url_for, flash
from taskmanager import app, db
from taskmanager.models import Category, Task
from sqlalchemy.exc import IntegrityError


@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        # Format the input to handle casing duplicates
        category_name = request.form.get("category_name").capitalize()
        try:
            category = Category(category_name=category_name)
            db.session.add(category)
            db.session.commit()
            flash("Category added successfully!", "success")  # Success message
            return redirect(url_for("categories"))
        except IntegrityError:
            db.session.rollback()
            flash("Category already exists.", "error")  # Error message
            return redirect(url_for("categories"))
    return render_template("add_category.html")

