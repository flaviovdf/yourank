yourank
=======

Simple web application for user evaluation of Youtube videos

requirements
============

   * python 2.5 or above
   * web.py (easy_install web.py)
   * flup (easy_install flup) - only needed when using lightppd or apache

how to populate database
========================

Use the create_db.py script

::

$ python create_db.py

It will read the contents of the *pairs/video.pairs* file. In this file each
line has to be two youtube video ids separated by whitespace. The database
will be in sqllite3 format under the name *database.db*.

how to deploy
=============

In standalone mode just jun the code.py script or use the start.sh script

::

$ python code.py

or

::

$ ./start.sh

using lightppd + fastcgi
========================

See https://wiki.ubuntu.com/Lighttpd%2BPHP and 
http://crosbymichael.com/webpy-server-setup.html (ignore the mysql part)
