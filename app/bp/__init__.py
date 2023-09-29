from flask import Blueprint, render_template, request, session, redirect,url_for, current_app
from app.models.messages import Messages, SetForm, GetForm, MessageForm

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
    url = request.url_root
    return render_template('set.html', hash=h, url=url)


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

@pages.route('/message/<string:hash>', methods=['GET', 'POST'])
def message(hash):
    messageform = MessageForm()
    if request.method == 'POST':
        if messageform.validate_on_submit():
            secret = messageform.secret.data
            m = Messages.query.filter_by(hash=hash, secret=secret).first()
            if m:
                t = m.text
                m.delete()
                
                return render_template('message.html', messageform=messageform, message=t, status=2)
            else:
                return render_template('message.html', messageform=messageform, status=3)
        else:
            print(messageform.errors)
    
    m = Messages.query.filter_by(hash=hash).first()
    if m:
        return render_template('message.html', messageform=messageform, status=1)
    return render_template('message.html', messageform=messageform, status=3)