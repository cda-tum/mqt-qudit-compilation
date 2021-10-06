#!/usr/binq/env python
from setuptools import setup, find_packages

setup(version='0.0',
      description='An incremental qudit compiler',
      author='Kevin Mato',
      author_email='kevn.mato@tum.de',
      packages=find_packages(),
      install_requires=[],
      test_suite="test",
)