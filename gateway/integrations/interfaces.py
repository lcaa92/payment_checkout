from abc import ABC, abstractmethod

class ProviderIntegrationBase(ABC):

    @abstractmethod
    def _build_payment_request(self, payment_data: dict) -> dict:
        """
        Build the payment request data structure.
        
        :param payment_data: Dictionary containing payment details.
        :return: Dictionary formatted for the payment provider.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def process_payment(self, payment_data: dict) -> dict:
        """
        Process a payment with the given data.
        
        :param payment_data: Dictionary containing payment details.
        :return: Dictionary with the result of the payment processing.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
