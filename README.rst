===============
Buzz CLI Tester
===============

This is a framework for automating CLI tests.  It is not intended to replace
unittest frameworks like tox or nosetests, nor is it attempting to be 
an automated test service like Jekins.  This is a simple framework for 
automating CLI sanity tests.  

When releasing software, even after the automated unit tests, smoke tests,
functional tests, and acceptance test pass you often want to run a 
a few commands by hand.  Further, sometimes as a developer you start
with a set of commands that you run to make sure things generally work.
Sometimes users will give you a set of commands that do not work, and
you have to repeatedly type them while you debug.

The repeated typing is no big deal if it is a single or small set of
commands.  However, when one command starts depending on another 
a lot of copy and pasting starts to happen, and a lot of time is 
wasted.

This module aims to automate that situation while still retaining the
look at feel of a CLI console.

Example Scenerio
----------------

As an example, lets say you have a program that will upload a file to 
some storage cloud.  On standard out, this program will give you a 
UUID that you must use to reference the file in the future.  You can
use the UUID to download the file, delete the file, or query the file 
for meta data.  

Now lets say a user comes a long and says, "If I upload a file, and then
query its meta data, I have to run delete twice in order to actually
delete it."

In order to recreate the bug you will start by uploading the file, 
copying the UUID, querying the file and pasting in the UUID, and
then deleting the file by again pasting the UUID to the console.

If the bug gets hairy you may find yourself performing that sequence 
of commands fifty times or more.

With this framwork you could instead create a small python file that
recreates the step for you and run them all (including the automated
copy and paste) with a single command.  Further, once you fix the
bug you will have a log file that mimics exactly what the console
would have looked like had you typed the commands.

that creates a file and gives
you its md5sum to stdard output.  You then 

