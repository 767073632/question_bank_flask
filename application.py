import os

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy



class Application(Flask):
    def __init__(self, import_name,template_folder=None,static_folder=None):
        super(Application, self).__init__(import_name,template_folder=template_folder,static_folder=static_folder)
        self.config.from_pyfile('config/base_setting.py')
        if "ops_config" in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__,template_folder=os.getcwd()+'/web/templates',static_folder=os.getcwd()+'/web/static')
manager = Manager(app)
