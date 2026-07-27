from abc import ABC, abstractmethod


class EmailProvider(ABC):

    @abstractmethod
    def send_verification_code_email(
        self,
        code: int,
        email: str,
    ) -> None:
        pass