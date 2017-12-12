from threading import Thread
import cozmo

# TODO: Create enumeration for behavior types

class poll_events(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        print("Starting notification thread")

    # Thread entry point
    def run(self):

        # Run until shutdown flag is set
        while (self.parent.behavior < 3):

            # If you want to wait for any cube to be tapped, you could
            # call the :meth:`~cozmo.event.Dispatcher.wait_for` method on the
            # :class:`World` object instead.  Eg::
            #     robot.world.wait_for(cozmo.objects.EvtObjectTapped)
            # In either case, ``wait_for`` will return the instance of the event's
            # :class:`~cozmo.objects.EvtObjectTapped` class, which includes a
            # :attr:`~cozmo.objects.EvtObjectTapped.obj` attribute, which identifies
            # exactly which cube has been tapped.
            event = self.parent.robot.world.wait_for(cozmo.objects.EvtObjectTapped, timeout=0)

            self.parent.behavior += 1
            print("Detected cube tab, executing behavior: {}".format(self.parent.behavior))
