import Preprocessing as ps
from LinearProgrammingSolver import *
import numpy as np
import pandas as pd
import streamlit as st



if __name__ == "__main__":
    st.title("Chương trình giải bài toán Quy hoạch tuyến tính")
    student = pd.DataFrame({"Họ và Tên": ["Jack_97", "Lý Vĩnh Thuận"], "MSSV": ["Number1-deptrai", "22280092"], "Lớp": ["22KDL1", "22KDL1"]})
    student.index = [1, 2]
    st.table(student)
    soBien = st.text_input('Mời bạn nhập số biến:', placeholder = "4")
    soRangBuoc = st.text_input('Mời bạn nhập số ràng buộc:', placeholder = "2")
    

    st.markdown("<u>Cách nhập hàm mục tiêu:</u>", unsafe_allow_html = True)
    st.caption("$min / max$ $z = c^Tx$", unsafe_allow_html = True)
    st.caption("- Nhập **'min'** hoặc **'max'** cho hàm mục tiêu trước.")
    opt=st.text_input('Mời bạn nhập min hoặc max cho hàm mục tiêu:', placeholder ="min")
    st.caption("- Nhập hệ số đi kèm với biến xuất hiện trong hàm mục tiêu ( với hệ số dương ta chỉ cần nhập **số nguyên**, còn hệ số âm ta nhập thêm dấu **-**).", unsafe_allow_html=True)
    st.caption("Ví dụ: Nếu muốn nhập hàm mục tiêu là 5x1 + 4x2 +0x3 + 0x4 ta nhập như sau: 5 4 0 0")
    hamMucTieu = st.text_input('Mời bạn nhập hàm mục tiêu: ', placeholder = "5 4 0 0")


    st.markdown("<u>Cách nhập ràng buộc:</u>", unsafe_allow_html = True)
    st.caption("$a_i x \leq b_i, i \epsilon M_1$", unsafe_allow_html = True)
    st.caption("$a_i x \geq b_i, i \epsilon M_2$", unsafe_allow_html = True)
    st.caption("$a_i x = b_i, i \epsilon M_3$", unsafe_allow_html = True)
    st.caption("- Nhập hệ số đi kèm với biến xuất hiện trong hàm mục tiêu ( với hệ số dương ta chỉ cần nhập **số nguyên**, còn hệ số âm ta nhập thêm dấu **-**).")
    st.caption("- Nhập các phần tử cách nhau một khoảng trắng rồi nhập dấu của ràng buộc.")
    st.caption("- Mỗi ràng buộc nhập trên một dòng.")
    st.caption("Ví dụ cần nhập ràng buộc là x1 + x2 - x3 = 1 ta nhập như sau: 1 1 -1 0 = 1")
    txt = st.text_area('Mời nhập các ràng buộc:', placeholder = """1 1 -1 0 =1
1 -1 0 -1 = 5""")

    st.markdown("<u>Cách nhập ràng buộc về dấu: </u>", unsafe_allow_html = True)
    st.caption("$x_j \geq 0, j \epsilon M_1$", unsafe_allow_html = True)
    st.caption("$x_j \leq 0, j \epsilon M_2$", unsafe_allow_html = True)
    st.caption("$x_j$ tự do, $j \epsilon M_3$", unsafe_allow_html = True)
    st.caption("- Nhập từng ràng buộc về dấu trên từng dòng.")
    st.caption("- Nếu biến đó tự do thì không cần nhập ràng buộc về dấu.")
    st.caption("Ví dụ cần nhập ràng buộc dấu là x1 >= 0 ,x2 >= 0, x3 >= 0, x4 tùy ý ta nhập như sau:  >= >= >= f ")
    txt1 = st.text_area('Mời nhập các ràng buộc về dấu:', placeholder = """>= >= >= f""")
    # st.caption(">Nếu biến $x_i$ là biến tự do, kết quả trả về sẽ là hai biến $x_i^+$ và $x_i^-$. Để tìm $x_i$, ta tính toán: $x_i$ = $x_i^+$ - $x_i^-$", unsafe_allow_html = True)
    # st.caption(">Nếu tồn tại biến $x_i \leq 0$, kết quả trả về sẽ là $x_i^*$. Ta tính toán $x_i$ = $-x_i^*$ ", unsafe_allow_html = True)
    
    st.write("<u>Click vào nút dưới đây để thực hiện giải bài toán:</u>", unsafe_allow_html = True)
    if st.button('Solve'):
        # Lấy dữ liệu từ collection dựa trên ID
        #Convert các dữ liệu
        preprocessor = ps.Preprocessing(opt=opt,objective=hamMucTieu,bounds=txt1,constr=txt)
        objective_converted = preprocessor.convert_objective()
        lhs, rhs=preprocessor.convert_constraints()
        bounds_convert=preprocessor.convert_bounds()
        print("objective:",objective_converted)
        #Tiến hành giải
        LNProgramming = LinearProgrammingSolver(objective=objective_converted, lhs=lhs, rhs=rhs, bounds=bounds_convert, num_var=int(soBien), opt=opt)
        solution=LNProgramming.solve_lp()
        st.write("\n\nGiải pháp tối ưu:")
        st.write("  Giá trị mục tiêu:", solution.fun)
        st.write("  Giá trị của vector biến tối ưu:", solution.x)
        st.write("  Trạng thái:", solution.message)
        st.write("  Số bước lặp:", solution.nit)  # Sửa đổi này
        st.write("\nRàng buộc:")
    else:
        st.write("Không tìm thấy dữ liệu trong collection.")
