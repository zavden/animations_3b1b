# ==============================================================================
# Scene:      ShowDotProduct
# Source:     videos/_2018/div_curl.py (lines 3477-3527)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDotProduct.py ShowDotProduct -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDotProduct(MovingCameraScene):
    CONFIG = {
        "prod_tex": "\\cdot"
    }

    def construct(self):
        plane = NumberPlane()
        v1 = Vector(RIGHT, color=BLUE)
        v2 = Vector(UP, color=YELLOW)

        dot_product = OldTex(
            "\\vec{\\textbf{v}}", self.prod_tex,
            "\\vec{\\textbf{w}}", "="
        )
        dot_product.set_color_by_tex_to_color_map({
            "textbf{v}": BLUE,
            "textbf{w}": YELLOW,
        })
        dot_product.add_background_rectangle()
        dot_product.next_to(2.25 * UP, RIGHT)
        dot_product_value = DecimalNumber(
            1.0,
            include_background_rectangle=True,
        )
        dot_product_value.next_to(dot_product)
        dot_product_value_update = ContinualChangingDecimal(
            dot_product_value,
            lambda a: self.get_product(v1, v2),
            include_background_rectangle=True,
        )

        self.camera_frame.set_height(4)
        self.camera_frame.move_to(DL, DL)
        self.add(plane)
        self.add(dot_product, dot_product_value_update)
        self.add_additional_continual_animations(v1, v2)
        self.add_foreground_mobjects(v1, v2)
        for n in range(5):
            self.play(
                Rotate(v1, 45 * DEGREES, about_point=ORIGIN),
                Rotate(v2, -45 * DEGREES, about_point=ORIGIN),
                run_time=3,
                rate_func=there_and_back
            )
            self.wait(0.5)

    def get_product(self, v1, v2):
        return np.dot(v1.get_vector(), v2.get_vector())

    def add_additional_continual_animations(self, v1, v2):
        pass
