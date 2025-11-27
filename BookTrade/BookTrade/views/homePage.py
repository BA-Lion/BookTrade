from flask import Blueprint,request,render_template,redirect,sessions
from utils import db#自定义数据库操作包

ac=Blueprint("homePage",__name__)

#首页页面，定义根目录
@ac.route('/',methods=["GET","POST"])
def homePage():
    #获取书籍订单
    book_list=db.fetch_all("select * from book",[])
    user_info=sessions.get("user_info")
    if user_info:
        role_list=user_info
    #未登录无用户信息，即user_info为none

    #根据role得到具体身份信息
    role_dict={1:"普通用户",2:"普通用户",3:"管理员"}

    """以字典形式向前端传递书籍售卖信息,
        字典形式返回用户信息，由于权限以数字的形式展现，故增加将数字转化为身份信息的字典
    """

    return render_template("homePage.html",book_list=book_list,role_list=role_list,role_dict=role_dict)


