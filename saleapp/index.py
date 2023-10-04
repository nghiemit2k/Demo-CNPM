import math

from flask import render_template, request
from saleapp import app
import utils
from saleapp.admin import *


@app.route("/")
def index():
    cates = utils.read_categories()
    page = request.args.get('page', 1)
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    products = utils.read_products(kw=kw, cate_id=cate_id, page=int(page))
    counter = utils.count_products()
    return render_template("index.html", categories=cates, products=products,
                           pages=math.ceil(counter / app.config['PAGE_SIZE']))


@app.route("/products")
def product_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    # if kw:
    #     kq = []
    #     for u in products:
    #         if u['name'].lower().find(kw.lower()) >= 0:
    #             kq.append(u)
    #     products = kq
    return render_template("products.html", products=products)


@app.route("/register", methods=['get', 'post'])
def user_register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
