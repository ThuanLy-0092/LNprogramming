import numpy as np
from scipy.optimize import linprog
import streamlit as st
class LinearProgrammingSolver:

    def __init__(self, objective, lhs, rhs, bounds, num_var, opt):
        self.objective = np.array(objective)
        self.lhs = np.array(lhs)
        self.rhs = np.array(rhs)
        self.bounds = bounds
        self.solution = None
        self.num_var = num_var
        self.opt = opt

    def solve_lp(self):
        method = 'simplex' if self.num_var < 100 else 'highs'
        if self.opt == "min":
            res = linprog(self.objective, A_ub=self.lhs, b_ub=self.rhs, bounds=self.bounds, method=method,callback = self.my_callback)
            self.solution = res
            return res
        else:
            res = linprog(self.objective, A_ub=self.lhs, b_ub=self.rhs, bounds=self.bounds, method=method,callback=self.my_callback)
            self.solution = -res
            return -res
        
    def display_solution(self):
        if self.solution is None:
            st.header("\nKhông tìm thấy giải pháp.")
        else:
            st.header("\n\nGiải pháp tối ưu:")
            st.write("  Giá trị mục tiêu:", self.solution.fun)
            st.write("  Giá trị của vector biến tối ưu:", self.solution.x)
            st.write("  Trạng thái:", self.solution.message)
            st.write("  Số bước lặp:", self.solution.nit)  # Sửa đổi này
            st.write("\nRàng buộc:")
            for i, (lhs, rhs) in enumerate(zip(self.lhs, self.rhs)):
                st.write(f"  Ràng buộc {i+1}: {lhs} <= {rhs}")
            st.write("\nHệ số của hàm mục tiêu:")
            for i, coef in enumerate(self.objective):
                st.write(f"  Hệ số cho x{i+1}: {coef}")

    def my_callback(self, xk, **kwargs):
        st.write("\nBước lặp:", xk.nit)
        st.write("Giá trị của vector biến tối ưu:", xk.x)
        st.write("Giá trị hàm mục tiêu:", xk.fun)