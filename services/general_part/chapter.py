from WebAutomation.general_utils import *

class Chapter(ABC):
    TChapter = Chapter

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
