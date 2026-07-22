from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/dashboard")
@login_required
def dashboard():

    if not current_user.is_admin:

        return redirect(
            url_for("student.dashboard")
        )


    return render_template(
        "admin_dashboard.html"
    )