from flask import Blueprint, render_template, request, session, redirect,url_for, current_app
from app.models.messages import Messages, SetForm, GetForm

pages = Blueprint('pages', __name__)


@pages.route('/set_lang/<string:language>')
def set_language(language):
    if language not in current_app.config['LANGUAGES']:
        language = 'en'
    session['language'] = language
    return redirect(url_for('pages.index'))

@pages.route('/')
def index():
    setform = SetForm()
    getform = GetForm()
    return render_template('index.html', setform = setform, getform=getform)


@pages.route('/set', methods=['POST'])
def set():
    setform = SetForm()
    if setform.validate_on_submit():
        text = setform.message.data
        secret = setform.secret.data
        print(text, secret)
    else:
        print(setform.errors)
    h = Messages.set(text, secret)
    return render_template('set.html', hash=h)


@pages.route('/get', methods=['POST'])
def get():
    getform = GetForm()
    if getform.validate_on_submit():
        h = getform.hash.data
        secret = getform.secret.data
    else:
        print(getform.errors)
    m = Messages.get(h, secret)
    return render_template('get.html', message=m)