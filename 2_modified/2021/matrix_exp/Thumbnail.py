# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2021/matrix_exp.py (lines 6207-6232)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - Placeholder ExpMatThumbnailBackdrop.png (dark blue background) in _lib/assets/raster_images/ (make_matrix_exp_assets.py)
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


class Thumbnail(Scene):
    def construct(self):
        im = ImageMobject("ExpMatThumbnailBackdrop")
        im.set_height(FRAME_HEIGHT)
        im.set_opacity(0.7)
        self.add(im)

        # rect = FullScreenFadeRectangle()
        # rect.set_fill(opacity=0.3)
        # self.add(rect)

        exp = get_matrix_exponential([[-1, -1], [1, 0]], scalar_tex="")
        exp.set_height(5)
        exp.set_stroke(BLACK, 50, opacity=0.5, background=True)

        fuzz = VGroup()
        N = 100
        for w in np.linspace(150, 0, N):
            ec = exp.copy()
            ec.set_stroke(BLUE_E, width=w, opacity=(1 / N))
            ec.set_fill(opacity=0)
            fuzz.add(ec)

        self.add(fuzz, exp)

        self.embed()
