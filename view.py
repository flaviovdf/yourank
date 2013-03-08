# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the handlers for different requests which
can be submitted to the application. In other words,
this is the view of the MVC pattern.
'''

from config import TEMPLATE_DIR

import string
import random
import web

RENDER = web.template.render(TEMPLATE_DIR, base='base') 

def random_string(num_chars=10):
   '''Generates a random ascii string composed of letters and numbers'''

   chars = string.ascii_uppercase + string.digits
   return u''.join(random.choice(chars) for x in xrange(num_chars))

class Redirect(object):
    '''Redirects pages ending in '/' to the correct urls'''

    def GET(self, page):
        return web.seeother('/' + page)

class Home(object):
    '''Renders the Home/Welcome page'''

    def GET(self):
        return RENDER.home()

class Disclaimer(object):
    '''Renders the Disclaimer page'''

    def GET(self):
        return RENDER.disclaimer()

class Code(object):
    '''Renders the Source Code page'''

    def GET(self):
        return RENDER.code()

class Privacy(object):
    '''Renders the Privacy page'''

    def GET(self):
        return RENDER.privacy()

class NewEval(object):
    '''
    Renders page for new evaluation, generating user id as a random string.
    Also redirects to actual evaluation after user clicks on submit.
    '''

    def GET(self):
        unique_id = random_string()
        form = web.form.Form(
                web.form.Button('start', type='submit', html='Start Evaluation'),
                web.form.Hidden('id', value=unique_id))

        return RENDER.new(unique_id, form())

    def POST(self):
        posted_data = web.input()
        id_ = posted_data['id']
        return web.seeother('/video_pair')

class ContinueEval:
    def GET(self):
        return RENDER.cont()
