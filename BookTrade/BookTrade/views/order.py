from flask import Blueprint,request,render_template,redirect,session
from utils import db#自定义数据库操作包

ac=Blueprint("order",__name__)

@ac.route('/seller_put_conduct',methods=["GET","POST"])
def seller_put_conduct():
    if request.method=="GET":
        #像前端传递书籍分类信息,希望前端做出标签供用户选择
        category_list=db.fetch_all("select name from category",[])
        return render_template("seller_put_conductl",category_dict=category_list)
    #获取售卖书籍信息
    user_info=session.get("user_info")
    book_name=request.form.get("book_name")
    author=request.form.get("author")
    condition=request.form.get("condition")
    price=request.form.get("price")
    description=request.form.get("description")
    seller_id=user_info["id"]
    #先将书籍信息加入book表
    new_book_id=db.execute_write("insert into book (seller_id,name,author,condition,price,description) values(%s,%s,%s,%s,%s,%s)",[seller_id,book_name,author,condition,price,description])
    #再将书籍分类信息加入book_category表
    category_list=request.form.get("category")
    for category in category_list:
        db.execute_write("insert into book_category (book_id,category_id) values(%s,%s)",[new_book_id,category])
    return redirect("/my_onsale_book")


#用户查看自己的出售书籍信息
@ac.route('/my_onsale_book',methods=["GET","POST"])
def my_onsale_book():
    user_info=session.get("user_info")
    seller_id=user_info["id"]
    book_list=db.fetch_all("select * from book where seller_id=%s",[seller_id])
    #向前端返回自己在售数据
    return render_template("my_onsale_book.html",book_list=book_list)


    
    
    
    
