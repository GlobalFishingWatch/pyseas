import os
from setuptools import setup
import pyseas

setup(
    name = "pyseas",
    version = pyseas.__version__,
    author = "Tim Hochberg",
    author_email = "tim@globalfishingwatch.org",
    description = ("Python Utilities for GFW Research and Innovation Group."),
    license = "Apache-2.0",
    keywords = "plot GFW",
    # url = "http://packages.python.org/an_example_pypi_project",
    packages=['pyseas'],
    # long_description=read('README.md'),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache-2.0 License",
    ],
)