# ==============================================================================
# Scene:      SourcesOfOriginality
# Source:     videos/_2018/wallis.py (lines 197-387)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SourcesOfOriginality.py SourcesOfOriginality -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import AmbientLight
from once_useful_constructs.light import Lighthouse
from once_useful_constructs.light import SwitchOn

# CHANGE: inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
from once_useful_constructs.light import inverse_power_law
DEFAULT_OPACITY_FUNCTION = inverse_power_law(1, 1.5, 1, 4)


class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


class SourcesOfOriginality(TeacherStudentsScene):
    def construct(self):
        self.mention_excitement()
        self.break_down_value_of_math_presentations()
        self.where_we_fit_in()

    def mention_excitement(self):
        self.teacher_says(
            "This one came about \\\\ a bit differently...",
            target_mode="speaking",
            run_time=1
        )
        self.play_student_changes("happy", "confused", "erm")
        self.wait(2)

    def break_down_value_of_math_presentations(self):
        title = OldTexText("The value of a", "math", "presentation")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        value_of, math, presentation = title

        MATH_COLOR = YELLOW
        COMMUNICATION_COLOR = BLUE

        big_rect = self.big_rect = Rectangle(
            width=title.get_width() + 2 * MED_LARGE_BUFF,
            height=3.5,
            color=WHITE
        )
        big_rect.next_to(title, DOWN)

        left_rect, right_rect = self.left_rect, self.right_rect = [
            Rectangle(
                height=big_rect.get_height() - 2 * SMALL_BUFF,
                width=0.5 * big_rect.get_width() - 2 * SMALL_BUFF,
                color=color
            )
            for color in (MATH_COLOR, COMMUNICATION_COLOR)
        ]
        right_rect.flip()
        left_rect.next_to(big_rect.get_left(), RIGHT, SMALL_BUFF)
        right_rect.next_to(big_rect.get_right(), LEFT, SMALL_BUFF)

        underlying_math = OldTexText("Underlying", "math")
        underlying_math.set_color(MATH_COLOR)
        communication = OldTexText("Communication")
        communication.set_color(COMMUNICATION_COLOR)
        VGroup(underlying_math, communication).scale(0.75)
        underlying_math.next_to(left_rect.get_top(), DOWN, SMALL_BUFF)
        communication.next_to(right_rect.get_top(), DOWN, SMALL_BUFF)

        formula = OldTex(
            "\\sum_{n = 1}^\\infty \\frac{1}{n^2} = \\frac{\\pi^2}{2}",
        )
        formula.scale(0.75)
        formula.next_to(underlying_math, DOWN)

        based_on_wastlund = OldTexText(
            "Previous video based on\\\\",
            "a paper by Johan W\\\"{a}stlund"
        )
        based_on_wastlund.set_width(
            left_rect.get_width() - MED_SMALL_BUFF)
        based_on_wastlund.next_to(formula, DOWN, MED_LARGE_BUFF)

        communication_parts = OldTexText("Visuals, narrative, etc.")
        communication_parts.scale(0.75)
        communication_parts.next_to(communication, DOWN, MED_LARGE_BUFF)
        lighthouse = Lighthouse(height=0.5)
        lighthouse.next_to(communication_parts, DOWN, LARGE_BUFF)
        ambient_light = AmbientLight(
            num_levels=200,
            radius=5,
            opacity_function=DEFAULT_OPACITY_FUNCTION,
        )
        ambient_light.move_source_to(lighthouse.get_top())

        big_rect.save_state()
        big_rect.stretch(0, 1)
        big_rect.stretch(0.5, 0)
        big_rect.move_to(title)

        self.play(
            FadeInFromDown(title),
            RemovePiCreatureBubble(
                self.teacher,
                target_mode="raise_right_hand",
                look_at=title,
            ),
            self.change_students(
                *["pondering"] * 3,
                look_at=title
            )
        )
        self.play(big_rect.restore)
        self.play(*list(map(ShowCreation, [left_rect, right_rect])))
        self.wait()
        self.play(
            math.match_color, left_rect,
            ReplacementTransform(VGroup(math.copy()), underlying_math)
        )
        self.play(FadeIn(formula))
        self.play(
            presentation.match_color, right_rect,
            ReplacementTransform(presentation.copy(), communication)
        )
        self.play(
            FadeIn(communication_parts),
            FadeIn(lighthouse),
            SwitchOn(ambient_light)
        )
        self.play(self.teacher.change, "tease")
        self.wait()

        self.play(
            FadeIn(based_on_wastlund),
            self.change_students(
                "sassy", "erm", "plain",
                look_at=based_on_wastlund
            ),
        )
        self.wait()

        self.math_content = VGroup(formula, based_on_wastlund)

    def where_we_fit_in(self):
        right_rect = self.right_rect
        left_rect = self.left_rect

        points = [
            right_rect.get_left() + SMALL_BUFF * RIGHT,
            right_rect.get_corner(UL),
            right_rect.get_corner(UR),
            right_rect.get_right() + SMALL_BUFF * LEFT,
            right_rect.get_corner(DR),
            right_rect.get_bottom() + SMALL_BUFF * UP,
            right_rect.get_corner(DL),
        ]
        added_points = [
            left_rect.get_bottom(),
            left_rect.get_corner(DL),
            left_rect.get_corner(DL) + 1.25 * UP,
            left_rect.get_bottom() + 1.25 * UP,
        ]

        blob1, blob2 = VMobject(), VMobject()
        blob1.set_points_smoothly(points + [points[0]])
        blob1.append_points(3 * len(added_points) * [points[0]])
        blob2.set_points_smoothly(points + added_points + [points[0]])
        for blob in blob1, blob2:
            blob.set_stroke(width=0)
            blob.set_fill(BLUE, opacity=0.5)

        our_contribution = OldTexText("Our target \\\\ contribution")
        our_contribution.scale(0.75)
        our_contribution.to_corner(UR)
        arrow = Arrow(
            our_contribution.get_bottom(),
            right_rect.get_right() + MED_LARGE_BUFF * LEFT,
            color=BLUE
        )

        wallis_product = get_wallis_product(n_terms=4)
        wallis_product.set_width(
            left_rect.get_width() - 2 * MED_LARGE_BUFF)
        wallis_product.move_to(self.math_content, UP)
        wallis_product_name = OldTexText("``Wallis product''")
        wallis_product_name.scale(0.75)
        wallis_product_name.next_to(wallis_product, DOWN, MED_SMALL_BUFF)

        new_proof = OldTexText("New proof")
        new_proof.next_to(wallis_product_name, DOWN, MED_LARGE_BUFF)

        self.play(
            DrawBorderThenFill(blob1),
            Write(our_contribution),
            GrowArrow(arrow),
        )
        self.wait(2)
        self.play(FadeOut(self.math_content))
        self.play(
            FadeIn(wallis_product),
            Write(wallis_product_name, run_time=1)
        )
        self.wait(2)
        self.play(
            Transform(blob1, blob2, path_arc=-90 * DEGREES),
            FadeIn(new_proof),
            self.teacher.change, "hooray",
        )
        self.play_all_student_changes("hooray", look_at=new_proof)
        self.wait(5)
