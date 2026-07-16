from flask import Flask
from sqlalchemy import select

from watchlist.settings import config
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.models import User
from watchlist.extensions import db, login_manager
from watchlist.errors import register_errors
from watchlist.commands import register_commands


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册错误处理函数和命令
    register_errors(app)
    register_commands(app)

    # 注册上下文处理函数
    @app.context_processor
    def inject_user():  # 函数名可以随意修改
        user = db.session.execute(select(User)).scalar()
        return dict(user=user)

    return app
