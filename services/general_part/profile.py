from WebAutomation.general_utils import *
from diplom_work.services.general.connect_data import ConnectData
from diplom_work.services.general.web_service import WebService

class Profile(ABC):
    TConnectData = ConnectData
    TWebService = WebService

    def __init__(
        self,
        connect_data: TConnectData,
        web_service: TWebService,
        avatar: str
    ) -> None:
        self.connect_data = connect_data
        self.web_service = web_service
        self.avatar = avatar

    connect_data = property()

    @connect_data.getter
    def connect_data(self):
        return self._connect_data

    @connect_data.setter
    def connect_data(self, value):
        self._connect_data = value

    web_service = property()
    
    @web_service.getter
    def web_service(self):
        return self._web_service
    
    @web_service.setter
    def web_service(self, value):
        self._web_service = value

    avatar = property()
    
    @avatar.getter
    def avatar(self):
        return self._avatar
    
    @avatar.setter
    def avatar(self, value):
        self._avatar = value