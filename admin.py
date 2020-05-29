from app import app
from app import db
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from models import *


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class InventoryModelView(ModelView):
    can_delete = True
    page_size = 50
    column_searchable_list = ['domen', 'wap', 'web']


class FormModelView(ModelView):
    inline_models = (Xpath, )


class XpathModelView(ModelView):
    inline_models = (Param, )


# class HomeAdminView(AdminMixin, AdminIndexView):
# 	pass
#
#
# class PostAdminView(AdminMixin, BaseModelView):
# 	form_columns = ['title', 'body']
#
#
# class UserAdminView(AdminMixin, ModelView):
# 	pass
#
#
# class RoleAdminView(AdminMixin, ModelView):
# 	pass


admin = Admin(app, 'FlaskApp', template_mode='bootstrap3', url='/', index_view=AdminIndexView(name="Home"))
admin.add_view(FormModelView(Form, db.session))
admin.add_view(ModelView(Input, db.session))
admin.add_view(InventoryModelView(Inventory, db.session))
admin.add_view(ModelView(SurfTask, db.session))
admin.add_view(XpathModelView(Xpath, db.session))
admin.add_view(ModelView(Param, db.session))
