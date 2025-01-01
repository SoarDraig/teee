import streamlit as st
import pyodbc

# SQL Server 数据库连接
def get_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=your_server_address;'
                          'DATABASE=your_database_name;'
                          'UID=your_username;'
                          'PWD=your_password')
    return conn

# 插入库存功能
def insert_stock(product_id, product_name, supplier_name, quantity):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO 库存表 (商品编号, 商品名称, 供应商名称, 数量) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (product_id, product_name, supplier_name, quantity))
            conn.commit()
            st.success("库存插入成功！")
    except Exception as e:
        st.error(f"发生错误：{e}")
    finally:
        conn.close()

# 查看库存功能
def view_stock():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
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

# 标题
st.title("进销存管理系统")

# 插入库存功能
st.header("插入库存")
product_id = st.text_input("商品编号")
product_name = st.text_input("商品名称")
supplier_name = st.text_input("供应商名称")
quantity = st.number_input("数量", min_value=0, step=1)

if st.button("插入库存"):
    insert_stock(product_id, product_name, supplier_name, quantity)

# 查看库存功能
st.header("查看库存")
if st.button("刷新库存列表"):
    view_stock()

