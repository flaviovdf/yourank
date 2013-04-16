#!/usr/bin/env python
# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the main for deploying the application. This code maps resources 
to view and starts the web.py application.
'''

import view
import web

URLS = ('/(.*)/', view.Redirect,
        '/', view.Home,
        '/home', view.Home,
        '/helppage', view.Help,
        '/new', view.NewEval,
        '/continue', view.ContinueEval,
        '/disclaimer', view.Disclaimer,
        '/privacy', view.Privacy,
        '/code', view.Code,
        '/userpage', view.UserPage,
        '/videopage', view.VideoPage)

if __name__ == '__main__':
    app = web.application(URLS, globals())
    app.run()
