'''
podderewski: A program to automate downloading of podcast episodes.

Copyright 2015, Tony Rein.
Licensed under MIT.
'''
import sys
from setuptools import setup, find_packages
#from setuptools.command.test import test as TestCommand
from setuptools.command.install import install as _install
from pkg_resources import resource_stream
import shutil



# # This is a plug-in for setuptools that will invoke py.test
# # when you run python setup.py test
# class PyTest(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True
# 
#     def run_tests(self):
#         import pytest  # import here, because outside the required eggs aren't loaded yet
#         sys.exit(pytest.main(self.test_args))


version = "0.9.5.1"

class install(_install):
    def install_config_file(self):
        instream = resource_stream('podderewski', '/data/podderewski.cfg')
        outfilename = '/etc/podderewski.cfg'
        with open(outfilename, 'wt') as f:
            shutil.copyfileobj(instream, f)
#     def install_logrotate_conf(self):
#         instream = resource_stream('podderewski', '/data/logrotate.cfg')
#         outfilename = '/etc/logrotate.d/podderewski'
#         with open(outfilename, 'wt') as f:
#             shutil.copyfileobj(instream, f)

    def run(self):
        _install.run(self)
        print('Post-install stage...')
        print('Copying config file...')
        self.install_config_file()
#         self.install_logrotate_conf()

setup(name="podderewski",
      version=version,
      description="podderewski is a utility for putting data generated by a HonSSH honeypot into an Elasticsearch database.",
      long_description=open("README.md").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Multimedia :: Sound/Audio',
        'Intended Audience :: End Users/Desktop'
      ],
      keywords="podcast download", # Separate with spaces
      author="Tony Rein",
      author_email="trein@cinci.rr.com",
      url="https://github.com/tonyrein/podderewski.git",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      #tests_require=['pytest'],
      cmdclass={'install': install},
      # package_data files are:
      #		* podderewski.cfg, a default configuration file
      #
      package_data = {'podderewski': ['data/podderewski.cfg']},
      install_requires=['wget', 'peewee' ],

      # The entry_points entry results in an executable script called 'podderewski'
      # in the PATH, which invokes the main() method in the 'main' module.
      entry_points={
        'console_scripts':
            ['podderewski=podderewski.main:main']
      }
)