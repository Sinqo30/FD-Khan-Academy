from flask import Blueprint, render_template


payments = Blueprint(
    "payments",
    __name__
)


@payments.route("/payments")
def payment_page():

    return render_template(
        "store.html"
    )