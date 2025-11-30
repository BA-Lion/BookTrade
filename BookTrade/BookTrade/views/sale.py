from flask import Blueprint,request,render_template,redirect,session
from utils import db#自定义数据库操作包

#买书操作集成
ac=Blueprint("sale",__name__)

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
    category_list=request.form.getlist("category")
    for category in category_list:
        db.execute_write("insert into book_category (book_id,category_id) values(%s,%s)",[new_book_id,category])
    return redirect("/my_sale_record")


#用户查看自己的出售书籍信息
@ac.route('/my_sale_record',methods=["GET","POST"])
def my_onsale_book():
    user_info=session.get("user_info")
    seller_id=user_info["id"]
    on_sale_list=db.fetch_all("select * from book where seller_id=%s and status='在售'",[seller_id])
    wait_to_deal_list=db.fetch_all("select * from book where seller_id=%s and status='在售'",[seller_id])
    already_sell_list=db.fetch_all("select * from book where seller_id=%s and status='已售出'",[seller_id])
    book_list={"on_sale":on_sale_list,"wait_to_sell":wait_to_deal_list,"already_sell":already_sell_list}
    #向前端返回自己在售数据
    return render_template("my_onsale_book.html",book_list=book_list)

#确认交易
@ac.route('/deal_trade',methods=["GET","POST"])
def confirm_trade():
    book_id=request.form.get("book_id")
    choice=request.form.get("choice")
    if choice=="yes":
       #将order中的状态改为卖家已确认
       db.execute_write("update order_record set order_status='卖家已确认' where book_id=%s",[book_id])
       #将book从book_category表中删除
       db.execute_write("delete from book_category where book_id=%s",[book_id])
      #将book的状态改为'已售出'
       db.execute_write("update book set status='已售出' where book_id=%s",[book_id])
    else:
        #将该order从库中删除
        db.execute_write("delete from order_record where book_id=%s",[book_id])
        #将书籍状态重新置为在售
        db.execute_write("update book set status='在售' where book_id=%s",[book_id])
    return redirect("/my_sale_record")

    
    
    
    
