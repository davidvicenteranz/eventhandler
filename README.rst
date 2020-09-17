eventhandler
============

<<<<<<< HEAD
A simple but, **effective event handler based in calbacks**, written in pure python 3.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
=======
Is a simple and effective event handler class, based in callbacks for python 3
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

eventhandler
~~~~~~~~~~~~
Is a **python simple and effective event handler class**, based in callbacks for python 3.

>>>>>>> release/1.1.24

Build Status:
~~~~~~~~~~~~~

<<<<<<< HEAD
| |Build Status| |Coverage Status|  |Python package and publish|

**Github code and samples** https://pypi.python.org/pypi/eventhandler
=======
| |Build Status| |Coverage Status| |Pypi| |Python package and publish|

**Github code and samples** https://github.com/davidvicenteranz/eventhandler
>>>>>>> release/1.1.24

Quick start
-----------

Install the package
~~~~~~~~~~~~~~~~~~~

.. code::

    $ pip install eventhandler

Usage example
~~~~~~~~~~~~~

<<<<<<< HEAD
=======
Lets see a simple example of a chat room controlled by a bot using event calls.

>>>>>>> release/1.1.24
.. code::

    from eventhandler import EventHandler

    class ChatRoom:
        """Simulates a chatroom environment with event handler implementation."""
        messages = [] # Holds user messages
        users = {'bot':[]} # Holds

        def __init__(self):
            """Initialize de chat room."""
            # Define posible events
            self.event_handler = EventHandler('on-newuser', 'on-message')
            # Bind callback function to events
            self.event_handler.bind('on-newuser', self.on_newuser_join)
            self.event_handler.bind('on-message', self.on_message)

        def user_list(self):
            """Return a list of users."""
            return [user for user in self.users.keys() if user != 'bot']

        def on_newuser_join(self, user):
            """Print a message when a user join the chat room."""
            print(f'{user} has joined the chat.')

        def on_message(self, user, msg):
            """Print the user message"""
            print(f'{user} says:\t {msg}')

        def say(self, user, msg):
            """Send a messega to the chat room."""
            if not user in self.users:
                self.users[user] = []
                self.event_handler.fire('on-newuser', user)

            if msg != '':
                self.messages.append((user, msg))
                self.event_handler.fire('on-message', user, msg)

    # Create the chatroom
    chat = ChatRoom()

    # This is a external callback to bind in the chatroom event habdler
    def saludate_new_user(user):
        """Bot saludates the user."""
        chat.say('bot', f'Hello {user}, welcome to the chat room.')

    # This is a external callback to bind in the chatroom event habdler
    def response_to_user(user, msg):
        """Bot responses to user."""
        if user=='bot':
            return
        if msg == 'Hey bot, are there anyone here?':
            if len(chat.users.keys()) == 2:
                chat.say('bot', f'Nope {user}. Just you and me.')
            else:
                chat.say('bot', f'Yes {user}. there are {len(chat.users.keys())-1} users in the room.')

    # Bind the external callbacks
    chat.event_handler.bind('on-newuser', saludate_new_user)
    chat.event_handler.bind('on-message', response_to_user)

    # Chat simulation
    chat.say('sergio', 'Hello World!')
    chat.say('sergio', 'Hey bot, are there anyone here?')
    chat.say('david', 'Hello everybody!')
    chat.say('david', 'Hey bot, are there anyone here?')
    chat.say('sergio', 'Hi david!')

**The avobe code must produce and output this:**

.. code:: text

    sergio has joined the chat.
    bot says:    Hello sergio, welcome to the chat room.
    sergio says:     Hello World!
    sergio says:     Hey bot, are there anyone here?
    bot says:    Nope sergio. Just you and me.
    david has joined the chat.
    bot says:    Hello david, welcome to the chat room.
    david says:  Hello everybody!
    david says:  Hey bot, are there anyone here?
    bot says:    Yes david. there are 2 users in the room.
    sergio says:     Hi david!

<<<<<<< HEAD
=======
**Thanks for watching and enjoy it.**

>>>>>>> release/1.1.24
.. |Build Status| image:: https://travis-ci.org/davidvicenteranz/eventhandler.svg?branch=master
   :target: https://travis-ci.org/davidvicenteranz/eventhandler
.. |Coverage Status| image:: https://coveralls.io/repos/github/davidvicenteranz/eventhandler/badge.svg
   :target: https://coveralls.io/github/davidvicenteranz/eventhandler
.. |Python package and publish| image:: https://github.com/davidvicenteranz/eventhandler/workflows/Python%20package%20and%20publish/badge.svg?branch=master
<<<<<<< HEAD
   :target: https://pypi.org/project/eventhandler/
=======
   :target: https://github.com/davidvicenteranz/eventhandler
.. |Pypi| image:: https://badge.fury.io/py/eventhandler.svg
    :target: https://badge.fury.io/py/eventhandler
>>>>>>> release/1.1.24
