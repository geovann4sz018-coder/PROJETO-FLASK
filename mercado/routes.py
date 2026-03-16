from mercado import app 
from flask import render_template, redirect, url_for, flash
from mercado.models import Item, User
from mercado.forms import CadastroForm, LoginForm
from mercado import db
from flask_login import login_user, logout_user, login_required
import stripe
import os
from dotenv import load_dotenv

# Só carrega .env se estiver local, Render já define variáveis
if os.environ.get("FLASK_ENV") == "development":
    load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def page_home():
    return render_template('home.html')


@app.route('/produtos')
@login_required
def page_produto():
    itens=Item.query.all()
    return render_template('produtos.html',itens =itens)

@app.route('/cadastro', methods=['GET', 'POST'])
def page_cadastro():
    form =CadastroForm()
    if form.validate_on_submit():
        usuario = User(
            usuario=form.usuario.data,
            email=form.email.data,
            senhacrip=form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_produto'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Erro ao cadastrar usuário {err}', category='danger')
    return render_template('cadastro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha1.data):
            login_user(usuario_logado)
            flash(f'Sucesso! Seu login é: {usuario_logado.usuario}', category='success')
            return redirect(url_for('page_produto'))
        else:
            flash(f'Usuário ou senha incorretos', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def page_logout():
    logout_user()
    flash("Você fez o logout com sucesso!", category='info')
    return redirect(url_for('page_home'))

@app.route('/comprar/<int:item_id>')
@login_required
def comprar(item_id):

    item = Item.query.get_or_404(item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'brl',
                'product_data': {
                    'name': item.nome,
                },
                'unit_amount': int(item.preco * 100), 
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('page_produto', _external=True),
        cancel_url=url_for('page_produto', _external=True),
    )

    return redirect(session.url)