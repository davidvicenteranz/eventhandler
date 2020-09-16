import os
import io
import sys
from unittest import TestCase, main as unittest_main
from eventhandler import EventHandler



class TestEventHandler(TestCase):


    def test_001_initialization_args(self):
        # Test init on no args
        eh = EventHandler()
        self.assertEqual(eh.count_events, 0)        # checks there is no events
        self.assertFalse(eh.verbose)                # checks verbose is false
        self.assertFalse(eh.tolerate_exceptions)    # checks no exception toleration
        self.assertIsNotNone(eh.stream_output)


    def test_002_initiaization_with_events(self):
        # Test init with args.
        eh = EventHandler('MyEvent')
        self.assertEqual(eh.count_events, 1)
        self.assertFalse(eh.verbose)  # checks verbose is false
        self.assertFalse(eh.tolerate_exceptions)  # checks no exception toleration
        self.assertIsNotNone(eh.stream_output)


    def test_003_initialization_verbose(self):
        eh = EventHandler(verbose=True)
        self.assertTrue(eh.verbose)

        eh = EventHandler(verbose=False)
        self.assertFalse(eh.verbose)

    def test_004_initialization_tolerate_execeptions(self):
        eh = EventHandler(tolerate_callbacks_exceptions=True)
        self.assertTrue(eh.tolerate_exceptions)

        eh = EventHandler(tolerate_callbacks_exceptions=False)
        self.assertFalse(eh.tolerate_exceptions)

    def test_005_initialization_file_to_verbose(self):
        with open('test.txt', '+w') as f:
            eh = EventHandler(stream_output=f, verbose=True)
            self.assertEqual('test.txt', eh.stream_output.name)

            instance_id = str(hex(id(eh)))
            f.close()
        with open('test.txt', 'r') as f:
            content = f.read()
            self.assertTrue((instance_id in content))

            f.close()
        os.remove('test.txt')


    def test_006_event_registration(self):
        eh = EventHandler()
        event_name = 'onMyCoolEventHappens'
        self.assertFalse(eh.is_event_registered(event_name))
        self.assertTrue(eh.register_event(event_name))
        self.assertTrue(eh.is_event_registered(event_name))


        eh = EventHandler('one', 'two', 'three', verbose=True)
        self.assertTrue(eh.is_event_registered('three'))
        self.assertFalse(eh.register_event('one'))

    def test_007_event_unregistration(self):
        eh = EventHandler()
        event_name = 'onMyCoolEventHappens'
        self.assertFalse(eh.is_event_registered(event_name))
        self.assertTrue(eh.register_event(event_name))
        self.assertTrue(eh.is_event_registered(event_name))
        eh.unregister_event(event_name)
        self.assertFalse(eh.unregister_event('one'))

    def test_008_is_callable(self):
        func = lambda x: print(x)
        not_func = 'This is not callable as method'

        self.assertTrue(EventHandler.is_callable(func))
        self.assertFalse(EventHandler.is_callable(not_func))

    def test_008_bind_callbacks(self):
        event_name= 'newCoolEvent'
        eh = EventHandler(event_name)
        def callback1(*args):
            pass

        self.assertFalse(eh.is_callback_in_event(event_name, callback1))

        output = io.StringIO()
        eh = EventHandler(event_name, verbose=True, stream_output=output)

        with self.assertRaises(EventHandler.Exceptions.EventNotAllowedError) as context:
            # Impossible to bind to a not registered callback, will raie error
            eh.bind('onNotRegisteredEvent', callback1)

        self.assertTrue(eh.bind(event_name, callback1))
        self.assertFalse(eh.bind(event_name, callback1))

        output = str(output.getvalue())

        self.assertTrue(callback1.__name__ in output)
        self.assertTrue(event_name in output)

        self.assertTrue(eh.is_callback_in_event(event_name, callback1))

    def test_009_unbind_callbacks(self):
        event_name= 'newCoolEvent'
        eh = EventHandler(event_name)

        def callback1(*args):
            pass

        self.assertTrue(eh.bind(event_name, callback1))
        self.assertTrue(eh.unbind(event_name, callback1))

        # Test already unregistered event
        output = io.StringIO()
        eh = EventHandler(event_name, verbose=True, stream_output=output)
        self.assertFalse(eh.unbind(event_name, callback1))

        self.assertTrue(eh.bind(event_name, callback1))
        self.assertFalse(eh.bind(event_name, callback1))

        value = output.getvalue()

        self.assertTrue(callback1.__name__ in value)
        self.assertTrue(event_name in value)

        # Test try unregister not exists event
        self.assertFalse(eh.unbind('inexistentEventName', callback1))

        value = output.getvalue()
        print(output)

        for event in eh.event_list:
            self.assertTrue(event in value)

    def test_010_fire_event(self):
        event_name= 'newCoolEvent'
        eh = EventHandler(event_name)

        def callback1(*args, **kwargs):
            self.assertEqual(args[0], 1)
            self.assertEqual(args[1], 2)
            self.assertEqual(args[2], 3)
            self.assertEqual(kwargs['extra'], 0)

        self.assertTrue(eh.bind(event_name, callback1))

        self.assertTrue(eh.fire(event_name, 1, 2, 3, extra=0))


        def will_fail_callback(number1, number2, number3, extra=0):
            return number1 / extra

        self.assertTrue(eh.bind(event_name, will_fail_callback))

        with self.assertRaises(ZeroDivisionError) as context:
            eh.fire(event_name, 1, 2, 3, extra=0)

        # Set callback fail toleration
        eh.verbose = True
        eh.tolerate_exceptions = True
        output = io.StringIO()
        eh.stream_output = output
        self.assertFalse(eh.fire(event_name, 1, 2, 3, extra=0))
        value = output.getvalue()
        self.assertTrue('WARNING' in value)
        self.assertTrue(will_fail_callback.__name__ in value)

    def test_011_string_representation(self):
        eh = EventHandler('one')

        def check__str__output():
            instance_id = str(hex(id(eh)))
            self.assertTrue(instance_id in eh.__str__())
            self.assertTrue(f'verbose={eh.verbose}' in eh.__str__())
            self.assertTrue(f'tolerate_exceptions={eh.tolerate_exceptions}' in eh.__str__())
            for event in eh.event_list:
                self.assertTrue(event in eh.__str__())
                for callback in eh.event_list:
                    self.assertTrue(callback in eh.__str__())

        def callback1_in_one():
            pass

        def callback2_in_one():
            pass

        def callback3_in_one():
            pass

        def callback1_in_two():
            pass

        def callback2_in_two():
            pass

        def callback1_in_three():
            pass

        self.assertTrue(eh.bind('one', callback1_in_one))
        check__str__output()
        self.assertTrue(eh.bind('one', callback2_in_one))
        check__str__output()
        self.assertTrue(eh.bind('one', callback3_in_one))
        check__str__output()
        self.assertTrue(eh.register_event('two'))
        self.assertTrue(eh.bind('two', callback1_in_two))
        check__str__output()
        self.assertTrue(eh.bind('two', callback2_in_two))
        check__str__output()
        self.assertTrue(eh.register_event('three'))
        self.assertTrue(eh.bind('three', callback1_in_three))
        check__str__output()
        self.assertTrue(eh.unregister_event('three'))
        check__str__output()
        self.assertTrue(eh.unbind('two', callback2_in_two))



