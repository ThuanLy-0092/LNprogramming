import numpy as np
class Preprocessing:
    def __init__(self, opt=None, objective=None, bounds=None, constr=None):
        self.opt = opt
        self.objective = objective
        self.bounds = bounds
        self.constr = constr

    def convert_objective(self):
        self.objective= self.objective.split()
        if self.opt == "min":
            return [float(val) for val in self.objective]
        elif self.opt == "max":
            return [float(val) * -1 for val in self.objective]

    def convert_bounds(self):
        converted_bounds = []
        self.bounds =self.bounds.split()
        for bound in self.bounds:
            if bound == '>=':
                converted_bounds.append((0, None))
            elif bound == '<=':
                converted_bounds.append((None, 0))
            elif bound == 'f':
                converted_bounds.append((None, None))
        return converted_bounds

    def convert_constraints(self):
        lhs_matrix = []
        rhs_vector = []
        constraints = self.constr.split('\n')
        constraints1=[]
        for constr in constraints:
            if constr:
                # Chuỗi ràng buộc
                # Chuẩn hóa
                constr = constr.strip()  # Loại bỏ khoảng trắng ở đầu và cuối chuỗi
                constr = ' '.join(constr.split())  # Thay thế mọi khoảng trắng nhiều lần liên tiếp bằng một khoảng trắng duy nhất

                # Tiếp tục với việc tách chuỗi constraint thành các phần tử riêng biệt
                constraint_parts = constr.split()

                sign = constraint_parts[-2]
                
                # Chuyển đổi các phần tử trong constraint thành số thực
                constraint_values = [float(val) if val != sign else val for val in constraint_parts]
                
                constraints1.append(constraint_values)
        
        for cons in constraints1:
            sign = cons[-2]
            rhs = cons[-1]
            lhs = cons[:-2]
            if sign == "<=":
                lhs_matrix.append(lhs)
                rhs_vector.append(rhs)
            elif sign == ">=":
                lhs_matrix.append([-1 * float(x) for x in lhs])
                rhs_vector.append(-1*float(rhs))
            elif sign == "=":
                lhs_matrix.append(lhs)
                rhs_vector.append(rhs)
                lhs_matrix.append([-1 * float(x) for x in lhs])
                rhs_vector.append(-1*float(rhs))

        return np.array(lhs_matrix, dtype=float), np.array(rhs_vector, dtype=float)
