from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget  # noqa: E501


class TimerView(QWidget):
    """
    Widget allowing input of a time interval and
    counts down the time interval
    """

    def __init__(self, time_preset, time_changed_handler, completion_handler):
        """
        Parameters:
        time_preset: the preset time to be displayed
        time_changed_handler: method called when time interval
            is changed
        completion_handler: method called when count down completes
        """
        super().__init__()
        self.TIME_PRESET = time_preset
        self.time_changed_handler = time_changed_handler
        self.completion_handler = completion_handler

        self.current_time = 0
        self.TIMER = QTimer(self, interval=1000, timeout=self.reload_timer)
        self.TIMER.setTimerType(Qt.PreciseTimer)

        self.running = False

        # set up the timer boxes
        timer_boxes = QHBoxLayout()

        secs_letter = QLabel("s")
        self.secs_box2 = QLineEdit()
        self.secs_box2.textChanged.connect(
            # change focus to the next box upon text input
            lambda: self._process_input(self.secs_box2, None)
        )
        self.secs_box1 = QLineEdit()
        self.secs_box1.textChanged.connect(
            # change focus to the next box upon text input
            lambda: self._process_input(self.secs_box1, self.secs_box2)
        )

        mins_letter = QLabel("m")
        self.mins_box2 = QLineEdit()
        self.mins_box2.textChanged.connect(
            # change focus to the next box upon text input
            lambda: self._process_input(self.mins_box2, self.secs_box1)
        )
        self.mins_box1 = QLineEdit()
        self.mins_box1.textChanged.connect(
            # change focus to the next box upon text input
            lambda: self._process_input(self.mins_box1, self.mins_box2)
        )

        hour_letter = QLabel("h")
        self.hour_box = QLineEdit()
        self.hour_box.textChanged.connect(
            # change focus to the next box upon text input
            lambda: self._process_input(self.hour_box, self.mins_box1)
        )

        # set timer time to preset time
        self.set_time(self.TIME_PRESET)

        # configure all letters and input boxes
        self.widget_list = [
            self.hour_box,
            hour_letter,
            self.mins_box1,
            self.mins_box2,
            mins_letter,
            self.secs_box1,
            self.secs_box2,
            secs_letter,
        ]

        for item in self.widget_list:
            if isinstance(item, QLineEdit):
                item.setObjectName("timertext")
                item.setMaxLength(1)
                item.setMaximumWidth(30)
                item.setMinimumHeight(30)
                # commit the time change when user press enter
                # TODO: allow time change when user
                # focus out of the current widget
                item.returnPressed.connect(self._on_time_changed)
            if isinstance(item, QLabel):
                item.setObjectName("timerlabel")
            timer_boxes.addWidget(item)

        self.setLayout(timer_boxes)

    def set_time(self, time):
        """
        Set the timer input box based on a time interval in seconds
        """
        split_time = self._split_seconds(time)
        self.hour_box.setText(self._replace_empty_with_zero(split_time["hour"]))
        self.mins_box1.setText(self._replace_empty_with_zero(split_time["mins1"]))
        self.mins_box2.setText(self._replace_empty_with_zero(split_time["mins2"]))
        self.secs_box1.setText(self._replace_empty_with_zero(split_time["secs1"]))
        self.secs_box2.setText(self._replace_empty_with_zero(split_time["secs2"]))

    def _gather_seconds(self):
        """
        Convert the time in timer input boxes to single
        time interval number in seconds
        """
        hour_to_seconds = float(self._replace_empty_with_zero(self.hour_box.text()))
        mins_to_seconds = float(
            self._replace_empty_with_zero(self.mins_box1.text())
        ) * 10 + float(self._replace_empty_with_zero(self.mins_box2.text()))
        seconds = float(
            self._replace_empty_with_zero(self.secs_box1.text())
        ) * 10 + float(self._replace_empty_with_zero(self.secs_box2.text()))
        total = (hour_to_seconds * 60 * 60) + (mins_to_seconds * 60) + seconds
        return total

    def _split_seconds(self, input):
        """
        Split the input time interval in seconds into
        hour, minute, seconds for each timer input box
        """
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

    def _replace_empty_with_zero(self, item):
        """
        Replaces empty text with 0
        """
        if item == "":
            return "0"
        else:
            return item

    def _process_input(self, cur_widget, next_widget):
        """
        Method called when the timer input box is changed

        Parameters:
        cur_widget: the current input box with changed text
        next_widget: the next input box to shift focus to
        """
        text = cur_widget.text()

        # if input text if not numeric, clear the
        # input from input box
        if text != "" and not text.isnumeric():
            cur_widget.setText("")
            return

        # if the current input box is the first
        # minutes box or first seconds box, make
        # sure the input is less than 6, otherwise
        # clear the input from input box
        if cur_widget == self.secs_box1 or cur_widget == self.mins_box1:
            if text != "" and int(text) >= 6:
                cur_widget.setText("")
                return

        # if the input text is not deleted and
        # a next focused input box is supplied,
        # focus on the next input box
        if text is not None and text != "":
            if next_widget is not None:
                next_widget.setFocus()

    def _on_time_changed(self):
        """
        Method called when time change is commited
        """
        if not self.running:
            # get the total time interval in seconds
            # and reset time preset
            seconds_total = self._gather_seconds()
            self.TIME_PRESET = seconds_total
            self.time_changed_handler(seconds_total)

        # fill all empty timer input boxes with 0
        # and clear focus of all timer input boxes
        for item in self.widget_list:
            if isinstance(item, QLineEdit):
                text = item.text()
                if text == "":
                    item.setText("0")
                item.clearFocus()

    def start(self):
        """
        Start count down of the timer
        """
        if self.running:
            return

        self.running = True
        self.current_time = self._gather_seconds()

        # disable all timer input boxes
        for widget in self.widget_list:
            if isinstance(widget, QLineEdit):
                widget.setEnabled(False)

        # start the timer
        self.TIMER.start()

    def reload_timer(self):
        """
        Method called every second once timer starts
        """
        self.current_time -= 1

        # if the current count down interval is
        # completed, stop the timer and call
        # completion handler
        if self.current_time == 0:
            self.running = False
            self.TIMER.stop()
            self.completion_handler()
            return

        # set the time according to the remainig
        # time in seconds
        self.set_time(self.current_time)
        self.TIMER.start()

    def reset(self):
        """
        Reset the timer widget
        """
        self.running = False
        # reset time according to time preset
        self.set_time(self.TIME_PRESET)

        # enable all timer input boxes
        for widget in self.widget_list:
            if isinstance(widget, QLineEdit):
                widget.setEnabled(True)
