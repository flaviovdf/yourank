#!/usr/bin/env python
# -*- coding: utf8

from __future__ import division, print_function
'''
Contains the main for deploying the application.
This code maps resources to handlers and starts
the web.py application.
'''

from yourank import handlers

import web

URLS = ('/', handlers.Index)

APP = web.application(URLS, locals())
if __name__ == '__main__':
    APP.run()
