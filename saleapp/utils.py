import json
import os.path
from flask import current_app
from saleapp import app, db
from saleapp.models import Category, Product, User,ReceiptDetail,Receipt
from flask_login import current_user
from sqlalchemy import func
import hashlib


def read_json(path):
    with open(path) as f:
        return json.load(f)


def read_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, "data/categories.json"))


def read_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    # products = read_json(os.path.join(app.root_path, "data/products.json"))
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    # return products
    products = Product.query.filter(Product.active.__eq__(True))
    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(float(from_price)))
    if to_price:
        products = products.filter(Product.price.__le__(float(to_price)))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return products.slice(start, end).all()


def add_user(name, username, password, **kwargs):
    if password is not None:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(), password=password, email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()

def check_login(username,password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),User.password.__eq__(password)).first()

def product_count_by_cate():
    return Category.query.join(Product, Product.category_id.__eq__(Category.id),isouter=True)\
        .add_columns(func.count(Product.id)).group_by(Category.id).all()

def product_stats(kw=None, from_date = None,to_date=None):
    p= db.session.query(Product.id,Product.name,func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
        .join(ReceiptDetail,ReceiptDetail.product_id.__eq__(Product.id),isouter=True)\
        .group_by(Product.id,Product.name)
    return p.all()

def cart_stats(cart):
    total_quantity,total_amount =0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']
    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,product_id=c['id'],
                              quantity = c['quantity'],unit_price=c['price'])
            db.session.add(d)

        db.session.commit()