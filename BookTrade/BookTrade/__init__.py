from flask import Flask

def create_app():
    app=Flask(__name__)
    from .views import account
    #其他功能导包暂时省略

    #导入登陆相关api
    app.register_blueprint(account.ac)

    return app