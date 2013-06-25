# -*- coding: utf8
from __future__ import division, print_function
'''
Contains the handlers for different requests which can be submitted to the
application. In other words, this is the view of the MVC pattern.
'''

from config import IDLEN
from config import TEMPLATE_DIR

from web import net
from web import utils

import control
import web

RENDER = web.template.render(TEMPLATE_DIR, base='base') 

class LeftAlignForm(web.form.Form):
    '''
    Overwrites the rendering of forms so that they are left aligned.
    '''

    def render(self):
        out = ''
        out += self.rendernote(self.note)
        out += '<table class="form">\n'
        
        for input_ in self.inputs:
            html = utils.safeunicode(input_.pre) + input_.render() + \
                    self.rendernote(input_.note) + \
                    utils.safeunicode(input_.post)

            if input_.is_hidden():
                out += '    <tr style="display: none;">'
                out += '<th></th><td>%s</td></tr>\n' % (html)
            else: 
                out += '<tr class="blank_row"><td colspan="2"></td></tr>'
                out += '    <tr>' #start row
                
                #header on the left
                out += '    <td class="question"><label for="%s">' % \
                        input_.id 
                out += '%s</td>' % net.websafe(input_.description)

                #content on the right
                out += '<td><div style="float:left;">%s</div></td></tr>' % html
                out += '<tr class="blank_row_ruler"><td colspan="2"></td></tr>'

        out += '</table>'
        return out

class MyRadio(web.form.Radio):
    '''Adds new line between choices, more readable for Radio buttons.'''

    def render(self):
        out = ''

        for arg in self.args:
            if isinstance(arg, (tuple, list)):
                value, desc = arg
            else:
                value, desc = arg, arg

            attrs = self.attrs.copy()
            attrs['name'] = self.name
            attrs['type'] = 'radio'
            attrs['value'] = value

            if self.value == value:
                attrs['checked'] = 'checked'

            out += '<input %s/> %s</br>' % (attrs, net.websafe(desc))

        return out


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
    Also redirects to actual evaluation after user clicks on submit. On a new
    evaluation the ID is added to the database. This guarantees that all other
    pages do not have to check if id exists. The user may change the url to
    supply invalid ids, but we do not deal with this!
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

            return RENDER.helppage(id_, form())
        else:
            return web.seeother('home')

    def POST(self):
        posted_data = web.input()
        id_ = int(posted_data['id'])
        if control.has_user_id(id_):
            return web.seeother('/videopage?id=%d' % id_)
        else:
          return web.seeother('/userpage?id=%d' % id_)

class UserPage(object):
    '''
    Page with a form to gather demographic and sharing habits information
    about the users
    '''

    def GET(self):

        params = web.input()
        id_ = int(params['id'])
        error = 'error' in params
        
        form = LeftAlignForm(
                web.form.Dropdown('age',
                    [('0', '--'),
                    ('15', '15 or less'),
                    ('20', '16 to 20'),
                    ('25', '21 to 25'),
                    ('30', '26 to 30'),
                    ('35', '31 to 35'),
                    ('40', '36 to 40'),
                    ('45', '41 to 45'),
                    ('50', '46 to 50'),
                    ('55', '41 to 55'),
                    ('56', '56 or above')],
                    description='How old are you?'),
                
                MyRadio('gender',
                    [('1', 'Male'),
                     ('2', 'Female')],
                    description='Are you a Male or a Female?'),
                
                web.form.Textbox('country', 
                    description='Type the country you live in:',
                    size=12, maxlength=50, cols=1, rows=1),
                
                MyRadio('view',
                    [('5', 'Very Often (once or more daily)'),
                     ('4', 'Often (few times a week)'),
                     ('3', 'Occasionally (few times a month)'),
                     ('2', 'Rarely (few times a year)'),
                     ('1', 'Never')],
                    description='How often do you watch a video on YouTube?'),

                MyRadio('share',
                    [('5', 'Very Often (once or more daily)'),
                     ('4', 'Often (few times a week)'),
                     ('3', 'Occasionally (few times a month)'),
                     ('2', 'Rarely (few times a year)'),
                     ('1', 'Never')],
                    description='How often do you share YouTube videos' + \
                            ' with friends or colleagues?'),
                
                MyRadio('shareall',
                    [('5', 'Very Often (once or more daily)'),
                     ('4', 'Often (few times a week)'),
                     ('3', 'Occasionally (few times a month)'),
                     ('2', 'Rarely (few times a year)'),
                     ('1', 'Never')],
                    description='How often do you share any kind of online '
                        'content with friends or colleagues?'),
                
                web.form.Button('done', type='submit', 
                    html='Go to Video Evaluations'),

                web.form.Hidden('id', value=id_))
 
        return RENDER.userpage(id_, form(), error)

    def POST(self):
        
        posted_data = web.input()
        valid = 'age' in posted_data and 'gender' in posted_data \
                and 'country' in posted_data and 'view' in posted_data \
                and 'share' in posted_data and 'shareall' in posted_data \
                and posted_data['country'].strip() != '' \
                and int(posted_data['age']) != 0

        id_ = int(posted_data['id'])
        
        if not valid: #at least one radio per question
            return web.seeother('/userpage?id=%d&error=1' % id_)
        else:
            age = int(posted_data['age'])
            gender = int(posted_data['gender'])
            country = posted_data['country']
            view = int(posted_data['view'])
            share = int(posted_data['share'])
            shareall = int(posted_data['shareall'])

            control.save_user_info(id_, age, gender, country, view, share,
                    shareall)

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
        
        if not error:
            data = control.get_video_ids(id_)
        else:
            data = control.get_current_pair(id_)

        if data: #If no more data, this session has evaluated all pairs
            pair_num, video_id1, video_id2 = data
            num_pairs = control.num_pairs(id_)
            
            control.save_start_eval(id_)

            form = LeftAlignForm(
                    MyRadio('like',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'I liked them both'),
                         ('0', 'I don\'t like either of them')],
                        description='Which video did you like more?'),
                    
                    MyRadio('share',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'Both'),
                         ('0', 'Neither')],
                        description='Which video would you share with your' + \
                                ' friends?'),

                    MyRadio('pop',
                        [('1', 'Video 1 (left)'),
                         ('2', 'Video 2 (right)'),
                         ('3', 'I think they will be equally popular'),
                         ('0', 'I don\'t know')],
                        description='Which video do you predict will be more popular on YouTube?'),

                    MyRadio('know',
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
