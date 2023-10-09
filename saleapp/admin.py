from saleapp import admin, db
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product, User
from flask_admin import BaseView,expose
from flask_login import logout_user,current_user
from flask import redirect
class ProductView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['name', 'price', 'category_id']

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

class StatsView(AuthenticatedBaseView):
    @expose('/')
    def inxex(self):
        return self.render('admin/stats.html')

admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(User,db.session, name='Nguoi dung'))
admin.add_view(LogoutView(name='Dang xuat'))
admin.add_view(StatsView(name='Thong ke bao cao'))