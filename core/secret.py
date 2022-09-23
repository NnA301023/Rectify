import base64  


class Encrypt:

    def __init__(self) -> None:
        ...

    def encode(self, text: str) -> str:
        return base64.b64encode(text.encode()).decode()

    def decode(self, text: str) -> str:
        return base64.b64decode(text).decode()