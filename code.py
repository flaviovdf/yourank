#!/usr/bin/env python
# -*- coding: utf8

from __future__ import division, print_function
'''
Contains the main for deploying the application.
This code maps resources to handlers and starts
the web.py application.
'''

import handlers

import web

URLS = ('/', handlers.Home)

APP = web.application(URLS, locals())
if __name__ == '__main__':
    APP.run()
