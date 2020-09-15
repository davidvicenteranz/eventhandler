from unittest import TestCase
from eventhandler import EventHandler

class TestEventHandler(TestCase):
    def setUp(self):
        self.emgr = EventHandler('on_event1', 'on_event2', 'on_event3')

    def test_bad_initialization(self):
        with self.assertRaises(EventHandler.Exceptions.InitializationError) as context:
            manager = EventHandler()

    def test_set_allowed_callbacks(self):
        self.assertEqual(self.emgr.allowed_callbacks, tuple(['on_event1', 'on_event2', 'on_event3']))

    def test_is_callable(self):
        not_callable_var = 'Not callable'
        callable_var = lambda : print("I'm callable")
        self.assertFalse(self.emgr.is_callable(not_callable_var))
        self.assertTrue(self.emgr.is_callable(callable_var))

    def test_bind_callback(self):
        callable = lambda : print(None)

        # Bind allowed callback
        self.assertTrue(self.emgr.bind('on_event1', callable))
        self.assertEqual(self.emgr.Callbacks.ON_EVENT1[0], callable)

        # Bind unallowed callback
        with self.assertRaises(EventHandler.Exceptions.EventNotAllowedError) as context:
            self.emgr.bind('on_not_extist_event', callable)

        # Bind existing callback
        self.assertFalse(self.emgr.bind('on_event1', callable))

    def test_unbind_callback(self):
        callable = lambda : print(None)
        self.assertTrue(self.emgr.bind('on_event1', callable))
        self.assertEqual(len(self.emgr.Callbacks.ON_EVENT1), 1)
        self.assertTrue(self.emgr.unbind('on_event1', callable))
        self.assertEqual(len(self.emgr.Callbacks.ON_EVENT1), 0)
        self.assertFalse(self.emgr.unbind('on_event1', lambda: print('another function not in callback list')))

    def test_fire(self):
        def on_fired_callback(*args, **kargs):
            self.assertEqual(args[0], 1)
            self.assertEqual(args[1], 2)
            self.assertEqual(args[2], 3)
            self.assertEqual(args[3], 4)
            self.assertEqual(kargs['extra'], 5)

        self.emgr.bind('on_event1', on_fired_callback)
        self.emgr.fire('on_event1', 1, 2, 3, 4, extra=5)