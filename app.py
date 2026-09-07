from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM properties")
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

    connection = sqlite3.connect("campusbridge.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
        (property_id, rating, review_text)
    )
    connection.commit()
    connection.close()

    return redirect(url_for("property_detail", property_id=property_id))

if __name__ == "__main__":
    app.run(debug=True)