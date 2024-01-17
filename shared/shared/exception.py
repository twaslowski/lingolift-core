class ApplicationException(Exception):
    error_message: str

    def __init__(self, error_message: str):
        self.error_message = error_message
        super().__init__(self.error_message)

    def dict(self):
        return {"error_message": self.error_message}


class MissingParameterException(ApplicationException):
    def __init__(self, parameter_name: str):
        super().__init__(f"Missing parameter '{parameter_name}'")
