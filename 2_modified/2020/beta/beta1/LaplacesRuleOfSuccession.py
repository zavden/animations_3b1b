# ==============================================================================
# Scene:      LaplacesRuleOfSuccession
# Source:     videos/_2020/beta/beta1.py (lines 613-919)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl LaplacesRuleOfSuccession.py LaplacesRuleOfSuccession -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - smooth(t, inflection) no longer accepts the second argument; the old sigmoid is written in the lambda
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


def get_checks_and_crosses(bools, width=12):
    result = VGroup()
    for positive in bools:
        if positive:
            mob = OldTex(CMARK_TEX)
            mob.set_color(GREEN)
        else:
            mob = OldTex(XMARK_TEX)
            mob.set_color(RED)
        mob.positive = positive
        mob.set_width(0.5)
        result.add(mob)
    result.arrange(RIGHT, buff=MED_SMALL_BUFF)
    result.set_width(width)
    return result


def get_underlines(marks):
    underlines = VGroup()
    for mark in marks:
        underlines.add(Underline(mark))
    for line in underlines:
        line.align_to(underlines[-1], DOWN)
    return underlines



# ----- From _2020/beta/beta1.py -----

class LaplacesRuleOfSuccession(Scene):
    def construct(self):
        # Setup
        title = OldTexText("How to read a rating")
        title.set_height(0.75)
        title.to_edge(UP)
        underline = Underline(title)
        underline.scale(1.2)
        self.add(title, underline)

        data = get_checks_and_crosses(11 * [True] + [False], width=10)
        data.shift(DOWN)
        underlines = get_underlines(data)

        real_data = data[:10]
        fake_data = data[10:]

        def get_review_label(num, denom):
            result = VGroup(
                Integer(num, color=GREEN),
                OldTexText("out of"),
                Integer(denom),
            )
            result.arrange(RIGHT)
            result.set_height(0.6)
            return result

        review_label = get_review_label(10, 10)
        review_label.next_to(data[:10], UP, MED_LARGE_BUFF)

        # Show initial review
        self.add(review_label)
        self.add(underlines[:10])

        self.play(
            ShowIncreasingSubsets(real_data, int_func=np.ceil),
            CountInFrom(review_label[0], 0),
            # CHANGE: smooth(t, inflection) no longer accepts the second argument; the old sigmoid is written in the lambda
            rate_func=lambda t: np.clip((1 / (1 + np.exp(-3 * (t - 0.5))) - 1 / (1 + np.exp(1.5))) / (1 - 2 / (1 + np.exp(1.5))), 0, 1),
        )
        self.wait()

        # Fake data
        fd_rect = SurroundingRectangle(VGroup(fake_data, underlines[10:]))
        fd_rect.set_stroke(WHITE, 2)
        fd_rect.set_fill(GREY_E, 1)

        fd_label = OldTexText("Pretend you see\\\\two more")
        fd_label.next_to(fd_rect, DOWN)
        fd_label.shift_onto_screen()

        self.play(
            FadeIn(fd_label, UP),
            DrawBorderThenFill(fd_rect),
            ShowCreation(underlines[10:])
        )
        self.wait()
        for mark in data[10:]:
            self.play(Write(mark))
        self.wait()

        # Update rating
        review_center = VectorizedPoint(review_label.get_center())
        pretend_label = OldTexText("Pretend that it's")
        pretend_label.match_width(review_label)
        pretend_label.next_to(review_label, UP, MED_LARGE_BUFF)
        pretend_label.match_x(data)
        pretend_label.set_color(BLUE_D)

        old_review_label = VGroup(Integer(0), OldTexText("out of"), Integer(0))
        old_review_label.become(review_label)

        self.add(old_review_label, review_label)
        self.play(
            review_center.set_x, data.get_center()[0],
            MaintainPositionRelativeTo(review_label, review_center),
            UpdateFromAlphaFunc(
                review_label[0],
                lambda m, a: m.set_value(int(interpolate(10, 11, a)))
            ),
            UpdateFromAlphaFunc(
                review_label[2],
                lambda m, a: m.set_value(int(interpolate(10, 12, a)))
            ),
            FadeIn(pretend_label, LEFT),
            old_review_label.scale, 0.5,
            old_review_label.set_opacity, 0.5,
            old_review_label.to_edge, LEFT,
        )
        self.wait()

        # Show fraction
        eq = OldTex(
            "{11", "\\over", "12}",
            "\\approx", "91.7\\%"
        )
        fix_percent(eq[-1][-1])
        eq.set_color_by_tex("11", GREEN)

        eq.next_to(pretend_label, RIGHT)
        eq.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        self.play(Write(eq))
        self.wait()
        self.play(ShowCreationThenFadeAround(eq))
        self.wait()

        # Remove clutter
        old_review_label.generate_target()
        old_review_label.target.next_to(title, DOWN, LARGE_BUFF)
        old_review_label.target.to_edge(LEFT)
        old_review_label.target.set_opacity(1)
        arrow = Vector(0.5 * RIGHT)
        arrow.next_to(old_review_label.target, RIGHT)

        self.play(
            MoveToTarget(old_review_label),
            FadeIn(arrow),
            eq.next_to, arrow, RIGHT,
            FadeOut(
                VGroup(
                    fake_data,
                    underlines,
                    pretend_label,
                    review_label,
                    fd_rect, fd_label,
                ),
                DOWN,
                lag_ratio=0.01,
            ),
            real_data.match_width, old_review_label.target,
            real_data.next_to, old_review_label.target, DOWN,
        )
        self.wait()

        # Show 48 of 50 case
        # Largely copied from above...not great
        data = get_checks_and_crosses(
            48 * [True] + 2 * [False] + [True, False],
            width=FRAME_WIDTH - 1,
        )
        data.shift(DOWN)
        underlines = get_underlines(data)

        review_label = get_review_label(48, 50)
        review_label.next_to(data, UP, MED_LARGE_BUFF)

        true_data = data[:-2]
        fake_data = data[-2:]

        fd_rect.replace(fake_data, stretch=True)
        fd_rect.stretch(1.2, 0)
        fd_rect.stretch(2.2, 1)
        fd_rect.shift(0.025 * DOWN)
        fd_label.next_to(fd_rect, DOWN, LARGE_BUFF)
        fd_label.shift_onto_screen()
        fd_arrow = Arrow(fd_label.get_top(), fd_rect.get_corner(DL))

        self.play(
            FadeIn(underlines[:-2]),
            ShowIncreasingSubsets(true_data, int_func=np.ceil),
            CountInFrom(review_label[0], 0),
            UpdateFromAlphaFunc(
                review_label,
                lambda m, a: m.set_opacity(a),
            ),
        )
        self.wait()
        self.play(
            FadeIn(fd_label),
            GrowArrow(fd_arrow),
            FadeIn(fd_rect),
            Write(fake_data),
            Write(underlines[-2:]),
        )
        self.wait()

        # Pretend it's 49 / 52
        old_review_label = VGroup(Integer(0), OldTexText("out of"), Integer(0))
        old_review_label.become(review_label)
        review_center = VectorizedPoint(review_label.get_center())

        self.play(
            review_center.set_x, data.get_center()[0] + 3,
            MaintainPositionRelativeTo(review_label, review_center),
            UpdateFromAlphaFunc(
                review_label[0],
                lambda m, a: m.set_value(int(interpolate(48, 49, a)))
            ),
            UpdateFromAlphaFunc(
                review_label[2],
                lambda m, a: m.set_value(int(interpolate(50, 52, a)))
            ),
            old_review_label.scale, 0.5,
            old_review_label.to_edge, LEFT,
        )
        self.wait()

        arrow2 = Vector(0.5 * RIGHT)
        arrow2.next_to(old_review_label, RIGHT)

        eq2 = OldTex(
            "{49", "\\over", "52}",
            "\\approx", "94.2\\%"
        )
        fix_percent(eq2[-1][-1])
        eq2[0].set_color(GREEN)
        eq2.next_to(arrow2, RIGHT)
        eq2.save_state()
        eq2[1].set_opacity(0)
        eq2[3:].set_opacity(0)
        eq2[0].replace(review_label[0])
        eq2[2].replace(review_label[2])

        self.play(
            Restore(eq2, run_time=1.5),
            FadeIn(arrow2),
        )
        self.wait()

        faders = VGroup(
            fd_rect, fd_arrow, fd_label,
            fake_data, underlines,
            review_label,
        )
        self.play(
            FadeOut(faders),
            true_data.match_width, old_review_label,
            true_data.next_to, old_review_label, DOWN,
        )

        # 200 review case
        final_review_label = get_review_label(186, 200)
        final_review_label.match_height(old_review_label)
        final_review_label.move_to(old_review_label, LEFT)
        final_review_label.shift(
            arrow2.get_center() -
            arrow.get_center()
        )

        data = get_checks_and_crosses([True] * 186 + [False] * 14 + [True, False])
        data[:200].arrange_in_grid(10, 20, buff=0)
        data[-2:].next_to(data[:200], DOWN, buff=0)
        data.set_width(FRAME_WIDTH / 2 - 1)
        data.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        data.to_edge(DOWN)
        for mark in data:
            mark.scale(0.5)

        true_data = data[:-2]
        fake_data = data[-2:]

        self.play(
            UpdateFromAlphaFunc(
                final_review_label,
                lambda m, a: m.set_opacity(a),
            ),
            CountInFrom(final_review_label[0], 0),
            ShowIncreasingSubsets(true_data),
        )
        self.wait()

        arrow3 = Vector(0.5 * RIGHT)
        arrow3.next_to(final_review_label, RIGHT)

        eq3 = OldTex(
            "{187", "\\over", "202}",
            "\\approx", "92.6\\%"
        )
        fix_percent(eq3[-1][-1])
        eq3[0].set_color(GREEN)
        eq3.next_to(arrow3, RIGHT)

        self.play(
            GrowArrow(arrow3),
            FadeIn(eq3),
            Write(fake_data)
        )
        self.wait()
        self.play(
            true_data.match_width, final_review_label,
            true_data.next_to, final_review_label, DOWN,
            FadeOut(fake_data)
        )
        self.wait()

        # Make a selection
        rect = SurroundingRectangle(VGroup(eq2, old_review_label))
        rect.set_stroke(YELLOW, 2)

        self.play(
            ShowCreation(rect),
            eq2[-1].set_color, YELLOW,
        )
        self.wait()

        # Retitle
        name = OldTexText("Laplace's rule of succession")
        name.match_height(title)
        name.move_to(title)
        name.set_color(TEAL)

        self.play(
            FadeInFromDown(name),
            FadeOut(title, UP),
            underline.match_width, name,
        )
        self.wait()
