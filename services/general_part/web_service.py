from WebAutomation.general_utils import *
from diplom_work.services.general.profile import Profile
from diplom_work.services.general.web_service_options import WebServiceOptions
from diplom_work.services.general.connect_data import ConnectData

class WebService(ABC):
    TOptions = WebServiceOptions

    title: Final[str]
    url: Final[str]
    options: Final[TOptions]