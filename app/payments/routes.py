import requests

from flask import Blueprint, jsonify, request

from flask_login import login_required, current_user

from ..models import Video, Purchase

from ..extensions import db

from config import Config



payments = Blueprint(
    "payments",
    __name__
)



def get_paypal_token():

    response = requests.post(

        "https://api-m.paypal.com/v1/oauth2/token",

        auth=(

            Config.PAYPAL_CLIENT_ID,

            Config.PAYPAL_CLIENT_SECRET

        ),

        data={

            "grant_type":
            "client_credentials"

        }

    )


    return response.json()["access_token"]





@payments.route(
    "/create-order/<int:lesson_id>",
    methods=["POST"]
)
@login_required
def create_order(lesson_id):


    lesson = Video.query.get_or_404(
        lesson_id
    )


    token = get_paypal_token()



    response = requests.post(

        "https://api-m.paypal.com/v2/checkout/orders",

        headers={

            "Authorization":
            f"Bearer {token}",

            "Content-Type":
            "application/json"

        },


        json={

            "intent":
            "CAPTURE",


            "purchase_units":[

                {

                    "amount":{

                        "currency_code":
                        "USD",

                        "value":
                        str(lesson.price)

                    }

                }

            ]

        }

    )


    return jsonify(
        response.json()
    )





@payments.route(
    "/capture-order",
    methods=["POST"]
)
@login_required
def capture_order():


    data = request.json


    order_id = data["orderID"]

    lesson_id = data["lessonID"]



    token = get_paypal_token()



    response = requests.post(

        f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture",


        headers={

            "Authorization":
            f"Bearer {token}",

            "Content-Type":
            "application/json"

        }

    )


    result = response.json()



    if result.get("status") == "COMPLETED":


        lesson = Video.query.get_or_404(
            lesson_id
        )


        purchase = Purchase(

            student_id=current_user.id,

            video_id=lesson.id,

            amount=lesson.price,

            payment_status="Completed"

        )


        db.session.add(
            purchase
        )

        db.session.commit()



        return jsonify(
            {
                "success": True
            }
        )



    return jsonify(
        {
            "success": False
        }
    )