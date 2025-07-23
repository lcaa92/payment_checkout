import os
import requests
from .interfaces import ProviderIntegrationBase
from fastapi import status
from models.payments import PaymentStatus


class Provider1Integration(ProviderIntegrationBase):

    _BASE_URL = os.getenv("PROVIDER1_URL", "http://localhost:8001")

    def _build_payment_request(self, payment_data: dict) -> dict:
        """
        Build the payment request data structure for Provider 1.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary formatted for Provider 1.
        """
        return {
            "amount": payment_data["amount"],
            "currency": payment_data["currency"],
            "description": payment_data.get("description"),
            "paymentMethod": {
                "type": "card",
                "card": {
                    "number": payment_data["paymentInfo"]["number"],
                    "holderName": payment_data["paymentInfo"]["holderName"],
                    "cvv": payment_data["paymentInfo"]["cvv"],
                    "expirationDate": payment_data["paymentInfo"]["expiration"],
                    "installments": payment_data["paymentInfo"]["installments"]
                }
            }
        }

    def process_payment(self, payment_data: dict) -> dict:
        """
        Process a payment with the given data.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary with the result of the payment processing.
        """
        payload = self._build_payment_request(payment_data)

        response = requests.post(f"{self._BASE_URL}/charges", json=payload)

        if response.status_code != status.HTTP_201_CREATED:
            raise Exception(f"Failed to process payment: {response.json()}")
        return response.json()

    def get_status_from_response(self, response: dict) -> str:
        """
        Extract the payment status from the response.

        :param response: Dictionary containing the response data.
        :return: Payment status as a string.
        """
        status = {
            "authorized": PaymentStatus.completed,
            "failed": PaymentStatus.failed,
            "refunded": PaymentStatus.cancelled,
        }
        return status.get(response.get("status"))
