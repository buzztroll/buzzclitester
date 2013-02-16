import os
import setuptools
import sys


setuptools.setup(
    name="buzztester",
    version="0.1",
    description="A tool for running CLI tests",
    long_description="""
      This python library allows for the automation of command line
      tests.  This is in no way intended to replace tools like tox
      or nosetests.  This is simply to automate things you would
      normally type at the command line.  Once a test is made a
      log file is created that should look exactly like the commands
      were typed into a command line.

      Creation of the tests are done with a framework around pexpect.
      """,
    license='Apache',
    author='John Bresnahan',
    author_email='buzztroll@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: OpenStack',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={'console_scripts': 
                    ['buzzclitests = buzzclitester.buzztest:main']},
)
