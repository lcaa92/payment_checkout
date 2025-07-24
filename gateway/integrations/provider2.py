import os
import requests
from .interfaces import ProviderIntegrationBase
from fastapi import status
from models.payments import PaymentStatus


class Provider2Integration(ProviderIntegrationBase):

    _BASE_URL = os.getenv("PROVIDER2_URL", "http://localhost:8002")

    def _build_payment_request(self, payment_data: dict) -> dict:
        """
        Build the payment request data structure for Provider 1.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary formatted for Provider 1.
        """

        expiration_date = payment_data["paymentInfo"]["expiration"]
        expiration_date = f"{expiration_date[0:2]}/{expiration_date[5:]}"

        return {
            "amount": payment_data["amount"],
            "currency": payment_data["currency"],
            "statementDescriptor": payment_data.get("description"),
            "paymentType": "card",
            "card": {
                "number": payment_data["paymentInfo"]["number"],
                "holder": payment_data["paymentInfo"]["holderName"],
                "cvv": payment_data["paymentInfo"]["cvv"],
                "expiration": expiration_date,
                "installmentNumber": payment_data["paymentInfo"]["installments"]
            }
        }

    def process_payment(self, payment_data: dict) -> dict:
        """
        Process a payment with the given data.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary with the result of the payment processing.
        """
        payload = self._build_payment_request(payment_data)

        response = requests.post(f"{self._BASE_URL}/transactions", json=payload)

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
            "paid": PaymentStatus.completed,
            "failed": PaymentStatus.failed,
            "voided": PaymentStatus.cancelled,
        }
        return status.get(response.get("status"))

    def _build_get_payment_reload(self, payment_data: dict) -> dict:
        """
        Build the payment request data structure for reloading payment details.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary formatted for Provider 1.
        """
        return {
            "id": payment_data.get("provider_id")
        }

    def get_payment_details(self, payment_data: dict) -> dict:
        """
        Retrieve payment details from Provider 1.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary with the payment details.
        """
        payload = self._build_get_payment_reload(payment_data)
        response = requests.get(f"{self._BASE_URL}/transactions/{payload['id']}")

        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Failed to retrieve payment details: {response.json()}")
        return response.json()
