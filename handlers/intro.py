import flask
from handlers import copy
from db import posts

blueprint = flask.Blueprint("intro", __name__)

@blueprint.route('/')
def introscreen():
    return flask.render_template('intro.html', title=copy.title, subtitle=copy.subtitle)

@blueprint.route('/createaccount', methods=['POST'])
def createaccount():
    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    return resp
    #return flask.redirect(flask.url_for('login.loginscreen'))

#@blueprint.route('/')
#def index():
#    submit = flask.request.get('type')
#    if submit == 'Create Account':
#        return flask.redirect(flask.url_for('login.loginscreen'))
#    else:
#        return flask.redirect(flask.url_for('intro.introscreen'))