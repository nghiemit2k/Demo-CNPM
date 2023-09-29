import json
import os.path

from saleapp import app
from saleapp.models import Category, Product


def read_json(path):
    with open(path) as f:
        return json.load(f)


def read_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, "data/categories.json"))


def read_products(cate_id=None,kw = None,from_price =None,to_price=None):
    # products = read_json(os.path.join(app.root_path, "data/products.json"))
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    # return products
    products = Product.query
    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(float(from_price)))
    if to_price:
        products = products.filter(Product.price.__le__(float(to_price)))
    return products.all()
