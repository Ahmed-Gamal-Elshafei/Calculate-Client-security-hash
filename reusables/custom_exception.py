class CustomException(Exception):
    """
    Custom exception to handle business logic errors.

    Attributes:
        message (str): The error message describing the exception.
        details (dict): Additional context or details about the error (optional).
    """

    def __init__(self, message: str, details: dict = None):
        """
        Initialize the CustomException.

        Args:
            message (str): The error message.
            details (dict, optional): Additional context or details about the error.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self):
        """
        String representation of the exception.

        Returns:
            str: The error message along with additional details if available.
        """
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message
