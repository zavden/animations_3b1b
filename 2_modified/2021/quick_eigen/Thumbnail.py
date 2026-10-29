# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2021/quick_eigen.py (lines 93-215)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix no longer has element_to_mobject_config; it is now element_config
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


def get_mod_mat(matrix, h_buff=1.3, v_buff=0.8, t2c={}):
    t2c["\\lambda"] = EIGEN_COLORS[1]
    mod_mat = Matrix(
        [
            [matrix[0][0] + " - \\lambda", matrix[0][1]],
            [matrix[1][0], matrix[1][1] + " - \\lambda"],
        ],
        # CHANGE: Matrix no longer has element_to_mobject_config; it is now element_config
        element_config={"tex_to_color_map": t2c},
        h_buff=h_buff,
        v_buff=v_buff,
    )
    return mod_mat


def get_det_mod_mat(mod_mat):
    parens = OldTex("(", ")")
    parens.stretch(2, 1)
    parens.match_height(mod_mat)
    parens[0].next_to(mod_mat, LEFT, SMALL_BUFF)
    parens[1].next_to(mod_mat, RIGHT, SMALL_BUFF)
    det = Text("det")
    det.next_to(parens, LEFT, SMALL_BUFF)
    return VGroup(det, parens, mod_mat)


def get_shadow(vmobject, width=50, n_copies=25):
    shadow = VGroup()
    for w in np.linspace(width, 0, n_copies):
        part = vmobject.copy()
        part.set_fill(opacity=0)
        part.set_stroke(BLACK, width=w, opacity=1.0 / width)
        shadow.add(part)
    return shadow


class Thumbnail(Scene):
    def construct(self):
        grid = NumberPlane(faded_line_ratio=0)
        grid.apply_matrix([[3, 1], [0, 2]])
        grid.set_opacity(0.5)
        self.add(grid)

        mat_mob = IntegerMatrix([[3, 1], [4, 3]], h_buff=0.8)
        mat_mob.set_height(3)
        mat_mob.add_to_back(BackgroundRectangle(mat_mob))
        mat_mob.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(mat_mob)

        a, b, c, d = mat_mob.get_entries()
        a_to_d = d.get_center() - a.get_center()
        rect = Rectangle(height=1, width=get_norm(a_to_d) + 1)
        rect.round_corners()
        rect.set_stroke(MEAN_COLOR, 3)
        rect.rotate(angle_of_vector(a_to_d))
        rect.move_to(VGroup(a, d))
        rect2 = rect.copy()
        rect2.set_color(PROD_COLOR)
        rect2.rotate(-2 * angle_of_vector(a_to_d))
        rect2.move_to(rect)

        dashed_rects = VGroup(
            DashedVMobject(rect.insert_n_curves(100), num_dashes=50),
            DashedVMobject(rect2.insert_n_curves(100), num_dashes=50),
        )

        self.add(dashed_rects)

        answer = OldTex(
            "\\lambda_1, \\lambda_2 = {3} \\pm \\sqrt{\\,{3}^2 - {5}} = 5, 1",
            tex_to_color_map={"{3}": MEAN_COLOR, "{p}": PROD_COLOR}
        )
        answer.add_background_rectangle()
        answer.set_width(12)
        answer.to_edge(DOWN)
        # answer.shift(SMALL_BUFF * UP)
        self.add(answer)

        # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
        arrow = FillArrow(mat_mob, answer, fill_color=YELLOW, thickness=0.15, buff=0.3)
        arrow.set_stroke(BLACK, 30, background=True)
        arrow.shift(0.2 * UP)
        self.add(arrow)

        return
        #old
        backdrop = ImageMobject("QuickEigenThumbnailBackdrop")
        backdrop.set_height(FRAME_HEIGHT)
        backdrop.set_opacity(0.5)
        self.add(backdrop)

        buff = 0.75
        det = get_det_mod_mat(get_mod_mat([["3", "1"], ["4", "1"]]))
        det.set_height(2.25)
        det.to_corner(UR, buff=buff)
        self.add(get_shadow(det), det)

        not_this = OldTexText("Not\\\\this")
        not_this.match_height(det)
        not_this.to_corner(UL, buff=buff)
        not_this.set_color(RED)
        self.add(not_this)

        kw = {
            "tex_to_color_map": {
                "\\lambda_1": EIGEN_COLORS[0],
                "\\lambda_2": EIGEN_COLORS[1],
                "M": YELLOW,
            }
        }
        facts = VGroup(
            OldTex("\\text{det}(M) = \\,\\, \\lambda_1 \\cdot \\lambda_2", **kw),
            OldTex("\\text{tr}(M) = \\lambda_1 + \\lambda_2", **kw),
        )
        facts.arrange(DOWN, buff=MED_SMALL_BUFF, index_of_submobject_to_align=2)
        facts.match_height(det)
        facts.match_x(det)
        facts.set_y(-det.get_y())
        self.add(get_shadow(facts), facts)

        use_these = OldTexText("Use\\\\these")
        use_these.match_height(not_this)
        use_these.to_corner(DL, buff=buff)
        use_these.set_color(BLUE)
        not_this.match_x(use_these)
        self.add(use_these)

        not_arrow = Arrow(not_this, det, fill_color=RED, thickness=0.1, buff=0.5)
        use_arrow = Arrow(use_these, facts, fill_color=BLUE, thickness=0.1, buff=0.5)
        self.add(get_shadow(not_arrow), not_arrow)
        self.add(get_shadow(use_arrow), use_arrow)

        ## DELETE
        # mp = OldTex(
        #     "{m} \\pm \\sqrt{\\,{m}^2 - {p}}",
        #     tex_to_color_map={
        #         "{m}": MEAN_COLOR,
        #         "{p}": MEAN_COLOR,
        #     }
        # )
        # for mob, u in [(det, -1), (mp, 1)]:
        #     mob.set_width(FRAME_WIDTH / 2 - 1)
        #     mob.set_x(u * FRAME_WIDTH / 4)
        #     mob.set_y(-1)

        # v_line = DashedLine(4 * UP, 4 * DOWN)

        # ex = Exmark()
        # check = Checkmark()
        # VGroup(ex, check).scale(5)
        # ex.move_to(det).to_edge(UP, LARGE_BUFF)
        # check.move_to(mp).to_edge(UP, LARGE_BUFF)

        # self.add(v_line)
        # self.add(det)
        # self.add(mp)
        # self.add(ex)
        # self.add(check)

        self.embed()
