# -*- coding: utf8
from __future__ import division, print_function

import web

RENDER = web.template.render('templates/', base='base') 

class Home:
    def GET(self):
        return RENDER.home()

class NewEval:
    def GET(self):
        return RENDER.new()

class ContinueEval:
    def GET(self):
        return RENDER.cont()

class Disclaimer:
    def GET(self):
        return RENDER.disclaimer()

class Code:
    def GET(self):
        return RENDER.code()

class Privacy:
    def GET(self):
        return RENDER.privacy()
