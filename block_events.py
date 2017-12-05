from threading import Thread
import cozmo

class poll_events(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.tap_count = 0
        print("Starting notification thread")

    # Thread entry point
    def run(self):

        # Run until shutdown flag is set
        while (self.parent.running):

            # If you want to wait for any cube to be tapped, you could
            # call the :meth:`~cozmo.event.Dispatcher.wait_for` method on the
            # :class:`World` object instead.  Eg::
            #     robot.world.wait_for(cozmo.objects.EvtObjectTapped)
            # In either case, ``wait_for`` will return the instance of the event's
            # :class:`~cozmo.objects.EvtObjectTapped` class, which includes a
            # :attr:`~cozmo.objects.EvtObjectTapped.obj` attribute, which identifies
            # exactly which cube has been tapped.
            event = self.parent.robot.world.wait_for(cozmo.objects.EvtObjectTapped)
            print("Detected cube tab, count={}".format(self.tap_count))
            self.parent.message_queue.put(event)

            # Incriment the tap counter
            self.tap_count += 1

            # Stop after the 3rd tap
            if (self.tap_count >= 3):
                self.parent.running = False