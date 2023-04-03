import PySide6
from PySide6.QtWidgets import QSizePolicy, QStackedWidget


class LentoResizableStackedWidget(QStackedWidget):
    """
    Stack Widget that can resize according to
    currently displayed widget size
    """

    def __init__(self) -> None:
        super().__init__()
        self.currentChanged.connect(self.onCurrentChanged)

    def addWidget(self, w: PySide6.QtWidgets.QWidget) -> int:
        w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        return super().addWidget(w)

    def onCurrentChanged(self, idx):
        current_w = None

        for i in range(self.count()):
            w = self.widget(i)
            policy = QSizePolicy.Ignored
            if i == self.currentIndex():
                policy = QSizePolicy.Expanding
                current_w = w

            w.setSizePolicy(policy, policy)
            w.adjust_height()

        self.setFixedHeight(current_w.height())
