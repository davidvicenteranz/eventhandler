from distutils.core import setup
from eventhandler import __version__, __author__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='eventhandler',
    version=__version__,
    packages=['eventhandler'],
    url='https://github.com/davidvicenteranz/eventhandler',
    license='MIT License',
    author=__author__,
    author_email='dvicente74@gmail.com',
    description='A simple and effective event handler class, based in callbacks for python 3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    long_description=long_description
)