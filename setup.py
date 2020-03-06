import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyseas",
    version = "0.0.1",
    author = "Tim Hochberg",
    author_email = "tim@globalfishingwatch.org",
    description = ("Python Utilities for GFW Research and Innovation Group."),
    license = "Apache-2.0",
    keywords = "plot GFW",
    # url = "http://packages.python.org/an_example_pypi_project",
    packages=['pyseas'],
    # long_description=read('README.md'),
    # install_requires=['jupytext'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache-2.0 License",
    ],
)