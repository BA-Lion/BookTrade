import pymysql
from pymysql import cursors
from dbutils.pooled_db import PooledDB
#建立数据库连接池，限制访问，避免数据库压力过大（多此一举，但就是要做）
POOL=PooledDB(
    creator=pymysql,
    maxconnections=100,
    mincached=4,
    maxcached=20,
    blocking=True,
    setsession=[],
    ping=0,

    host='113.44.77.78',port=3306,user='SW_developer1',passwd='d8D@8B_^34R',charset='utf8',db='softwareproject'
)
def fetch_one(sql,params):
    # 初始化连接和游标为None，以便在finally中安全检查
    conn = None
    cursor = None
    try:
        conn=POOL.connection()
        #从数据库中获取字典类型数据
        cursor=conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql,params)
        result=cursor.fetchone()
        cursor.close()
        conn.close()#将链接交还给连接池
        return result
    except Exception as e:
        # 打印异常信息，方便调试
        print(f"数据库查询出错:")
        print(f"SQL: {sql}")
        print(f"Params: {params}")
        print(f"Error: {e}")
        # 发生异常时返回None
        return None
    finally:
        # 确保游标和连接被关闭，即使发生异常
        if cursor:
            cursor.close()
        if conn:
            conn.close()  # 将链接交还给连接池

#可以获取所有符合条件数据的集成
def fetch_all(sql,params):
     # 初始化连接和游标为None，以便在finally中安全检查
    conn = None
    cursor = None
    try:
        conn=POOL.connection()
        #从数据库中获取字典类型数据
        cursor=conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql,params)
        result=cursor.fetchall()
        cursor.close()
        conn.close()#将链接交还给连接池
        return result
    except Exception as e:
        # 打印异常信息，方便调试
        print(f"数据库查询出错:")
        print(f"SQL: {sql}")
        print(f"Params: {params}")
        print(f"Error: {e}")
        # 发生异常时返回None
        return None
    finally:
        # 确保游标和连接被关闭，即使发生异常
        if cursor:
            cursor.close()
        if conn:
            conn.close()  # 将链接交还给连接池

def execute_write(sql, params):
    """
    执行数据库写入操作（INSERT, UPDATE, DELETE）
    :param sql: 写入操作的SQL语句（使用%s作为占位符）
    :param params: 与SQL语句中占位符对应的参数元组
    :return: 受影响的行数，如果执行失败返回0
    """
    conn = None
    cursor = None
    try:
        # 1. 从连接池获取连接
        conn = POOL.connection()
        
        # 2. 创建游标
        cursor = conn.cursor(cursor=cursors.DictCursor)
        
        # 3. 执行SQL语句
        # cursor.execute() 会返回受影响的行数
        affected_rows = cursor.execute(sql, params)
        
        # 4. 提交事务（这是写入操作必不可少的一步）
        conn.commit()
        
        # 如果是插入操作，返回最新自增主键
        if sql.strip().upper().startswith("INSERT"):
            return cursor.lastrowid  # 返回最新自增主键
        else:
            return affected_rows#返回受影响的行数

    except Exception as e:
        # 6. 如果发生异常，打印错误信息并回滚事务
        print(f"数据库写入出错:")
        print(f"SQL: {sql}")
        print(f"Params: {params}")
        print(f"Error: {e}")
        
        # 重要：发生错误时必须回滚，否则事务会一直占用资源
        if conn:
            conn.rollback()
            
        # 失败时返回0
        return 0

    finally:
        # 7. 确保游标和连接被关闭，归还给连接池
        if cursor:
            cursor.close()
        if conn:
            conn.close()