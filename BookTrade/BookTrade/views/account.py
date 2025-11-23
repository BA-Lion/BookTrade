from flask import Blueprint,request,render_template,redirect
from utils import db#自定义数据库操作包

ac=Blueprint("account",__name__)


#登陆功能
@ac.route('/login',methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")#报错太难受了，仅为示例，引号位置应写上实际前端登陆界面的html文件名称
    #点击登陆按钮，即为发送post请求
    #一定要修改html文件与以下两行适配，发送的post请求一定要对应名称account，password
    account=request.form.get("account")
    password=request.form.get("password")
    user_dict=db.fetch_one("select * from user where Account=%s and Password=%s",[account,password])
    if user_dict:
        #登录成功，后端跳转至应用初始界面，还没做，以“登陆成功做测试”
        return "登陆成功"
    #失败
    return render_template("login.html",error="用户名或密码错误")

#前端登陆界面跳转到注册界面后，记得向向regist API发送请求，其他和登陆类似
@ac.route('/regist',methods=["GET","POST"])
def regist():
    if request.method=="GET":
        return render_template("regist.html")
    account=request.form.get("account")
    password=request.form.get("password")
    #账号密码为空，不允许注册
    if account and password:
        db.execute_write("insert into user (Account,Password,role) values(%s,%s,1)",[account,password])

        #成功后，后端自动返回'/login' api，前端做相应提示，并返回登陆界面，下一行代码可以优化
        return redirect("/login")
    return render_template("regist.html",error="账号密码不符合规范")