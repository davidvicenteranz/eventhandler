from distutils.core import setup
from eventhandler import __version__, __author__

setup(
    name='eventhandler',
    version=__version__,
    setup_requires=['wheel']
    packages=['eventhandler'],
    url='https://github.com/davidvicenteranz/eventhandler',
    license='MIT License',
    author=__author__,
    author_email='dvicente74@gmail.com',
    description='A simple but effective event handler, based in calbacks, written in pure python 3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: 6'
    ]
)
