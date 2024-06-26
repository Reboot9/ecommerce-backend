"""
Business logic to handle payment process in the ecommerce shop.
"""
import logging
from typing import Union

import requests
from django.utils import timezone
from liqpay import LiqPay
from rest_framework import status

from ecommerce_backend.settings import base

PUBLIC_KEY = base.LIQPAY_PUBLIC_KEY
PRIVATE_KEY = base.LIQPAY_PRIVATE_KEY
LIQPAY_CHECKOUT_URL = "https://www.liqpay.ua/api/3/checkout/"


class Payment:
    """Custom payment handling class using LiqPay API."""

    def __init__(self):
        """
        Initialize Payment object.
        """
        self.liqpay = LiqPay(PUBLIC_KEY, PRIVATE_KEY)
        self.data_const = {
            "public_key": PUBLIC_KEY,
            "version": "3",
        }

    def generate_new_url_for_pay(self, order_id, cost, *, text="") -> tuple[dict[str, str], int]:
        """
        Generate new payment url for order.

        :param order_id: id of order.
        :param cost: amount of money to be paid.
        :param text: additional text for payment description.
        :return: generated payment url or none if any error occurs.
        """
        data = {k: v for k, v in self.data_const.items()}

        data["action"] = "pay"
        data["amount"] = cost
        data["currency"] = "UAH"
        data["language"] = "uk"
        data["description"] = f"{text}"
        data["order_id"] = order_id

        # Couldn't resolve an issue that LiqPay doesn't send any requests to the server
        # data["server_url"] = f"http://host/api/orders/callback/"

        data_to_sign = self.liqpay.data_to_sign(data)
        params = {"data": data_to_sign, "signature": self.liqpay.cnb_signature(data)}

        try:
            response = requests.post(url=LIQPAY_CHECKOUT_URL, data=params)
            if response.status_code == 200:
                return {"payment_url": response.url}, status.HTTP_200_OK
            else:
                logging.warning(
                    f"[{timezone.localtime(timezone.now())}] "
                    f"| incorrect status code from response - {response.status_code}, "
                    f"has to be 200, data - {data}, params - {params}"
                )

                return (
                    {"message": f"Incorrect status code from response - {response.status_code}"},
                    status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except requests.RequestException as e:
            logging.exception(
                f"Error sending request to LiqPay: {e}, data - {data}, params - {params}"
            )

            return {"message": "Error processing payment"}, status.HTTP_503_SERVICE_UNAVAILABLE

    def get_order_status_from_liqpay(self, order_id) -> Union[dict, bool]:
        """
        Get a status of the order from LiqPay.

        :param order_id: id of the order.
        :return: order status or False if any error occurs
        """
        data = {k: v for k, v in self.data_const.items()}
        data["action"] = "status"
        data["order_id"] = order_id
        response = self.liqpay.api("request", data)
        if response.get("action") == "pay" and response.get("public_key") == PUBLIC_KEY:
            return response

        return False
