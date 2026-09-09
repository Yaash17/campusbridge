from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "test"
ADMIN_PASSWORD = "test"

@app.route("/")
def home():
    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT properties.id, properties.name, properties.area, properties.university,
               AVG(reviews.rating), COUNT(reviews.id)
        FROM properties
        LEFT JOIN reviews ON reviews.property_id = properties.id
        GROUP BY properties.id
    """)
    properties = cursor.fetchall()
    connection.close()
    return render_template("index.html", properties=properties)

@app.route("/property/<int:property_id>")
def property_detail(property_id):
    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    property = cursor.fetchone()
    cursor.execute("SELECT * FROM reviews WHERE property_id = ?", (property_id,))
    reviews = cursor.fetchall()
    connection.close()
    return render_template("property.html", property=property, reviews=reviews)

@app.route("/property/<int:property_id>/review", methods=["POST"])
def add_review(property_id):
    rating = request.form["rating"]
    review_text = request.form["review_text"]

    try:
        rating = int(rating)
    except ValueError:
        return "Invalid rating — please enter a whole number.", 400

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5.", 400

    if not review_text.strip():
        return "Review text can't be empty.", 400

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
        (property_id, rating, review_text)
    )
    connection.commit()
    connection.close()

    flash("Review submitted!")

    return redirect(url_for("property_detail", property_id=property_id))

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
        (property_id, rating, review_text)
    )
    connection.commit()
    connection.close()

    return redirect(url_for("property_detail", property_id=property_id))

@app.route("/add-property", methods=["GET", "POST"])
def add_property():
    if request.method == "POST":
        name = request.form["name"]
        area = request.form["area"]
        university = request.form["university"]

        if not name.strip():
            return "Property name can't be empty.", 400

        connection = sqlite3.connect("campusbridge.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO properties (name, area, university) VALUES (?, ?, ?)",
            (name, area, university)
        )
        connection.commit()
        connection.close()

        flash("Property added!")

        return redirect(url_for("home"))

    return render_template("add_property.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Incorrect password.", 401

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    connection.close()

    return render_template("admin_dashboard.html", properties=properties, reviews=reviews)

@app.route("/admin/delete-property/<int:property_id>", methods=["POST"])
def delete_property(property_id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reviews WHERE property_id = ?", (property_id,))
    cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)