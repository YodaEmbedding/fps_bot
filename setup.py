#!/usr/bin/env python3
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fps_bot",
    version = "0.1.0",
    author = "Mateen Ulhaq",
    description = "Bot for reddit to improve fps of requested videos through motion interpolation",
    license = "MIT",
    keywords = "reddit bot motion-interpolation",
    packages=['fps_bot'],
    long_description=read('README.md'),
    install_requires=[
        'praw',
        'pfycat',
        'youtube-dl',
    ],
)
