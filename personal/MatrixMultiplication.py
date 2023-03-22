import numpy as np
from manim import *


class MatrixMultiplication(Scene):
    left_matrix = [[1, 2], [3, 4]]
    right_matrix = [[5, 6], [7, 8]]
    use_parens = True

    def construct(self):
        left_string_matrix, right_string_matrix = [
            np.array(matrix).astype("str")
            for matrix in (self.left_matrix, self.right_matrix)
        ]
        if right_string_matrix.shape[0] != left_string_matrix.shape[1]:
            raise Exception("Incompatible shapes for matrix multiplication")

        left = Matrix(left_string_matrix)
        right = Matrix(right_string_matrix)
        result = self.get_result_matrix(left_string_matrix, right_string_matrix)

        self.organize_matrices(left, right, result)
        self.animate_product(left, right, result)

    def get_result_matrix(self, left, right):
        left_matrix, right_matrix = left, right
        (m, k), n = left_matrix.shape, right_matrix.shape[1]
        mob_matrix = np.empty((m, n), dtype=object)

        for a in range(m):
            for b in range(n):
                template = "(%s)(%s)" if self.use_parens else "%s%s"
                parts = [
                    MathTex(prefix + template % (left_matrix[a][c], right_matrix[c][b]))
                    for c in range(k)
                    for prefix in ["" if c == 0 else "+"]
                ]
                mob_matrix[a][b] = VGroup(*parts).arrange(RIGHT)

        A = MobjectMatrix(mob_matrix, v_buff=2, h_buff=4)
        return A

    def organize_matrices(self, left, right, result):
        equals = Tex("=")
        everything = VGroup(left, right, equals, result).arrange(RIGHT)
        self.add(everything)

    def animate_product(self, left, right, result):
        l_matrix = left.get_mob_matrix()
        r_matrix = right.get_mob_matrix()
        result_matrix = result.get_mob_matrix()
        circle = Circle(radius=l_matrix[0][0].height, color=GREEN)
        circles = VGroup(
            *[entry.get_point_mobject() for entry in (l_matrix[0][0], r_matrix[0][0])]
        )
        m, k, n = len(l_matrix), len(l_matrix[0]), len(r_matrix[0])

        for i in range(m):
            for j in range(n):
                result_matrix[i][j].set_color(BLACK)

        for i in range(m):
            for j in range(n):
                for c in range(k):
                    l_matrix[i][c].set_color(YELLOW)
                    r_matrix[c][j].set_color(YELLOW)

                for c in range(k):
                    start_parts = VGroup(l_matrix[i][c].copy(), r_matrix[c][j].copy())
                    result_entry = result_matrix[i][j].split()[c]

                    new_circles = VGroup(
                        *[
                            circle.copy().move_to(part.get_center())
                            for part in start_parts
                        ]
                    )
                    self.play(Transform(circles, new_circles))
                    self.play(
                        ReplacementTransform(
                            start_parts,
                            result_entry.copy().set_color(YELLOW),
                            path_arc=-np.pi / 2,
                            lag_ratio=0,
                        ),
                        run_time=0.5,
                    )
                    result_entry.set_color(YELLOW)
                    self.remove(start_parts)

                for c in range(k):
                    l_matrix[i][c].set_color(WHITE)
                    r_matrix[c][j].set_color(WHITE)

        self.play(FadeOut(circles))
        self.wait()
