from threading import Timer

class RepeatTimer(Timer):
    """
    Timer repeats function call every self.interval
    amount of time.

    Implementation taken from:
    https://stackoverflow.com/questions/12435211/
    threading-timer-repeat-function-every-n-seconds
    """

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def format_website(website_url):
    """
    Takes out the "www." in front of web URL,
    if there exists any
    """
    if website_url[:4] == "www.":
        return website_url[4:]

    return website_url
