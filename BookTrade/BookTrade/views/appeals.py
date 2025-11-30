from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import db  # 自定义数据库操作包

# 创建申诉功能的 Blueprint
ac = Blueprint("appeal", __name__)


# ----------------------------------------------------------------
# 用户端功能
# ----------------------------------------------------------------

# 1. 用户提交申诉
@ac.route('/submit_appeal', methods=["GET", "POST"])
def submit_appeal():
    # 鉴权：确保用户已登录
    
    user_info = session.get("user_info")

    if request.method == "GET":
        # 获取URL参数中的订单ID（如果是从订单列表点击“申诉”过来的）
        order_id = request.args.get("order_id", "")
        return render_template("appeal_submit.html", order_id=order_id)

    # 处理 POST 请求
    user_id = user_info["id"]
    order_id = request.form.get("order_id")
    order_id = int(order_id) if order_id.isdigit() else None  # 转为整数，非数字则为None
    content = request.form.get("content")

    # 简单校验
    if not content:
        return render_template("appeal_submit.html", error="申诉内容不能为空", order_id=order_id)

    try:
        # 插入申诉记录
        # 注意：这里假设 db.execute_write 支持这种参数传递方式
        sql = "INSERT INTO appeals (user_id, order_id, content, status, create_time) VALUES (%s, %s, %s, '待处理', NOW())"
        db.execute_write(sql, [user_id, order_id, content])

        # 提交成功后，跳转到我的申诉列表
        return redirect("/appeal/my_appeals")
    except Exception as e:
        print(f"Error: {e}")
        return render_template("appeal_submit.html", error="提交失败，请稍后重试", order_id=order_id)


# 2. 用户查看自己的申诉历史
@ac.route('/my_appeals', methods=["GET"])
def my_appeals():
    user_info = session.get("user_info")

    user_id = user_info["id"]

    # 查询该用户的所有申诉
    # 假设 db.fetch_all 存在，如果你的 utils 只有 fetch_one，你需要实现 fetch_all
    sql = "SELECT * FROM appeals WHERE user_id = %s ORDER BY create_time DESC"
    # 这里假设你有一个 fetch_all 方法，如果没有，请在 utils.db 中添加
    appeals_list = db.fetch_all(sql, [user_id])

    return render_template("appeal_list.html", appeals=appeals_list)


# ----------------------------------------------------------------
# 管理员端功能
# ----------------------------------------------------------------

# 3. 管理员查看及处理申诉
@ac.route('/manager_appeal_list', methods=["GET"])
def manager_appeal_list():
    user_info = session.get("user_info")

    # 获取筛选状态，默认显示待处理
    status_filter = request.args.get("status", "待处理")
    #单独处理想要查看全部的请求
    if status_filter == "all":
        sql = "SELECT a.*, u.name as user_name FROM appeals a LEFT JOIN user u ON a.user_id = u.Id ORDER BY a.create_time DESC"
        params = []
    else:
        #降序排序，最新提交的在最上面
        sql = "SELECT a.*, u.name as user_name FROM appeals a LEFT JOIN user u ON a.user_id = u.Id WHERE a.status = %s ORDER BY a.create_time DESC"
        params = [status_filter]

    appeals_list = db.fetch_all(sql, params)

    return render_template("admin_appeal_manage.html", appeals=appeals_list)


# 4. 管理员提交处理结果
@ac.route('/manager_handle_appeal', methods=["POST"])
def manager_handle_appeal():
    user_info = session.get("user_info")
    #增加展示申诉具体信息
    if request.method == "GET":
        appeal_id = request.args.get("appeal_id")
        sql = "SELECT * FROM appeals WHERE Id = %s"
        appeal = db.fetch_one(sql, [appeal_id])
        return render_template("admin_appeal_detail.html", appeal=appeal)
    # 获取管理员回复
    appeal_id = request.form.get("appeal_id")
    reply_content = request.form.get("reply", "").strip()
    action = request.form.get("action")

    # 补充校验：appeal_id 和 reply_content 不能为空
    if not appeal_id or not reply_content or not action:
        return "参数不完整", 400

    new_status = "已通过" if action == "已通过" else "已拒绝"

    try:
        sql = "UPDATE appeals SET reply = %s, status = %s WHERE Id = %s"
        db.execute_write(sql, [reply_content, new_status, appeal_id])
    except Exception as e:
        print(f"处理申诉失败：{e}")
        return "处理失败，请稍后重试", 500

    return redirect("/appeal/admin/list")