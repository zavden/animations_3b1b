# ==============================================================================
# Scene:      ThisIsAFootnote
# Source:     videos/_2019/bayes/footnote.py (lines 29-127)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/bayes/part1.py
#
# Run from this folder:
#     manimgl ThisIsAFootnote.py ThisIsAFootnote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


# ----- From _2019/bayes/part1.py -----

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


def get_bayes_formula(expand_denominator=False):
    t2c = {
        "{H}": HYPOTHESIS_COLOR,
        "{\\neg H}": NOT_HYPOTHESIS_COLOR,
        "{E}": EVIDENCE_COLOR1,
    }
    isolate = ["P", "\\over", "=", "\\cdot", "+"]

    tex = "P({H} | {E}) = {P({H}) P({E} | {H}) \\over "
    if expand_denominator:
        tex += "P({H}) P({E} | {H}) + P({\\neg H}) \\cdot P({E} | {\\neg H})}"
    else:
        tex += "P({E})}"

    formula = OldTex(
        tex,
        tex_to_color_map=t2c,
        isolate=isolate,
    )

    # CHANGE: identify the probabilities by their LaTeX parts, without Cairo glyph indices that do
    # not match the OldTex groups of GL.
    starts = [i for i, part in enumerate(formula) if part.get_tex().strip() == "P"]

    def probability(index):
        start = starts[index]
        end = start + 1
        while end < len(formula) and ")" not in formula[end].get_tex():
            end += 1
        return formula[start:end + 1]

    formula.posterior = probability(0)
    formula.prior = probability(1)
    formula.likelihood = probability(2)
    if expand_denominator:
        formula.denom_prior = probability(3)
        formula.denom_likelihood = probability(4)
        formula.denom_anti_prior = probability(5)
        formula.denom_anti_likelihood = probability(6)
    else:
        formula.p_evidence = probability(3)

    return formula



# ----- From _2019/bayes/footnote.py -----

def get_bayes_formula():
    return OldTex(
        "P(A|B) = {P(A)P(B|A) \\over P(B)}",
        tex_to_color_map={
            "A": YELLOW,
            "B": BLUE,
        },
        isolate=list("P(|)")
    )


class ThisIsAFootnote(TeacherStudentsScene):
    def construct(self):
        image = ImageMobject("bayes_thumbnail")
        image.set_height(2.5)
        rect = SurroundingRectangle(image, buff=0)
        rect.set_stroke(WHITE, 3)
        title = OldTexText("Bayes' theorem")
        title.match_width(image)
        title.next_to(image, UP)

        image_group = Group(rect, image, title)
        image_group.to_corner(UL)

        asterisk = OldTexText("*")
        asterisk.set_height(0.5)
        asterisk.set_stroke(BLACK, 3, background=True)
        asterisk.move_to(image.get_corner(UR), LEFT)

        formula = get_bayes_formula()
        formula.move_to(self.hold_up_spot, DOWN)

        pab = formula[:6]
        eq = formula[6]
        pa = formula[7:11]
        pba = formula[11:17]
        over = formula[17]
        pb = formula[18:23]

        # Show main video
        self.play(
            FadeInFromDown(image_group),
            self.change_students(
                "pondering", "hooray", "tease",
                look_at=image
            )
        )
        self.play(
            Write(asterisk),
            self.teacher.change, "speaking",
        )
        self.play(
            self.change_students(
                "thinking", "erm", "thinking"
            )
        )
        self.wait(3)
        self.play(
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(formula),
            self.change_students(*3 * ["pondering"])
        )
        self.wait()

        # Rearrange
        parts = VGroup(
            pb, pab, eq, pa, pba,
        )
        parts.generate_target()
        parts.target.arrange(RIGHT, buff=SMALL_BUFF)
        parts.target.move_to(self.hold_up_spot)

        self.play(
            MoveToTarget(parts, path_arc=-30 * DEGREES),
            FadeOut(over),
            self.teacher.change, "pondering",
        )
        self.wait()

        # Move to top
        p_both = OldTex(
            "P(A \\text{ and } B)",
            tex_to_color_map={"A": YELLOW, "B": BLUE},
        )
        eq2 = OldTex("=")
        full_equation = VGroup(
            pb, pab, eq, p_both, eq2, pa, pba
        )
        full_equation.generate_target()
        full_equation.target.arrange(RIGHT, buff=SMALL_BUFF)
        full_equation.target.set_width(FRAME_WIDTH - 1)
        full_equation.target.center()
        full_equation.target.to_edge(UP)

        p_both.set_opacity(0)
        p_both.scale(0.2)
        p_both.move_to(eq)
        eq2.move_to(eq)

        self.play(
            MoveToTarget(full_equation),
            FadeOut(image_group, 2 * LEFT),
            FadeOut(asterisk, 2 * LEFT),
            self.teacher.look_at, 4 * UP,
            self.change_students(
                "thinking", "erm", "confused",
                look_at=4 * UP
            )
        )
        self.wait(2)
