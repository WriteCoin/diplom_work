from WebAutomation.general_utils import *
from diplom_work.services.general import ConnectData, Message, Messenger, Profile
from respect_validation import Validator as v

class VkConnectData(ConnectData):
    def __init__(self, email: Optional[str], phone: Optional[str], password: Optional[str]) -> None:
        super().__init__(email, phone, password)

    client_id = property()
    
    @client_id.getter
    def client_id(self):
        return self._app_id
    
    @client_id.setter
    def client_id(self, value):
        self._app_id = value

    client_secret = property()
    
    @client_secret.getter
    def client_secret(self):
        return self._client_secret
    
    @client_secret.setter
    def client_secret(self, value):
        self._client_secret = value


class Vkontakte(Messenger):
    TConnectData = VkConnectData
    TProfile = ForwardRef('VkProfile')

    title = "ВКонтакте"
    url = "https://vk.com/"
    # адрес сервера для обработки ответа
    redirect_url = "https://localhost:3000"

    def connect(data: TConnectData) -> TProfile:
        pass

    def update() -> None:
        pass

class VkProfile(Profile):
    pass

class VkMessage(Message):
    pass