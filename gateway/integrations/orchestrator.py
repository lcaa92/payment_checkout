from typing import Dict
from integrations.interfaces import ProviderIntegrationBase
from .provider1 import Provider1Integration

class PaymentProcessException(Exception):
    """Custom exception for payment processing errors."""

    def __init__(self, errors: list, message: str):
        super().__init__(message)
        self.errors = errors

class PaymentOrchestrator:

    _PROVIDERS_ORDER: Dict[str, ProviderIntegrationBase] = {
        "provider1": Provider1Integration,
    }

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
                return {
                    "provider_name": provider_name,
                    "provider_details": provider.process_payment(payment_data)
                }
            except Exception as e:
                # Log the error or handle it as needed
                errors.append({
                    "provider": provider_name,
                    "error": str(e)
                })
                print(f"Error processing payment with {provider_name}: {e}")

        raise PaymentProcessException(errors, "All payment providers failed to process the payment.")
