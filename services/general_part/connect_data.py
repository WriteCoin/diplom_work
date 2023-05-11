from WebAutomation.general_utils import *
from respect_validation import Validator as v


class ConnectData(ABC):
    def __init__(self, email: Optional[str], phone: Optional[str], password: Optional[str]) -> None:
        if not email is None:
            self.email = email
        if not phone is None:
            self.phone = phone
        if not password is None:
            self.password = password

    email = property()

    @email.getter
    def email(self):
        return self._email

    def validate_email(self) -> bool:
        return v.email().validate(self.email)

    @email.setter
    def email(self, value):
        if not self.validate_email():
            raise ValueError("Некорректный Email")
        self._email = value

    phone = property()

    @phone.getter
    def phone(self):
        return self._phone

    def validate_phone(self) -> bool:
        return v.phone().validate(self.phone)

    @phone.setter
    def phone(self, value):
        if not self.validate_phone():
            raise ValueError("Некорректный номер телефона")
        self._phone = value

    password = property()

    @password.getter
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value