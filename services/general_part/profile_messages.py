from WebAutomation.general_utils import *
from diplom_work.services.general.profile import Profile
from diplom_work.services.general.message import Message

class ProfileMessages(ABC):
    TProfile = Profile
    TMessage = Message

    def __init__(self, profile: Profile, messages: list[Message]) -> None:
        self.profile = profile
        self.messages = messages

    profile = property()
    
    @profile.getter
    def profile(self):
        return self._profile
    
    @profile.setter
    def profile(self, value):
        self._profile = value

    messages = property()
    
    @messages.getter
    def messages(self):
        return self._messages
    
    @messages.setter
    def messages(self, value):
        self._messages = value
