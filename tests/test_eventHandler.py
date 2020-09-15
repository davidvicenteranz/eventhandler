from unittest import TestCase
from eventhandler import EventHandler

class TestEventHandler(TestCase):

    def test_is_callable(self):
        evntmgr = EventHandler('on_event1', 'on_event2', 'on_event3')
        not_callable_var = 'Not callable'
        callable_var = lambda : print("I'm callable")
        self.assertFalse(evntmgr.is_callable(not_callable_var))
        self.assertTrue(evntmgr.is_callable(callable_var))

    def test_bind_callback(self):
        evntmgr = EventHandler('on_event1', 'on_event2', 'on_event3')
        callable = lambda : print(None)

        # Bind allowed callback
        self.assertTrue(evntmgr.bind('on_event1', callable))
        self.assertEqual(evntmgr.events['on_event1'][0], callable)

        # Bind unallowed callback
        with self.assertRaises(EventHandler.Exceptions.EventNotAllowedError) as context:
            evntmgr.bind('on_not_extist_event', callable)

        # Bind existing callback
        self.assertFalse(evntmgr.bind('on_event1', callable))

        # Try to bind a not callable variable
        self.assertFalse(evntmgr.bind('on_event2', 'impossible text var'))

    def test_unbind_callback(self):
        evntmgr = EventHandler('on_event1')
        callable = lambda : print(None)
        self.assertTrue(evntmgr.bind('on_event1', callable))
        self.assertEqual(len(evntmgr.events['on_event1']), 1)
        self.assertTrue(evntmgr.unbind('on_event1', callable))
        self.assertEqual(len(evntmgr.events['on_event1']), 0)
        self.assertFalse(evntmgr.unbind('on_event1', lambda: print('another function not in callback list')))

    def test_fire(self):
        evntmgr = EventHandler('on_event1')
        def on_fired_callback(*args, extra=None):
            self.assertEqual(args[0], 1)
            self.assertEqual(args[1], 2)
            self.assertEqual(args[2], 3)
            self.assertEqual(args[3], 4)
            self.assertEqual(extra, 5)

        evntmgr.bind('on_event1', on_fired_callback)

        evntmgr.fire('on_event1', 1, 2, 3, 4, extra=5)