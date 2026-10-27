from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User, Role
from ..email import send_email, send_simple_message
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            role = Role.query.filter_by(name='User').first()
            if role is None:  # se a função ainda não existe no banco, cria
                role = Role(name='User')
                db.session.add(role)
            user = User(username=form.name.data, role=role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            print('FLASKY_ADMIN: ' + str(current_app.config['FLASKY_ADMIN']), flush=True)
            if current_app.config['FLASKY_ADMIN']:
                #send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
                print('Enviando mensagem...', flush=True)
                resposta = send_simple_message([form.email.data, current_app.config['FLASKY_ADMIN'], "flaskaulasweb@zohomail.com"], 'Novo usuário', form.name.data)
                if resposta.status_code == 200:
                    flash('E-mail enviado para ' + form.email.data + '.')
                else:
                    flash('O e-mail ' + form.email.data + ' aguarda autorização para receber mensagens.')
                print('Mensagem enviada...', flush=True)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    pessoas = User.query.all()

    return render_template('index.html',
                           form=form, name=session.get('name'), pessoas=pessoas,
                           known=session.get('known', False))