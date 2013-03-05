# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the main for deploying the application.
'''

import web

URLS = ('/', 'index')

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == '__main__':
    app = web.application(URLS, globals())
    app.run()
