class UnauthorizedException(Exception):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)
