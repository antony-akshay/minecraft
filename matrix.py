import copy
import math

def copy_matrix(matrix):
    return copy.deepcopy(matrix)

clean_matrix = [[0.0] * 4 for _ in range(4)]
identity_matrix = copy_matrix(clean_matrix)

identity_matrix[0][0] = 1.0
identity_matrix[1][1] = 1.0
identity_matrix[2][2] = 1.0
identity_matrix[3][3] = 1.0

def multiply_matrices(x_matrix, y_matrix):
    result = copy_matrix(clean_matrix)
    for i in range(4):
        for j in range(4):
            result[i][j] = (
                x_matrix[0][j] * y_matrix[i][0] +
                x_matrix[1][j] * y_matrix[i][1] +
                x_matrix[2][j] * y_matrix[i][2] +
                x_matrix[3][j] * y_matrix[i][3]
            )
    return result

class Matrix:
    def __init__(self, base=None):
        if isinstance(base, Matrix):
            self.data = copy_matrix(base.data)
        elif isinstance(base, list):
            self.data = copy_matrix(base)
        else:
            self.data = copy_matrix(clean_matrix)

    def load_identity(self):
        self.data = copy_matrix(identity_matrix)

    def __mul__(self, other):
        return Matrix(multiply_matrices(self.data, other.data))

    def translate(self, x, y, z):
        for i in range(4):
            self.data[3][i] += (
                self.data[0][i] * x +
                self.data[1][i] * y +
                self.data[2][i] * z
            )

    def rotate(self, angle, x, y, z):
        magnitude = math.sqrt(x * x + y * y + z * z)
        x /= -magnitude
        y /= -magnitude
        z /= -magnitude

        s = math.sin(angle)
        c = math.cos(angle)
        oc = 1.0 - c

        rot = copy_matrix(identity_matrix)
        rot[0][0] = oc * x * x + c
        rot[0][1] = oc * x * y - z * s
        rot[0][2] = oc * x * z + y * s

        rot[1][0] = oc * y * x + z * s
        rot[1][1] = oc * y * y + c
        rot[1][2] = oc * y * z - x * s

        rot[2][0] = oc * z * x - y * s
        rot[2][1] = oc * z * y + x * s
        rot[2][2] = oc * z * z + c

        self.data = multiply_matrices(self.data, rot)

    def rotate_2d(self, x, y):
        self.rotate(x, 0, 1, 0)
        self.rotate(-y, math.cos(x), 0, math.sin(x))

    def perspective(self, fov, aspect, near, far):
        ymax = near * math.tan(math.radians(fov) / 2)
        xmax = ymax * aspect
        self.frustum(-xmax, xmax, -ymax, ymax, near, far)

    def frustum(self, left, right, bottom, top, near, far):
        self.data = copy_matrix(clean_matrix)
        self.data[0][0] = (2 * near) / (right - left)
        self.data[1][1] = (2 * near) / (top - bottom)
        self.data[2][0] = (right + left) / (right - left)
        self.data[2][1] = (top + bottom) / (top - bottom)
        self.data[2][2] = -(far + near) / (far - near)
        self.data[2][3] = -1
        self.data[3][2] = -(2 * far * near) / (far - near)
