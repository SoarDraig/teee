import streamlit as st
import pyodbc

# 云数据库连接函数
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=rm-xxxxx.sqlserver.rds.aliyuncs.com,1433;"  # 替换为你的 SQL Server 地址
        "DATABASE=InventorySystem;"
        "UID=admin;"  # 替换为你的数据库账号
        "PWD=your_password;"  # 替换为你的密码
    )

# 应用标题
st.title("进销存管理系统")

# 插入库存功能
st.header("插入库存")
product_id = st.text_input("商品编号")
product_name = st.text_input("商品名称")
supplier_name = st.text_input("供应商名称")
quantity = st.number_input("数量", min_value=0, step=1)

if st.button("插入库存"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO 库存表 (商品编号, 商品名称, 供应商名称, 数量) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (product_id, product_name, supplier_name, quantity))
        conn.commit()
        st.success("库存插入成功！")
    except pyodbc.IntegrityError:
        st.error("插入失败，可能是商品编号重复。")
    except Exception as e:
        st.error(f"发生错误：{e}")
    finally:
        conn.close()

# 查看库存功能
st.header("查看库存")
if st.button("刷新库存列表"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM 库存表"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                st.write(f"商品编号: {row[0]}, 商品名称: {row[1]}, 供应商: {row[2]}, 数量: {row[3]}")
        else:
            st.warning("暂无库存信息。")
    except Exception as e:
        st.error(f"发生错误：{e}")
    finally:
        conn.close()
