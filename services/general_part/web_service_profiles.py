from WebAutomation.general_utils import *
from diplom_work.services.general.web_service import WebService
from diplom_work.services.general.profile import Profile
from diplom_work.services.general.connect_data import ConnectData


class WebServiceProfiles(ABC):
    TWebService = WebService
    TProfile = Profile
    TConnectData = ConnectData

    def __init__(self, web_service: TWebService, current_profile: TProfile, profiles: list[TProfile]) -> None:
        self.web_service = web_service
        self.current_profile = current_profile
        self.profiles = profiles

    @abstractmethod
    def connect(data: TConnectData) -> TProfile:
        pass

    @abstractmethod
    def update() -> None:
        pass

    web_service = property()
    
    @web_service.getter
    def web_service(self):
        return self._web_service
    
    @web_service.setter
    def web_service(self, value):
        self._web_service = value

    profiles = property()

    @profiles.getter
    def profiles(self):
        return self._profiles

    @profiles.setter
    def profiles(self, value):
        self._profiles = value

    current_profile = property()
    
    @current_profile.getter
    def current_profile(self):
        return self._current_profile
    
    @current_profile.setter
    def current_profile(self, value):
        self._current_profile = value
