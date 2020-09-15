from distutils.core import setup
from eventhandler import __version__

setup(
    name='eventhandler',
    version=__version__,
    packages=['eventhandler'],
    url='https://github.com/davidvicenteranz/eventhandler',
    license='MIT License',
    author='David Vicente',
    author_email='dvicente74@gmail.com',
    description='eventhandler is a basic, but effective, event handler library for Python',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    )
)
