import numpy as np
from scipy.optimize import linprog

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
            res = linprog(self.objective, A_ub=self.lhs, b_ub=self.rhs, bounds=self.bounds, method=method)
            self.solution = -res
            return res
        
    def display_solution(self):
        if self.solution is None:
            print("\nKhông tìm thấy giải pháp.")
        else:
            print("\n\nGiải pháp tối ưu:")
            print("  Giá trị mục tiêu:", self.solution.fun)
            print("  Giá trị của vector biến tối ưu:", self.solution.x)
            print("  Trạng thái:", self.solution.message)
            print("  Số bước lặp:", self.solution.nit)  # Sửa đổi này
            print("\nRàng buộc:")
            for i, (lhs, rhs) in enumerate(zip(self.lhs, self.rhs)):
                print(f"  Ràng buộc {i+1}: {lhs} <= {rhs}")
            print("\nHệ số của hàm mục tiêu:")
            for i, coef in enumerate(self.objective):
                print(f"  Hệ số cho x{i+1}: {coef}")

    def my_callback(self,xk, **kwargs):
        print("\nBước lặp:", xk.nit)
        print("Giá trị của vector biến tối ưu:", xk.x)
        print("Giá trị hàm mục tiêu:", xk.fun)