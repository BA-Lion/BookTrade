from flask import Blueprint,request,render_template,redirect,session
from BookTrade.utils import db#自定义数据库操作包

ac=Blueprint("buyer",__name__)
#直接在商品详情页调用，向该api发送post请求
@ac.route('/buy',methods=["GET","POST"])
def buy():
    user_info=session.get("user_info")
    book_id=request.form.get("book_id")
    book_dict=db.fetch_one("select * from book where book_id=%s",[book_id])


    #将book中的status状态更新为待确认
    db.execute_write("update book set status='待确认' where book_id=%s",[book_id])
    #将未完全确认的订单加到order表
    db.execute_write("insert into order (buyer_id,book_id,seller_id,total_amount,order_status) " \
    "values(%s,%s,%s,%s,%s)",[user_info["id"],book_id,book_dict["seller_id"],book_dict["price"],"待卖家未确认"])
    return redirect("/my_order")

@ac.route('/my_order',methods=["GET","POST"])
def my_order():
    user_info=session.get("user_info")
    order_list=db.fetch_all("select * from order where buyer_id=%s",[user_info["id"]])
    return render_template("my_order.html",order_list=order_list)
    
   