import Preprocessing as ps
from LinearProgrammingSolver import *
import numpy as np
import pandas as pd
import streamlit as st

st.title("Chương trình giải bài toán Quy hoạch tuyến tính")
st.image("LN_Programming.jpg")
soBien = st.number_input('Mời bạn nhập số biến:', placeholder="4")
st.markdown("<u>Cách nhập hàm mục tiêu:</u>", unsafe_allow_html=True)
opt = st.selectbox('Chọn yêu cầu bài toán', ['min','max'])
st.caption("- Nhập hệ số đi kèm với biến xuất hiện trong hàm mục tiêu ( với hệ số dương ta chỉ cần nhập **số nguyên**, còn hệ số âm ta nhập thêm dấu **-**).", unsafe_allow_html=True)
st.caption("Ví dụ: Nếu muốn nhập hàm mục tiêu là 5x1 + 4x2 +0x3 + 0x4 ta nhập như sau: 5 4 0 0")
hamMucTieu = st.text_input('Mời bạn nhập hàm mục tiêu: ', placeholder="5 4 0 0")

st.markdown("<u>Cách nhập ràng buộc:</u>", unsafe_allow_html=True)
st.caption("- Nhập các phần tử cách nhau một khoảng trắng rồi nhập dấu của ràng buộc.")
st.caption("- Mỗi ràng buộc nhập trên một dòng.")
st.caption("Ví dụ cần nhập ràng buộc là x1 + x2 - x3 = 1 ta nhập như sau: 1 1 -1 0 = 1")
txt = st.text_area('Mời nhập các ràng buộc:', placeholder="""1 1 -1 0 =1
1 -1 0 -1 = 5""")

st.markdown("<u>Cách nhập ràng buộc về dấu: </u>", unsafe_allow_html=True)
st.caption("Ví dụ cần nhập ràng buộc dấu là x1 >= 0 ,x2 >= 0, x3 >= 0, x4 tùy ý ta nhập như sau:  >= >= >= f ")
txt1 = st.text_area('Mời nhập các ràng buộc về dấu:', placeholder=">= >= >= f")

st.write("<u>Click vào nút dưới đây để thực hiện giải bài toán:</u>", unsafe_allow_html=True)
if st.button('Solve'):
    # Lấy dữ liệu từ collection dựa trên ID
    # Convert các dữ liệu
    preprocessor = ps.Preprocessing(opt=opt, objective=hamMucTieu, bounds=txt1, constr=txt)
    objective_converted = preprocessor.convert_objective()
    lhs, rhs = preprocessor.convert_constraints()
    bounds_convert = preprocessor.convert_bounds()
    # Tiến hành giải
    LNProgramming = LinearProgrammingSolver(objective=objective_converted, lhs=lhs, rhs=rhs, bounds=bounds_convert, num_var=soBien, opt=opt)
    solution = LNProgramming.solve_lp()
    LNProgramming.display_solution()

