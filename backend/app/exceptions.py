

class AppException(Exception):
    """Base class for all exceptions in the application."""
    status_code: int
    error_code: str
    message: str

    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(message)   

class ProductNotFoundException(AppException):
    def __init__(self):
        super().__init__(404,"PRODUCT_NOT_FOUND","The requested product was not found.")


class ProductAlreadySoldException(AppException):
    def __init__(self):
        super().__init__(409,"PRODUCT_ALREADY_SOLD","The product has already been sold.")

class ResellerPriceTooLowException(AppException):
    def __init__(self):
        super().__init__(400,"RESELLER_PRICE_TOO_LOW","The price set by the reseller is below the minimum sell price.")


class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(401,"UNAUTHORIZED","You are not authorized to perform this action.")   