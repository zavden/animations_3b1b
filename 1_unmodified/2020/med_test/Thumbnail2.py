# ==============================================================================
# Scene:      Thumbnail2
# Source:     videos/_2020/med_test.py (lines 178-226)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail2.py Thumbnail2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail2(Scene):
    def construct(self):
        dots = Dot().get_grid(9 * 5, 16 * 5, buff=MED_LARGE_BUFF)
        dots.set_height(FRAME_HEIGHT)
        dots.set_color(GREY_D)
        VGroup(*random.sample(list(dots), 50)).set_fill(YELLOW, 1)
        # self.add(dots)

        title = Text("A better Bayes rule?")
        title.set_width(FRAME_WIDTH - 2)
        title.to_edge(UP, buff=1)
        title.set_stroke(BLACK, 25, background=True)
        self.add(title)

        formula = OldTex(
            "O(H | E)", "=", "O(H)", "{P(E | H) \\over P(E | \\neg H)",
            tex_to_color_map={"H": YELLOW, "E": BLUE}
        )
        formula.set_width(FRAME_WIDTH - 4)
        formula.set_y(-1)

        H = formula.get_part_by_tex("H")
        E = formula.get_part_by_tex("E")
        hyp_label = Text("Hypothesis", color=YELLOW, font_size=24)
        hyp_label.next_to(H, UP, buff=1).shift_onto_screen()
        ev_label = Text("Evidence", color=BLUE, font_size=24)
        ev_label.next_to(E, DOWN, buff=1)

        self.add(hyp_label, ev_label)
        self.add(Arrow(hyp_label, H, buff=0.1, color=YELLOW))
        self.add(Arrow(ev_label, E, buff=0.1, color=BLUE))

        p_rect = SurroundingRectangle(formula[6:9])
        p_rect.set_stroke(GREY_B, 2)
        p_label = Text("Prior")
        p_label.next_to(p_rect, UP)
        # self.add(p_rect, p_label)

        rect = SurroundingRectangle(formula[9:])
        rect.set_stroke(GREEN, 3)
        rect.set_fill(BLACK, 1)
        rect_label = Text("Bayes factor", color=GREEN)
        rect_label.match_width(rect)
        rect_label.next_to(rect, DOWN)

        self.add(BackgroundRectangle(formula[:9]))
        self.add(rect)
        self.add(rect_label)
        self.add(formula)
