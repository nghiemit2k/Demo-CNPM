from flask import render_template,request
from saleapp import app
import utils

@app.route("/")
def index():
    cates = utils.read_categories()
    return render_template("index.html",categories =cates)
@app.route("/products")
def product_list():
    cate_id = request.args.get("category_id")
    products = utils.read_products(cate_id=cate_id)

    return render_template("products.html", products =products)

if __name__ == '__main__':
    app.run(debug=True)