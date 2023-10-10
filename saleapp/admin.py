from saleapp import db, app,utils
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product, User, UserRole
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
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
    def index(self):
        return self.render('admin/stats.html',stats=utils.product_stats())


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.product_count_by_cate()
        return self.render('admin/index.html',stats=stats)


admin = Admin(app=app, name="Khai Nghiem", template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(AuthenticatedModelView(User, db.session, name='Nguoi dung'))
admin.add_view(LogoutView(name='Dang xuat'))
admin.add_view(StatsView(name='Thong ke bao cao'))
