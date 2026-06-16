from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = "fd-khan-secret-key"

# Temporary booking storage
bookings = []


# ==========================
# PUBLIC PAGES
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/store")
def store():
    return render_template("store.html")


# ==========================
# BOOKING SUBMISSION
# ==========================

@app.route("/submit_booking", methods=["POST"])
def submit_booking():

    booking = {
        "name": request.form["name"],
        "email": request.form["email"],
        "subject": request.form["subject"],
        "message": request.form["message"]
    }

    bookings.append(booking)

    return redirect("/booking")


# ==========================
# ADMIN LOGIN
# ==========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

            session["logged_in"] = True

            return redirect("/dashboard")

        return """
        <h2>Incorrect Username or Password</h2>
        <a href="/admin">Try Again</a>
        """

    return render_template("admin_login.html")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect("/admin")

    return render_template(
        "admin_dashboard.html",
        bookings=bookings
    )


# ==========================
# DELETE BOOKING
# ==========================

@app.route("/delete_booking/<int:booking_id>")
def delete_booking(booking_id):

    if not session.get("logged_in"):
        return redirect("/admin")

    if 0 <= booking_id < len(bookings):
        bookings.pop(booking_id)

    return redirect("/dashboard")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)