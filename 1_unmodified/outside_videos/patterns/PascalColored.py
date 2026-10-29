# ==============================================================================
# Scene:      PascalColored
# Source:     videos/outside_videos/patterns.py (lines 4-81)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PascalColored.py PascalColored -w -m --fps 15
#
# Notes:
#   No published video: it takes more than an hour to render and it is only points; it was dropped from the final render (2026-10-24).
# ==============================================================================

from manim_imports_ext import *

class PascalColored(Scene):
    CONFIG = {
        "colors": [BLUE_E, BLUE_D, BLUE_B],
        "dot_radius": 0.16,
        "n_layers": 2 * 81,
        "rt_reduction_factor": 0.5,
    }

    def construct(self):
        max_height = 6
        rt = 1.0

        layers = self.get_dots(self.n_layers)
        triangle = VGroup(layers[0])
        triangle.to_edge(UP, buff=LARGE_BUFF)
        self.add(triangle)
        last_layer = layers[0]
        for layer in layers[1:]:
            height = last_layer.get_height()
            layer.set_height(height)
            layer.next_to(last_layer, DOWN, 0.3 * height)
            for i, dot in enumerate(layer):
                pre_dots = VGroup(*last_layer[max(i - 1, 0):i + 1])
                self.play(*[
                    ReplacementTransform(
                        pre_dot.copy(), dot,
                        run_time=rt
                    )
                    for pre_dot in pre_dots
                ])
            last_layer = layer
            triangle.add(layer)
            if triangle.get_height() > max_height:
                self.play(
                    triangle.set_height, 0.5 * max_height,
                    triangle.to_edge, UP, LARGE_BUFF
                )
                rt *= self.rt_reduction_factor
                print(rt)
        self.wait()

    def get_pascal_point(self, n, k):
        return n * rotate_vector(RIGHT, -2 * np.pi / 3) + k * RIGHT

    def get_dot_layer(self, n):
        n_to_mod = len(self.colors)
        dots = VGroup()
        for k in range(n + 1):
            point = self.get_pascal_point(n, k)
            # p[0] *= 2
            nCk_residue = choose(n, k) % n_to_mod
            dot = Dot(
                point,
                radius=2 * self.dot_radius,
                color=self.colors[nCk_residue]
            )
            if n <= 9:
                num = OldTex(str(nCk_residue))
                num.set_height(0.5 * dot.get_height())
                num.move_to(dot)
                dot.add(num)
            # num = DecimalNumber(choose(n, k), num_decimal_points = 0)
            # num.set_color(dot.get_color())
            # max_width = 2*dot.get_width()
            # max_height = dot.get_height()
            # if num.get_width() > max_width:
            #     num.set_width(max_width)
            # if num.get_height() > max_height:
            #     num.set_height(max_height)
            # num.move_to(dot, aligned_edge = DOWN)
            dots.add(dot)
        return dots

    def get_dots(self, n_layers):
        dots = VGroup()
        for n in range(n_layers + 1):
            dots.add(self.get_dot_layer(n))
        return dots
