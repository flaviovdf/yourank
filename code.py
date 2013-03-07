# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the main for deploying the application.
This code maps resources to handlers and starts
the web.py application.
'''

import handlers

import web

URLS = ('/(.*)/', handlers.Redirect,
        '/', handlers.Home,
        '/home', handlers.Home,
        '/new', handlers.NewEval,
        '/continue', handlers.ContinueEval,
        '/disclaimer', handlers.Disclaimer,
        '/privacy', handlers.Privacy,
        '/code', handlers.Code)

APP = web.application(URLS, locals())
if __name__ == '__main__':
    APP.run()
