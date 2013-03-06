# -*- coding: utf8
from __future__ import division, print_function

import web

RENDER = web.template.render('templates/') 

class Home:
    def GET(self):
        return "Hello, world!"
