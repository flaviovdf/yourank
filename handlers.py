# -*- coding: utf8
from __future__ import division, print_function

import web

RENDER = web.template.render('templates/', base='base') 

class Home(object):

    def GET(self):
        return RENDER.home()
