from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..models import User


auth = Blueprint(
    "auth",
    __name__
)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )


        user.set_password(password)


        db.session.add(user)

        db.session.commit()


        flash(
            "Account created. Please login.",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "register.html"
    )





@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        user = User.query.filter_by(
            email=email
        ).first()


        if user and user.check_password(password):

            login_user(user)


            if user.is_admin:

                return redirect(
                    url_for("admin.dashboard")
                )


            return redirect(
                url_for("student.dashboard")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )





@auth.route("/logout")
@login_required
def logout():

    logout_user()


    return redirect(
        url_for("home")
    )
@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]


        if not current_user.check_password(current_password):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )


        current_user.set_password(new_password)

        db.session.commit()


        flash(
            "Password updated successfully.",
            "success"
        )


        return redirect(
            url_for("student.dashboard")
        )


    return render_template(
        "change_password.html"
    )