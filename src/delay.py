class NonBlockingDelay:
    def __init__(self, interval_ms):
        self.interval = interval_ms
        self.previous = 0

    def ready(self):
        import time
        now = int(time.time() * 1000)
        if now - self.previous >= self.interval:
            self.previous = now
            return True
        return False

def timestamp():
    import time
    return int(time.time() * 1000)

def sleep_ms(ms):
    import time
    time.sleep(ms / 1000.0)