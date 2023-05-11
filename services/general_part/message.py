from WebAutomation.general_utils import *
from datetime import datetime
from diplom_work.services.general.profile import Profile
from diplom_work.services.general.attachment import Attachment
from diplom_work.services.general.chapter import Chapter

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