from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget  # noqa: E501
from lento.common import cards_management as CardsManagement
from lento.common import get_block_controller


class TimerView(QWidget):
    def __init__(
        self,
        current_card,
        time_preset,
        activated_card,
        refresh_handler
    ):
        super().__init__()
        self.CURRENT_CARD = current_card
        self.TIME_PRESET = time_preset
        self.refresh = refresh_handler

        self.current_time = time_preset
        self.TIMER = QTimer(self, interval=1000, timeout=self.reload_timer)

        self.BLOCK_IS_RUNNING = activated_card is not None
        if self.BLOCK_IS_RUNNING:
            block_controller = get_block_controller()
            self.current_time = block_controller.get_remaining_block_time(
                self.TIME_PRESET
            )
            self.TIMER.start()

        main_layout = QVBoxLayout()
        timer_boxes = QHBoxLayout()
        nums = self.split_seconds(self.TIME_PRESET)

        secs_letter = QLabel("s")
        self.secs_box2 = QLineEdit(
            self.replace_empty_with_zero(nums["secs2"])
        )
        self.secs_box1 = QLineEdit(
            self.replace_empty_with_zero(nums["secs1"])
        )
        self.secs_box1.textChanged.connect(self.secs_box2.setFocus)

        mins_letter = QLabel("m")
        self.mins_box2 = QLineEdit(
            self.replace_empty_with_zero(nums["mins2"])
        )
        self.mins_box2.textChanged.connect(self.secs_box1.setFocus)
        self.mins_box1 = QLineEdit(
            self.replace_empty_with_zero(nums["mins1"])
        )
        self.mins_box1.textChanged.connect(self.mins_box2.setFocus)

        hour_letter = QLabel("h")
        self.hour_box = QLineEdit(
            self.replace_empty_with_zero(nums["hour"])
        )
        self.hour_box.textChanged.connect(self.mins_box1.setFocus)

        for item in [
            self.hour_box, hour_letter, self.mins_box1, self.mins_box2,
            mins_letter, self.secs_box1, self.secs_box2, secs_letter
        ]:
            if isinstance(item, QLineEdit):
                item.setObjectName("timertext")
                item.setMaxLength(1)
                item.setMaximumWidth(30)
                item.setMinimumHeight(30)
                item.returnPressed.connect(self.update_timer_data)
                if self.BLOCK_IS_RUNNING:
                    item.setEnabled(False)
            if isinstance(item, QLabel):
                item.setObjectName("timerlabel")
            timer_boxes.addWidget(item)

        self.start_button = QPushButton("Start Block")
        self.start_button.clicked.connect(self.start_block)
        self.start_button.setObjectName("startbutton")

        main_layout.addLayout(timer_boxes)
        main_layout.addWidget(self.start_button)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("timerbox")
        self.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

    def replace_empty_with_zero(self, item):
        if item == "":
            return "0"
        else:
            return item

    def gather_seconds(self):
        hour_to_seconds = float(
            self.replace_empty_with_zero(self.hour_box.text())
        )
        mins_to_seconds = (
            float(
                self.replace_empty_with_zero(self.mins_box1.text())
            ) * 10 + float(
                self.replace_empty_with_zero(self.mins_box2.text())
            )
        )
        seconds = (
            float(
                self.replace_empty_with_zero(self.secs_box1.text())
            ) * 10 + float(
                self.replace_empty_with_zero(self.secs_box2.text())
            )
        )
        total = (hour_to_seconds * 60 * 60) + (mins_to_seconds * 60) + seconds
        return total

    def split_seconds(self, input):
        hours = str(int(input // 3600))
        minutes = str(int((input % 3600) // 60)).zfill(2)
        seconds = str(int(input % 60)).zfill(2)
        total = {
            "hour": hours,
            "mins1": minutes[0],
            "mins2": minutes[1],
            "secs1": seconds[0],
            "secs2": seconds[1],
        }
        return total

    def update_timer_data(self):
        if self.BLOCK_IS_RUNNING:
            return
        total = self.gather_seconds()
        CardsManagement.update_metadata(
            self.CURRENT_CARD,
            "time",
            total
        )
        self.refresh()

    def start_block(self):
        if self.BLOCK_IS_RUNNING:
            return
        total = self.gather_seconds()
        print(f"START BLOCK WITH CARD {self.CURRENT_CARD} AND TOTAL {total}")
        block_controller = get_block_controller()
        block_controller.start_block(self.CURRENT_CARD, int(total))
        self.BLOCK_IS_RUNNING = True
        self.start_button.setEnabled(False)
        self.start_button.setObjectName("disabled_startbutton")
        self.start_button.setText("Session is running!")
        self.TIMER.start()

    def reload_timer(self):
        self.current_time -= 1
        if self.current_time == 0:
            block_controller = get_block_controller()
            block_controller.end_block()
            return self.refresh()
        split_time = self.split_seconds(self.current_time)
        self.hour_box.setText(split_time["hour"])
        self.mins_box1.setText(split_time["mins1"])
        self.mins_box2.setText(split_time["mins2"])
        self.secs_box1.setText(split_time["secs1"])
        self.secs_box2.setText(split_time["secs2"])
        for item in [
            self.hour_box, self.mins_box1, self.mins_box2,
            self.secs_box1, self.secs_box2
        ]:
            item.setEnabled(False)
        self.TIMER.start()
