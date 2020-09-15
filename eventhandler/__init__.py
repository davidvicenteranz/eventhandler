import sys
import types

__version__ = '1.0.2'


class EventHandler:
    """Event manager, bind, unbind and fire events."""

    class Exceptions:
        """Custom error classes."""
        class EventNotAllowedError(Exception):
            pass

    events: dict = {}  # Wil hold events names as keys and callbacks as value list of the event key.
    tolerate_exceptions = False  # Do not raise an error if a callback fails

    def __init__(self, *event_names, verbose=False, file_to_verbose=sys.stdout, tolerate_callbacks_exceptions=False):
        """EventHandler initiazition recibes a list of allowed event names as arguments."""
        self.verbose = verbose
        self.tolerate_exceptions = tolerate_callbacks_exceptions
        self.print_file = file_to_verbose
        if event_names:
            for event in event_names:
                self.register_event(str(event)) # cast as str to be safe

    @property
    def registered_events(self) -> [str]:
        """Retun  list of regitered events."""
        return self.events.keys()

    def event_registered(self, event_name: str) -> bool:
        """Return if an event is current registered."""
        return event_name in self.events

    def register_event(self, event_name: str) -> bool:
        """Register an event name."""
        # print('registering event', event_name, self.events)
        if event_name in self.events:
            print(f'Omiting. {event_name} is already implemented', file=self.print_file) if self.verbose else None
            return False

        self.events[event_name] = []
        return True

    def unregister_event(self, event_name: str) -> bool:
        """Unregister an event name."""
        if event_name in self.events:
            del self.events[event_name]
            return True
        print(f'Omiting unregister_event. {event_name} '
              f'is not implemented.', file=self.print_file) if self.verbose else None
        return False

    def is_callable(self, func: callable) -> bool:
        """Return true if func is a callable variable."""
        return isinstance(func,
                          (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType))

    def bind(self, event_name: str, callback: callable) -> bool:
        """Bind a callback to an event."""

        if not self.is_callable(callback):
            print(f'Callback not registered. Type {type(callback)} '
                  f'is not a callable function.', file=self.print_file) if self.verbose else None
            return False

        if not self.event_registered(event_name):
            raise EventHandler.Exceptions.EventNotAllowedError(
                f'Can not bind event {event_name}, not registered. Registered events are:'
                f' {", ".join(self.events.keys())}. Please register event {event_name} before bind callbacks.')

        if callback not in self.events[event_name]:
            self.events[event_name].append(callback)
            return True

        print(f'Can not bind callback {str(callback.__name__)}, already registered in '
              f'{event_name} event.', file=self.print_file) if self.verbose else None
        return False

    def fire(self, event_name: str, *args, **kwargs) -> bool:
        """Fire an event callbacks and return True only if all callbacks was successfully."""

        all_ok = True
        for callback in self.events[event_name]:
            try:
                callable(callback(*args, **kwargs))
            except Exception as e:
                if not self.tolerate_exceptions:
                    raise e
                else:
                    if self.verbose:
                        print(f'WARNING: {str(callback.__name__)} produces an exception error.', file=self.print_file)
                        print('Arguments', args, file=self.print_file)
                        print(e, file=self.print_file)
                        all_ok = False
                    continue

        return all_ok

    def unbind(self, event_name: str, callback: callable) -> bool:
        """Unbind a callback from an event."""
        if not self.event_registered(event_name):
            print(f'Can not unbind event {event_name}, not registered. Registered events '
                  f'are: {", ".join(self.events.keys())}. '
                  f'Please register event {event_name} before unbind callbacks.', file=self.print_file)
            return False

        if callback in self.events[event_name]:
            self.events[event_name].remove(callback)
            return True

        print(f'Can not unbind callback {str(callback.__name__)}, is not registered in '
              f'{event_name} event.', file=self.print_file) if self.verbose else None

        return False
