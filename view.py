# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the handlers for different requests which can be submitted to the
application. In other words, this is the view of the MVC pattern.
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
                    html='Proceed to Instructions Page'),
                web.form.Hidden('id', value=unique_id))

        return RENDER.new(unique_id, form())

    def POST(self):
        posted_data = web.input()
        id_ = int(posted_data['id'])
        control.add_id(id_)
        return web.seeother('/helppage?id=%d' % id_)

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
            return web.seeother('/helppage?id=%d' % id_)
        else:
            return web.seeother('/continue?error=1')

class Help(object):
    '''Displays the help page with what is expected from the user'''

    def GET(self):

        posted_data = web.input()
        if 'id' in posted_data:
            id_ = int(posted_data['id'])
            form = web.form.Form(
                    web.form.Button('start', type='submit',
                        html='Proceed to Evaluations'),
                    web.form.Hidden('id', value=id_))

            num_pairs = control.num_pairs()
            return RENDER.helppage(id_, num_pairs, form())
        else:
            return web.seeother('home')

    def POST(self):
        posted_data = web.input()
        id_ = int(posted_data['id'])
        return web.seeother('/videopage?id=%d' % id_)
    
class VideoPage(object):
    '''
    The actual experiment is performed on video pages. Here each user will be
    required to evaluate a video pair and answer a form. If the answer is 
    invalid (e.g, a required field was not set) the code issues an error.
    Otherwise, it will save the answer and proceed to the next pair untill
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
                    web.form.Radio('like',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'I liked them both'),
                         ('0', 'I don\'t like either of them')],
                        description='Which video did you like the most?'),
                    
                    web.form.Radio('share',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'Both'),
                         ('0', 'Neither')],
                        description='Which video would you share with your' + \
                                ' friends?'),

                    web.form.Radio('pop',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'I think they will be equally popular'),
                         ('0', 'I don\'t know')],
                        description='Which video do you think will become' + \
                                ' more popular?'),

                    web.form.Radio('know',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'Both'),
                         ('0', 'Neither')],
                        description='Did you already know one of these videos?'),

                    web.form.Textarea('details', 
                        description='If you want, provide extra feedback' + \
                                ' on the videos:',
                        cols=80, rows=2),
                    
                    web.form.Button('done', type='submit', 
                        html='Send Evaluation'),
                    web.form.Button('ignore', type='submit', 
                        html='I was unable to watch one (or both) of the videos'),

                    web.form.Hidden('id', value=id_))
            
            return RENDER.videopage(id_, pair_num, num_pairs, video_id1, 
                    video_id2, form, error)
        else:
            return RENDER.thankyou()

    def POST(self):

        posted_data = web.input()
        print(posted_data)
        id_ = int(posted_data['id'])

        valid = ('like' in posted_data and 'share' in posted_data \
                and 'pop' in posted_data and 'done' in posted_data \
                and 'know' in posted_data) or 'ignore' in posted_data

        if not valid: #at least one radio per question
            return web.seeother('/videopage?id=%d&error=1' % id_)
        else:
            if 'ignore' in posted_data:
                like = -1
                share = -1
                pop = -1
                know = -1
            else:
                like = int(posted_data['like'])
                share = int(posted_data['share'])
                pop = int(posted_data['pop'])
                know = int(posted_data['know'])

            details = u''
            if 'details' in posted_data:
                details = posted_data['details']

            control.save_results(id_, like, share, pop, details)
            return web.seeother('/videopage?id=%d' % id_)
