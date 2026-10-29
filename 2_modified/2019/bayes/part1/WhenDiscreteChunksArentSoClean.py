# ==============================================================================
# Scene:      WhenDiscreteChunksArentSoClean
# Source:     videos/_2019/bayes/part1.py (lines 3681-3808)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WhenDiscreteChunksArentSoClean.py WhenDiscreteChunksArentSoClean -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Keep the column order and Cairo spacing in the grid so that the indices of people and cells correspond to the right region.
# ==============================================================================

from manim_imports_ext import *

class WhenDiscreteChunksArentSoClean(Scene):
    def construct(self):
        squares = VGroup(*[Square() for x in range(100)])
        # CHANGE: preserve Cairo column order and spacing for indexed grid members.
        cairo_arrange_in_grid(squares, n_cols=10, buff=0)
        squares.set_stroke(WHITE, 1)
        squares.set_fill(GREY_E, 1)
        squares.set_height(6)
        squares.to_edge(DOWN)

        target_p = 0.3612

        rain, sun = icon_templates = VGroup(
            SVGMobject("rain_cloud"),
            SVGMobject("sunny"),
        )
        for icon in icon_templates:
            icon.set_width(0.6 * squares[0].get_width())
            icon.set_stroke(width=0)
            icon.set_sheen(0.5, UL)
        rain.set_color(BLUE_E)
        sun.set_color(YELLOW)

        partial_rects = VGroup()
        icons = VGroup()
        q_marks = VGroup()
        for i, square in enumerate(squares):
            icon = rain.copy() if i < 40 else sun.copy()
            icon.move_to(square)
            icons.add(icon)

            partial_rect = square.copy()
            partial_rect.set_stroke(width=0)
            partial_rect.scale(0.95)
            partial_rect.stretch(
                0.4,
                0,
                about_edge=RIGHT
            )
            partial_rects.add(partial_rect)

            q_mark = OldTex("?")
            q_mark.replace(partial_rect, dim_to_match=0)
            q_mark.scale(0.8)
            q_marks.add(q_mark)

        p_label = VGroup(
            OldTex("P", "(", "\\text{Rain}", ")", "="),
            DecimalNumber(40, unit="\\%", num_decimal_places=2)
        )
        percentage = p_label[1]
        p_label.arrange(RIGHT)
        p_label.to_edge(UP)
        p_label[0].set_color_by_tex("Rain", BLUE)
        percentage.align_to(p_label[0][0], DOWN)

        alt_percentage = Integer(0, unit="\\%")
        alt_percentage.move_to(percentage, LEFT)

        self.add(squares)
        self.add(p_label[0])
        self.play(
            ChangeDecimalToValue(alt_percentage, 40),
            ShowIncreasingSubsets(icons[:40])
        )
        self.play(FadeIn(icons[40:]))
        self.wait()
        self.remove(alt_percentage)
        self.add(percentage)
        self.play(
            ChangeDecimalToValue(percentage, 100 * target_p),
            FadeIn(partial_rects[30:40]),
            FadeIn(q_marks[30:40], lag_ratio=0.3)
        )
        self.wait(2)

        l_rect = Rectangle(fill_color=BLUE_D)
        r_rect = Rectangle(fill_color=GREY_B)
        rects = VGroup(l_rect, r_rect)
        for rect, p in (l_rect, target_p), (r_rect, 1 - target_p):
            rect.set_height(squares.get_height())
            rect.set_width(p * squares.get_width(), stretch=True)
            rect.set_stroke(WHITE, 2)
            rect.set_fill(opacity=1)
        rects.arrange(RIGHT, buff=0)
        rects.move_to(squares)

        brace = Brace(l_rect, UP, buff=SMALL_BUFF)

        sun = icons[40].copy()
        rain = icons[0].copy()
        for mob, rect in [(rain, l_rect), (sun, r_rect)]:
            mob.generate_target()
            mob.target.set_stroke(BLACK, 3, background=True)
            mob.target.set_height(1)
            mob.target.move_to(rect)
        self.play(
            FadeIn(rects),
            MoveToTarget(rain),
            MoveToTarget(sun),
            GrowFromCenter(brace),
            p_label.shift,
            brace.get_top() + MED_SMALL_BUFF * UP -
            percentage.get_bottom(),
        )
        self.wait()

        # With updaters
        full_width = rects.get_width()
        rain.add_updater(lambda m: m.move_to(l_rect))
        sun.add_updater(lambda m: m.move_to(r_rect))
        r_rect.add_updater(lambda m: m.set_width(
            full_width - l_rect.get_width(),
            about_edge=RIGHT,
            stretch=True,
        ))
        brace.add_updater(lambda m: m.match_width(l_rect, stretch=True))
        brace.add_updater(lambda m: m.next_to(l_rect, UP, SMALL_BUFF))
        percentage.add_updater(lambda m: m.set_value(
            100 * l_rect.get_width() / full_width,
        ))
        percentage.add_updater(lambda m: m.next_to(brace, UP, MED_SMALL_BUFF))

        self.play(
            MaintainPositionRelativeTo(p_label[0], percentage),
            l_rect.stretch, 2, 0, {"about_edge": LEFT},
            run_time=8,
            rate_func=there_and_back,
        )
