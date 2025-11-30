from flask import Flask,request,session,redirect,render_template

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
        #未登录
        if not user_info:
            return redirect('/login')
        elif user_info['role']>1:
            return
        else:
            return redirect('/apply_to_be_seller')
    if request.path=='/my_sale_record':
        #未登录
        if not user_info:
            return redirect('/login')
        #是买家
        elif user_info['role']>1:
            return
        #未有权限
        else:
            return redirect('/apply_to_be_seller')
    if request.path=='/submit_appeal':
        if not user_info:
            return redirect('/login')
        return
    if request.path=='/my_appeals':
        if not user_info:
            return redirect('/login')
        return
    if request.path=='/manager_appeal_list':
        if not user_info:
            return redirect('/login')
        #是管理员，不拦截
        elif user_info['role']==3:
            return
        #不是管理员，首页
        else:
            return render_template("homePage.html",error="权限不足")
        
    if request.path=='/manager_book_list':
        #未登录
        if not user_info:
            return redirect('/login')
        #是管理员，不拦截
        elif user_info['role']==3:
            return
        #不是管理员，首页
        else:
            return render_template("homePage.html",error="权限不足")
        
    if request.path=='/buy':
        #未登录
        if not user_info:
            return redirect('/login')
        return
    if request.path=='/my_order':
        #未登录
        if not user_info:
            return redirect('/login')
        return



def create_app():
    app=Flask(__name__)
    #密钥
    app.secret_key='123456'
    app.before_request(auth)
    from .views import account
    from .views import homePage
    from .views import sale
    from .views import appeals
    #其他功能导包暂时省略

    #导入登陆相关api
    app.register_blueprint(account.ac)
    app.register_blueprint(homePage.ac)
    app.register_blueprint(sale.ac)
    app.register_blueprint(appeals.ac)

    return app