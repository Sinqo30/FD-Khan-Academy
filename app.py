from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Change this later to something secure
app.secret_key = "fd-khan-secret-key"


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
# ADMIN LOGIN
# ==========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # TEMPORARY LOGIN
        if username == "admin" and password == "1234":

            session["logged_in"] = True

            return redirect("/dashboard")

        return """
        <h2>Incorrect Username or Password</h2>
        <a href='/admin'>Try Again</a>
        """

    return render_template("admin_login.html")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect("/admin")

    return render_template("admin_dashboard.html")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)