from dataclasses import dataclass, asdict

USER = "user"
ASSISTANT = "assistant"
SYSTEM = "system"


@dataclass
class Message:
    role: str
    content: str

    def asdict(self) -> dict:
        return asdict(self)
