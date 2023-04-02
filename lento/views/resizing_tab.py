from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import QSize


class ResizingTabWidget(QTabWidget):
    """
    Tab Widget that can resize according to
    widget size in current tab
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def minimumSizeHint(self):
        return self.sizeHint()

    def sizeHint(self):
        """
        Override sizeHint() method to always
        return the current tab widget size
        """
        current = self.currentWidget()
        width = current.sizeHint().width()
        height = current.sizeHint().height()
        if not current:
            return super().sizeHint()
        # add extra buffer in height
        return QSize(width, height + 25)
