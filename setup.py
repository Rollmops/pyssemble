from setuptools import setup, find_packages

from pyssemble import __version__

setup(name="pyssemble",
      version=__version__,
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pyssemble = pyssemble.main.pyssemble:main'
          ]
      },
      )
