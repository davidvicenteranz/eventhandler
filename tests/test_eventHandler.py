from unittest import TestCase
from eventhandler import EventHandler

class TestEventHandler(TestCase):

    def test_is_callable(self):
        eventHandler = EventHandler()
        not_callable_var = 'Not callable'
        callable_var = lambda : print("I'm callable")
        self.assertFalse(eventHandler.is_callable(not_callable_var))
        self.assertTrue(eventHandler.is_callable(callable_var))

    def test_bind_callback(self):
        evntmgr = EventHandler('on_event1')
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

