from flask import Blueprint, render_template


store = Blueprint(
    "store",
    __name__
)


@store.route("/store")
def store_page():

    return render_template(
        "store.html"
    )