from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout  # noqa: E501


class Card():
    def __init__(self):
        super().__init__()

    def render_card(self):
        body = QWidget()
        body_layout = QVBoxLayout()
        body_rect = QWidget()

        body_rect.setObjectName("bob")
        body_text = QLabel("hi mom")
        body_layout.addWidget(body_text)
        body_layout.addWidget(body_rect)
        body.setLayout(body_layout)
        return body
