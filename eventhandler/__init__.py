import sys
import types

__version__ = '1.1.25'
__author__ = 'David Vicente Ranz'


class EventHandler:
    """Event manager, link, unlink and fire events."""

    class Exceptions:
        """Custom error classes."""

        class EventNotAllowedError(Exception):
            pass

    def __init__(self, *event_names, verbose=False, stream_output=sys.stdout, tolerate_callbacks_exceptions=False):
        """EventHandler initiazition recibes a list of allowed event names as arguments."""
        self.__events = {}
        self.verbose = verbose
        self.tolerate_exceptions = tolerate_callbacks_exceptions
        self.stream_output = stream_output

        if event_names:
            for event in event_names:
                self.register_event(str(event))  # cast as str to be safe

        print(f'{self.__str__()} has been init.', file=self.stream_output) if self.verbose else None

    @property
    def events(self):
        """Return events as readOnly."""
        return self.__events

    def clear_events(self):
        """Clear all events."""
        self.__events = {}
        return True

    @property
    def event_list(self) -> [str]:
        """Retun  list of regitered events."""
        return self.__events.keys()

    @property
    def count_events(self) -> int:
        """Return number of registered events."""
        return len(self.event_list)

    def is_event_registered(self, event_name: str) -> bool:
        """Return if an event is current registered."""
        return event_name in self.__events

    def register_event(self, event_name: str) -> bool:
        """Register an event name."""
        # print('registering event', event_name, self.events)
        if self.is_event_registered(event_name):
            print(f'Omiting event {event_name} registration, already implemented',
                  file=self.stream_output) if self.verbose else None
            return False

        self.__events[event_name] = []
        return True

    def unregister_event(self, event_name: str) -> bool:
        """Unregister an event name."""
        if event_name in self.__events:
            del self.__events[event_name]
            return True
        print(f'Omiting unregister_event. {event_name} '
              f'is not implemented.', file=self.stream_output) if self.verbose else None
        return False

    @staticmethod
    def is_callable(func: callable) -> bool:
        """Return true if func is a callable variable."""
        return isinstance(func,
                          (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType))

    def is_callback_in_event(self, event_name: str, callback: callable):
        return callback in self.__events[event_name]

    def link(self, callback: callable, event_name: str) -> bool:
        """Bind a callback to an event."""

        if not self.is_callable(callback):
            print(f'Callback not registered. Type {type(callback)} '
                  f'is not a callable function.', file=self.stream_output) if self.verbose else None
            return False

        if not self.is_event_registered(event_name):
            raise EventHandler.Exceptions.EventNotAllowedError(
                f'Can not link event {event_name}, not registered. Registered events are:'
                f' {", ".join(self.__events.keys())}. Please register event {event_name} before link callbacks.')

        if callback not in self.__events[event_name]:
            self.__events[event_name].append(callback)
            return True

        print(f'Can not link callback {str(callback.__name__)}, already registered in '
              f'{event_name} event.', file=self.stream_output) if self.verbose else None
        return False

    def unlink(self, callback: callable, event_name: str) -> bool:
        """Unbind a callback from an event."""
        if not self.is_event_registered(event_name):
            print(f'Can not unlink event {event_name}, not registered. Registered events '
                  f'are: {", ".join(self.__events.keys())}. '
                  f'Please register event {event_name} before unlink callbacks.', file=self.stream_output)
            return False

        if callback in self.__events[event_name]:
            self.__events[event_name].remove(callback)
            return True

        print(f'Can not unlink callback {str(callback.__name__)}, is not registered in '
              f'{event_name} event.', file=self.stream_output) if self.verbose else None

        return False

    def fire(self, event_name: str, *args, **kwargs) -> bool:
        """Fire an event callbacks and return True only if all callbacks was successfully."""
        all_ok = True
        for callback in self.__events[event_name]:
            try:
                callable(callback(*args, **kwargs))
            except Exception as e:
                if not self.tolerate_exceptions:
                    raise e
                else:
                    if self.verbose:
                        print(f'WARNING: {str(callback.__name__)} produces an exception error.',
                              file=self.stream_output)
                        print('Arguments', args, file=self.stream_output)
                        print(e, file=self.stream_output)
                    all_ok = False
                    continue

        return all_ok

    def __str__(self):
        """Return a string representation"""

        event_related = \
            [f"{event}=[{', '.join([callback.__name__ for callback in self.__events[event]])}]" for event in
             self.__events]
        mem_address = str(hex(id(self)))
        return f'<class {self.__class__.__name__} at ' \
            f'{mem_address}: events=({event_related}), verbose={self.verbose}, ' \
            f'tolerate_exceptions={self.tolerate_exceptions}>'
