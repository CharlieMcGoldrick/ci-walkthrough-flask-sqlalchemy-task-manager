from flask import render_template, request, redirect, url_for, flash
from taskmanager import app, db
from taskmanager.models import Category, Task
from sqlalchemy.exc import IntegrityError


@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)


@app.route("/categories")
def categories():
    # Using the .all method will return a Cursor Object
    # Wrapping the variable inside of list() will convert back to py list  
    categories = list(Category.query.order_by(Category.category_name).all())
    # 1st categories is the variable name to be used within the HTML template
    # 2nd is the the variable name above that contains the list
    return render_template("categories.html", categories=categories)

# Category Routing
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

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Attempts to query the database and if no record is found it will 404
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)

@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

# Task Routing
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        try:
            task = Task(
                task_name=request.form.get("task_name"),
                task_description=request.form.get("task_description"),
                is_urgent=bool(True if request.form.get("is_urgent") else False),
                due_date=request.form.get("due_date"),
                category_id=request.form.get("category_id")
            )
            db.session.add(task)
            db.session.commit()
            flash("Task added successfully!", "success")  # Success message
            return redirect(url_for("home"))
        except IntegrityError:
            db.session.rollback()
            flash("Task already exists.", "error")  # Error message
            return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)