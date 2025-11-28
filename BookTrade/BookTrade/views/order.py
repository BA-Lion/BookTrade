from flask import Blueprint,request,render_template,redirect,session
from utils import db#自定义数据库操作包

ac=Blueprint("order",__name__)

@ac.route('/seller_put_conduct',methods=["GET","POST"])
def seller_put_conduct():
    if request.method=="GET":
        return render_template("seller_put_conductl")
    #获取售卖书籍信息
    user_info=session.get("user_info")
    book_name=request.form.get("book_name")
    author=request.form.get("author")
    condition=request.form.get("condition")
    price=request.form.get("price")
    description=request.form.get("description")
    seller_id=user_info["id"]
    #处理图书分类
    name=
    #将售卖书籍放入数据库
    db.execute_write("insert into book (Account,Password,role,name) values(%s,%s,1,%s)")
    
    
    
