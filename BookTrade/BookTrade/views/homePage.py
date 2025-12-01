from flask import Blueprint,request,render_template,redirect,session
from utils import db#自定义数据库操作包

ac=Blueprint("homePage",__name__)

#首页页面，定义根目录
@ac.route('/',methods=["GET","POST"])
def homePage():
    #获取书籍订单
    book_list=db.fetch_all("select * from book where status='在售",[])
    user_info=session.get("user_info")
    if user_info:
        role_list={"role":user_info["role"],"name":user_info["name"]}
    #未登录无用户信息，即user_info为none
    else:
        role_list=None
    #根据role得到具体身份信息
    role_dict={1:"普通用户",2:"普通用户",3:"管理员"}

    """以字典形式向前端传递书籍售卖信息,
        字典形式返回用户信息，由于权限以数字的形式展现，故增加将数字转化为身份信息的字典
    """

    return render_template("homePage.html",book_list=book_list,role_list=role_list,role_dict=role_dict)

@ac.route('/name_inquery',methods=["GET","POST"])
def inquery():
    #获取用户输入的书籍名称
    book_name=request.form.get("book_name","").strip()#去除首尾空格
    if not book_name:
        return redirect("/")
    sql = "select * from book where name LIKE %s and status='在售'"
    book_list = db.fetch_all(sql, [f"%{book_name}%"])  # 参数需用列表/元组包裹
    return render_template("inquery_page.html",book_list=book_list)

@ac.route('/category_inquery',methods=["GET","POST"])
def category_inquery():
    category_list=request.form.get("category","").strip()#去除首尾空格
    if not category_list:
        return redirect("/")
    
    # 处理分类ID列表（分割、转整数、过滤无效值）
    category_ids = []
    for cid in category_list.split(","):
        cid = cid.strip()
        if cid.isdigit():
            category_ids.append(int(cid))
    
    if not category_ids:
        return redirect("/")
    
    # 生成占位符（适配多个分类ID）
    placeholders = ", ".join(["%s"] * len(category_ids))
    # 修正SQL逻辑：子查询应关联book_id，而非category_id
    sql = f"""
        select * from book 
        where book_id in(select book_id from book_category where category_id in ({placeholders})) 
        and status='在售'
    """
    
    # 执行查询
    book_list = db.fetch_all(sql, category_ids)
    return render_template("inquery_page.html", book_list=book_list)
    

#书籍具体信息查看功能
@ac.route('/book_detail',methods=["GET","POST"])
def book_detail():
    book_id=request.form.get("book_id","").strip()#去除首尾空格
    book_dict=db.fetch_one("select * from book where id=%s",[book_id])
    return render_template("book_detail.html",book_dict=book_dict)

#返回书籍分类标签
@ac.route('/get_category',methods=["GET","POST"])
def get_category():
    category_list=db.fetch_all("select * from category",[])
    return (category_list)

#管理员管理分类
@ac.route('/manager_category',methods=["GET","POST"])
def manager_category():
    #获取处理信息
    operator=request.form.get("operator","")
    category_name=request.form.get("category_name","")
    if operator=="add":
        #添加到分类表中
        db.execute_write("insert into category (name) values(%s)",[category_name])
    if operator=="delete":
        #先获取category_id
        category_id=request.form.get("category_id","")
        #从book_category表中删除category_id对应的数据
        db.execute_write("delete from book_category where category_id=%s",[category_id])
        #从category表中删除category_id对应的数据
        db.execute_write("delete from category where category_id=%s",[category_id])
    return redirect("/")
        
    
    
    


