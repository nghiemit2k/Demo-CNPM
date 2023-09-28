import json
import os.path

from saleapp import app
def read_json(path):
    with open(path) as f:
       return json.load(f)
def read_categories():
    return read_json(os.path.join(app.root_path,"data/categories.json"))

def read_products(cate_id=None):
    products= read_json(os.path.join(app.root_path,"data/products.json"))
    if cate_id:
        products = [p for p in products if p['category_id']==int(cate_id)]
    return products