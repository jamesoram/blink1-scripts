import urllib2
import time
import Queue
import os
import threading 

class HttpMonitor(object):

    def __init__(self, name, url, expected, colour):
        self.name = name
        self.url = url
        self.expected = expected
        self.colour = colour

    def check(self):
        try:
            response = urllib2.urlopen(self.url).read()
        except urllib2.URLError:
            return False
        return self.expected in response

class BlinkAlerter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.LifoQueue()
        self.command = "blink1-tool --rgb "
        self.blink_time = "95"

    def add(self, monitor):
        self.queue.put(monitor)
        print "Error in: " + monitor.name
        cmd = self.command + self.queue.get().colour + " -q --blink " + self.blink_time
        os.system(cmd)

class Poller(object):

    def __init__(self, monitors):
        self.poll_time = 90
        self.monitors = monitors
        self.alerter = BlinkAlerter()

    def poll(self):
        while True:
            for monitor in self.monitors:
                if not monitor.check():
                    self.alerter.add(monitor)
            time.sleep(self.poll_time)

MON = []
MON.append(HttpMonitor("hs", "http://chhlapphot006.karmalab.net:7405/header_svc/version.txt", "release.tag", "AA123F"))
MON.append(HttpMonitor("da", "http://uk.staging1-hotels.com/da/version.txt", "release.tag", "FA219E"))
POLLER = Poller(MON)
POLLER.poll()
