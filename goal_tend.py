from threading import Thread
import cozmo

class keeper(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        print("Starting keeper thread")

    # Thread entry point
    def run(self):

        # Run until shutdown flag is set
        while self.parent.running:

            # Wait for a tap event from a cube
            if not self.parent.message_queue.empty():
                event = self.parent.message_queue.get()
                print("Received block tap event")