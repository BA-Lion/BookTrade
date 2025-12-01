from flask import Blueprint,request,render_template,redirect,session
from utils import db#自定义数据库操作包

ac=Blueprint("seller_right",__name__)
#向管理员申请卖家权限
@ac.route('/apply_to_be_seller',methods=["GET","POST"])
def apply_to_be_seller():
    #获取post请求
    user_info=session.get("user_info")
    application_desc=request.form.get("application_desc")
    user_id=user_info["id"]
    #写入seller_application表
    db.execute_write("insert into seller_application (user_id,application_desc) values(%s,%s)",[user_id,application_desc])
    return redirect("/")

@ac.route('/appliacation_status',methods=["GET","POST"])
def application_status():
    #从数据库中获取申请状态
    user_info=session.get("user_info")
    user_id=user_info["id"]
    application_list=db.fetch_one("select * from seller_application where user_id=%s",[user_id])
    return render_template("application_status.html",application_list=application_list)#返回字典

#管理员处理申请
@ac.route('/application_list',methods=["GET","POST"])
def application_list():
    #从数据库中获取待审核的申请
    wait_to_deal_list=db.fetch_all("select * from seller_application where audit_status='待审核'",[])
    #从数据库中获取已处理的该账号已处理的申请
    user_info=session.get("user_info")
    user_id=user_info["id"]
    already_deal_list=db.fetch_all("select * from seller_application where audit_status in('已驳回','已通过') and user_id=%s",[user_id])
    #传回两个列表，分别为待处理的申请和已处理的申请
    return render_template("application_list.html",wait_to_deal_list=wait_to_deal_list,already_deal_list=already_deal_list)

@ac.route('/deal_application',methods=["GET","POST"])
def deal_application():
    #获取当前管理员id
    user_info=session.get("user_info")
    user_id=user_info["id"]
    
    #通过前端发送的post请求，获取待处理的申请的id，管理员的处理决定，与处理理由
    application_id=request.form.get("application_id")
    audit_status=request.form.get("audit_status")
    audit_opinion=request.form.get("audit_opinion")
    #写入seller_application表,同时将处理时间更新为当前时间
    db.execute_write("update seller_application set audit_status=%s,audit_opinion=%s,audit_time=now() where appliecation_id=%s",[audit_status,audit_opinion,application_id])
    if audit_status=="已通过":
        #将申请人的权限改为卖家
        buyer_id=db.fetch_one("select user_id from seller_application where application_id=%s",[application_id])
        db.execute_write("update user set role=2 where id=%s",[buyer_id])
    return redirect("/application_list")
    
    

