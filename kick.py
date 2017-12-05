from threading import Thread

class kicker(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        print("Starting kicker thread")

    # Thread entry point
    def run(self):

        # Run until shutdown flag is set
        while self.parent.running:
            pass