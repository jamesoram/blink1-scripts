import urllib2
import time
import Queue

class Monitor(object):

    def __init__(self):
        self.url = "http://chhlapphot006.karmalab.net:7405/header_svc/version.txt"
        self.expected = "release.tag"
        self.colour = "12AA3F"
        self.blink_time = "700"

    def check(self):
        response = urllib2.urlopen(self.url).read()
        return self.expected in response

class Blinker(object):

    def __init__(self):
        self.queue = Queue.LifoQueue()
        self.command = "blink1-tool --rgb "

    def add(self, monitor):
        self.queue.put(monitor)
        self.command.run(self.queue.get().colour + " -t " + self.queue.get().blink_time)

class Poller(object):

    def __init__(self):
        self.poll_time = 90
        self.monitors = []
        self.monitors.append(Monitor())
        self.blinker = Blinker()

    def poll(self):
        for monitor in self.monitors:
            if not monitor.check():
                self.blinker.add(monitor)
        time.sleep(self.poll_time)

poller = Poller()
poller.poll()
