from typing import Dict
from core.log import logger
from models.payments import Payments
from integrations.interfaces import ProviderIntegrationBase
from .provider1 import Provider1Integration
from .provider2 import Provider2Integration


class PaymentProcessException(Exception):
    """Custom exception for payment processing errors."""

    def __init__(self, errors: list, message: str):
        super().__init__(message)
        self.errors = errors


class PaymentOrchestrator:

    _PROVIDERS_ORDER: Dict[str, ProviderIntegrationBase] = {}

    def __init__(self, providers: Dict[str, ProviderIntegrationBase] = {
            'provider1': Provider1Integration,
            'provider2': Provider2Integration
        }
    ):
        self._PROVIDERS_ORDER = providers

    def process_payment(self, payment_data: dict) -> dict:
        """
        Process a payment with the given data.

        :param payment_data: Dictionary containing payment details.
        :return: Dictionary with the result of the payment processing.
        """
        errors = []
        for provider_name, provider_class in self._PROVIDERS_ORDER.items():
            provider: ProviderIntegrationBase = provider_class()
            try:
                data = provider.process_payment(payment_data)
                return {
                    "provider_name": provider_name,
                    "status": provider.get_status_from_response(data),
                    "provider_details": data
                }
            except Exception as e:
                errors.append({
                    "provider": provider_name,
                    "error": str(e)
                })
                logger.error(f"Error processing payment with {provider_name}: {e}", extra={
                    "provider": provider,
                    "error": str(e)
                })

        raise PaymentProcessException(errors, "All payment providers failed to process the payment.")

    def get_payment_details(self, payment: Payments) -> dict:
        """
        Retrieve payment details from the orchestrator.

        :param payment: Payment object containing the payment details.
        :return: Dictionary with the payment details.
        """
        provider_name = payment.provider
        if provider_name not in self._PROVIDERS_ORDER:
            raise ValueError(f"Unknown provider: {provider_name}")

        provider_class = self._PROVIDERS_ORDER[provider_name]
        provider: ProviderIntegrationBase = provider_class()
        return provider.get_payment_details(payment.model_dump())
