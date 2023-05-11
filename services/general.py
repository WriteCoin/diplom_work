from respect_validation import Validator as v
from WebAutomation.general_utils import *
from datetime import datetime

class AppOptions(ABC):
    ms_update: Final[int]

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

class WebService(ABC):
    title: Final[str]
    url: Final[str]

    TProfile = ForwardRef('Profile')
    TOptions = AppOptions
    TConnectData = ConnectData

    def __init__(
        self,
        profiles: list[TProfile],
        app_options: TOptions,
    ):
        self.profiles = profiles
        self.app_options = app_options

    @abstractmethod
    def connect(data: TConnectData) -> TProfile:
        pass

    @abstractmethod
    def update() -> None:
        pass

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

    app_options = property()

    @app_options.getter
    def app_options(self):
        return self._app_options

    @app_options.setter
    def app_options(self, value):
        self._app_options = value

class ProfileData(ABC):
    def __init__(self, avatar: Optional[str]) -> None:
        if not avatar is None:
            self.avatar = avatar

    avatar = property()

    @avatar.getter
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        self._avatar = value

class Profile(ABC):
    TConnectData = ConnectData
    TWebService = WebService
    TMessage = ForwardRef('Message')
    TProfileData = ProfileData

    def __init__(
        self,
        connect_data: TConnectData,
        web_service: TWebService,
        messages: list[TMessage],
        profile_data: TProfileData,
    ) -> None:
        self.connect_data = connect_data
        self.web_service = web_service
        self.messages = messages
        self.profile_data = profile_data

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

    messages = property()

    @messages.getter
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    profile_data = property()

    @profile_data.getter
    def profile_data(self):
        return self._profile_data

    @profile_data.setter
    def profile_data(self, value):
        self._profile_data = value

class Attachment(ABC):
    pass

class Chapter(ABC):
    TChapter = ForwardRef('Chapter')

    def __init__(
        self,
        title: str,
        childs: list[TChapter],
        parent: Optional[TChapter],
    ) -> None:
        self.title = title
        self.childs = childs
        if not parent is None:
            self.parent = parent

    title = property()

    @title.getter
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    childs = property()

    @childs.getter
    def childs(self):
        return self._childs

    @childs.setter
    def childs(self, value):
        self._childs = value

    parent = property()

    @parent.getter
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

class Message(ABC):
    TProfile = Profile
    TAttachment = Attachment
    TChapter = Chapter

    def __init__(
        self,
        from_: TProfile,
        to: Union[TProfile, list[TProfile]],
        id: Optional[int],
        attachments: list[TAttachment],
        date_time: datetime,
        text: str,
        statuses: dict[TProfile, str],
        chapter: TChapter,
    ) -> None:
        self.from_ = from_
        self.to = to
        if not id is None:
            self.id = id
        self.attachments = attachments
        self.date_time = date_time
        self.text = text
        self.statuses = statuses
        self.chapter = chapter

    from_ = property()

    @from_.getter
    def from_(self):
        return self._from_

    @from_.setter
    def from_(self, value):
        self._from_ = value

    to = property()

    @to.getter
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        self._to = value

    id = property()

    @id.getter
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    attachments = property()

    @attachments.getter
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments = value

    date_time = property()

    @date_time.getter
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        self._date_time = value

    text = property()

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    statuses = property()

    @statuses.getter
    def statuses(self):
        return self._statuses

    @statuses.setter
    def statuses(self, value):
        self._statuses = value

    chapter = property()

    @chapter.getter
    def chapter(self):
        return self._chapter

    @chapter.setter
    def chapter(self, value):
        self._chapter = value

class Messenger(WebService):
    pass

class MailClient(WebService):
    pass

if "-t" in sys.argv and __name__ == "__main__":
    # Тестовый режим запуска
    pass
elif __name__ == "__main__":
    # Релизный режим запуска
    pass
