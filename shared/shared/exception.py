class ApplicationException(Exception):
    error_message: str

    def __init__(self, error_message: str):
        self.error_message = error_message
        super().__init__(self.error_message)

    def dict(self):
        return {"error_message": self.error_message}


class LanguageNotAvailableException(ApplicationException):
    def __init__(self):
        super().__init__("Analysis for this language is not supported (yet).")


class LanguageNotIdentifiedException(ApplicationException):
    def __init__(self):
        super().__init__("Language could not be identified.")


class SentenceTooLongException(ApplicationException):
    def __init__(self):
        super().__init__(
            "This sentence is too long for syntactical analysis and literal translation."
        )
