# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the handlers for different requests which
can be submitted to the application. In other words,
this is the view of the MVC pattern.
'''

from config import IDLEN
from config import TEMPLATE_DIR

import control
import web

RENDER = web.template.render(TEMPLATE_DIR, base='base') 

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
        unique_id = control.random_id()
        form = web.form.Form(
                web.form.Button('start', type='submit',
                    html='Start Evaluation'),
                web.form.Hidden('id', value=unique_id))

        return RENDER.new(unique_id, form())

    def POST(self):
        posted_data = web.input()
        id_ = int(posted_data['id'])
        control.add_id(id_)
        return web.seeother('/videopage?id=%d' % id_)

class ContinueEval(object):

    def __init__(self):
        s = IDLEN
        self.form = web.form.Form(
                web.form.Textarea('id', description='Unique ID',
                    size=s, maxlength=s, cols=s, rows=1),
                web.form.Button('start', type='submit', 
                    html='Continue Evaluation'))

    def GET(self):
        input_data = web.input()
        if 'error' in input_data:
            return RENDER.cont(self.form(), True)
        else:
            return RENDER.cont(self.form(), False)

    def POST(self):
        posted_data = web.input()
        
        if 'id' in posted_data and posted_data['id'].isdigit() and \
                control.has_id(int(posted_data['id'])):
            id_ = int(posted_data['id'])
            return web.seeother('/videopage?id=%d' % id_)
        else:
            return web.seeother('/continue?error=1')

class VideoPage(object):

    def GET(self):
        
        params = web.input()
        id_ = int(params['id'])
        
        data = control.get_video_ids(id_)
        if data:
            pair_num, video_id1, video_id2 = data
            form = web.form.Form(
                    web.form.Radio('Which Video Would You Send to a Friend?',
                        [('vid1', 'I would send Video 1 (left)'),
                         ('vid2', 'I would send Video 2 (right)')],
                    id='choice'),
                    web.form.Textarea('details', 
                        description='Please provide additional' + 
                            ' details here (optional)',
                        cols=80, rows=2),
                    web.form.Button('done', type='submit', html='Send Evaluation'),
                    web.form.Hidden('id', value=id_))
            
            return RENDER.videopage(pair_num, video_id1, video_id2, form)
        else:
            return RENDER.thankyou()

    def POST(self):

        posted_data = web.input()
        id_ = int(posted_data['id'])
        control.increment_pair_num(id_)
        return web.seeother('/videopage?id=%d' % id_)
