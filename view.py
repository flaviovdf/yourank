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
    '''
    Renders the continue evaluation page. Here users will be
    required to provide their unique session id to continue
    an evaluation. If the user supplies an invalid id an error
    is issued.
    '''

    def __init__(self):
        s = IDLEN
        self.form = web.form.Form(
                web.form.Textbox('id', description='Unique ID',
                    size=s, maxlength=s, cols=s, rows=1),
                web.form.Button('start', type='submit', 
                    html='Continue Evaluation'))

    def GET(self):
        params = web.input()
        if 'error' in params:
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
    '''
    The actual experiment is performed on video pages. Here each user will be
    required to evaluate a video pair and answer a form. If the answer is 
    invalid (e.g, a required field was not set) the code issues an error.
    Otherwise, it will save the answer and proceed to the next pair until
    completion.
    '''

    def GET(self):
        
        params = web.input()
        id_ = int(params['id'])
        error = 'error' in params
        
        data = control.get_video_ids(id_)
        if data: #If no more data, this session has evaluated all pairs
            pair_num, video_id1, video_id2 = data
            num_pairs = control.num_pairs()

            form = web.form.Form(
                    web.form.Radio('choice',
                        [('1', 'I would send Video 1 (left)'),
                         ('2', 'I would send Video 2 (right)')],
                        description='Which Video Would You Send to a Friend?'),
                    web.form.Textarea('details', 
                        description='Please provide additional' + 
                            ' details here (optional)',
                        cols=80, rows=2),
                    web.form.Button('done', type='submit', html='Send Evaluation'),
                    web.form.Hidden('id', value=id_))
            
            return RENDER.videopage(id_, pair_num, num_pairs, video_id1, 
                    video_id2, form, error)
        else:
            return RENDER.thankyou()

    def POST(self):

        posted_data = web.input()
        id_ = int(posted_data['id'])

        if 'choice' not in posted_data: #at least one radio has to be checked
            return web.seeother('/videopage?id=%d&error=1' % id_)
        else:
            choice = int(posted_data['choice'])
            details = ''
            if 'details' in posted_data:
                details = posted_data['details']

            control.save_results(id_, choice, details)
            return web.seeother('/videopage?id=%d' % id_)