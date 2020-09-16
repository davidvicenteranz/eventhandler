from unittest import TestCase, main as unittest_main
from eventhandler import EventHandler



class TestEventHandler(TestCase):
    evntHdlr = None
    def setUp(self):
        pass

    def test_registered_events(self):
        evntHdlr = EventHandler()
        self.assertEqual(len(evntHdlr.registered_events), 0)
        evntHdlr.register_event('OnMyEvent')
        self.assertEqual(len(evntHdlr.registered_events), 1)

    def test_event_registered(self):
        evntHdlr2 = EventHandler()
        self.assertFalse(evntHdlr2.event_registered('MyEvent'))
        evntHdlr2.register_event('MyEvent')
        self.assertTrue(evntHdlr2.event_registered('MyEvent'))


    def test_register_event(self):
        evntHdlr3 = EventHandler('EventOne', verbose=True)
        self.assertEqual(len(evntHdlr3.registered_events), 1)

        # Try to register existing event
        self.assertFalse(evntHdlr3.register_event('EventOne'))
        self.assertEqual(len(evntHdlr3.registered_events), 1)

        # Add new one
        self.assertTrue(evntHdlr3.register_event('EventTwo'))
        self.assertEqual(len(evntHdlr3.registered_events), 2)

    def test_unregister_event(self):
        pass

    def test_is_callable(self):
        pass

    def test_bind(self):
        pass

    def test_fire(self):
        pass

    def test_unbind(self):
        pass

if __name__ == '__main__':
    unittest_main()