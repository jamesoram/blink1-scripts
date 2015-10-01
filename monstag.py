import urllib2
import time

class Monitor:

  def __init__(self):
    self.url = "http://chhlapphot006.karmalab.net:7405/header_svc/version.txt"
    self.expected = "release.tag"
    self.colour = "12AA3F"
    self.blink_time = "700"

  def check(self):
    response = urllib2.urlopen(self.url).read()
    return self.expected in response

class Blinker:

  def __init__(self):
    q = Queue.LifoQueue()
    command = "blink1-tool --rgb "

  def add(monitor):
    q.put(monitor)
    command.run(q.get().colour + " -t " + q.get().blink_time)
    
class Poller:

  def __init__(self):
    self.poll_time = 90

  def poll(self):
    for monitor in monitors:
      if not monitor.check
        blinker.add(monitor)
    time.sleep(poll_time)

