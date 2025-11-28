from flask import Flask,request,session,redirect

#拦截器
def auth():
    #避免静态文件无法加载
    if request.path.startswith("/static"):
        return
    #登录不拦截
    if request.path=='/login':
        return
    #注册不拦截
    if request.path=='/regist':
        return
    user_info=session.get("user_info")
    #拦截非买家用户
    if request.path=='/seller_put_conduct':
        if user_info['role']>1:
            return
        return redirect('/login')



def create_app():
    app=Flask(__name__)
    app.before_request(auth)
    from .views import account
    from .views import homePage
    #其他功能导包暂时省略

    #导入登陆相关api
    app.register_blueprint(account.ac)
    app.register_blueprint(homePage.ac)

    return app