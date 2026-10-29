# ==============================================================================
# Scene:      NonlinearityOfLanguage
# Source:     videos/_2024/transformers/mlp.py (lines 1758-1921)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NonlinearityOfLanguage.py NonlinearityOfLanguage -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NonlinearityOfLanguage(InteractiveScene):
    def construct(self):
        # Set up axes and M + J
        unit_size = 2.5

        plane = NumberPlane(
            axis_config=dict(
                stroke_width=1,
            ),
            background_line_style=dict(
                stroke_color=BLUE_D,
                stroke_width=1,
                stroke_opacity=0.75
            ),
            faded_line_ratio=1,
            unit_size=unit_size,
        )
        m_vect = Vector(unit_size * RIGHT).rotate(60 * DEGREES, about_point=ORIGIN)
        j_vect = m_vect.copy().rotate(-90 * DEGREES, about_point=ORIGIN)
        m_vect.set_color(YELLOW)
        j_vect.set_color(RED)
        m_ghost = m_vect.copy().shift(j_vect.get_vector())
        j_ghost = j_vect.copy().shift(m_vect.get_vector())
        VGroup(m_ghost, j_ghost).set_stroke(opacity=0.25)

        sum_point = m_ghost.get_end()
        span_line = Line(-sum_point, sum_point)
        span_line.set_length(2 * FRAME_WIDTH)
        span_line.set_stroke(WHITE, 2, opacity=0.5)

        self.add(plane)
        self.add(m_vect, m_ghost, j_vect, j_ghost)
        self.add(span_line)

        # Label vectors
        m_label = Text("First Name Michael")
        j_label = Text("Last Name Jordan")
        for label, vect in [(m_label, m_vect), (j_label, j_vect)]:
            label.scale(0.6)
            label.match_color(vect)
            direction = np.sign(vect.get_vector()[1]) * UP
            label.next_to(ORIGIN, direction, buff=0.2, aligned_edge=LEFT)
            label.rotate(vect.get_angle(), about_point=ORIGIN)
            label.set_backstroke(BLACK, 3)

        self.add(m_label)
        self.add(j_label)

        # Add dot product expression
        expr = Tex(R"(\vec{\textbf{M}} + \vec{\textbf{J}}) \cdot \textbf{E}")
        expr[1:3].match_color(m_vect)
        expr[4:6].match_color(j_vect)
        expr.to_corner(UL)
        self.add(expr)

        # Set up embedding with dot product tracker
        emb_point = VectorizedPoint(unit_size * UL)
        emb = Vector()
        emb.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, emb_point.get_center()))
        normalized_sum = normalize(sum_point)

        def get_line_point():
            return normalized_sum * np.dot(normalized_sum, emb_point.get_center())

        shadow = Line()
        shadow.set_stroke(PINK, 3)
        shadow.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, get_line_point()))  # This is a long line

        dot = Dot()
        dot.set_fill(PINK, 1)
        dot.f_always.move_to(get_line_point)

        dashed_line = always_redraw(
            lambda: DashedLine(emb_point.get_center(), get_line_point()).set_stroke(PINK, 2)
        )

        dp_decimal = DecimalNumber(font_size=36)
        dp_decimal.match_color(dot)
        dp_decimal.f_always.set_value(lambda: np.dot(normalized_sum, emb_point.get_center()) * 2.0 / 3.535534)
        dp_decimal.always.next_to(dot, DR, buff=SMALL_BUFF)

        self.add(shadow, emb, dot, dashed_line, dp_decimal)

        emb_point.move_to(ORIGIN + 0.01 * UP)
        for point in [m_vect.get_end(), m_ghost.get_end(), j_vect.get_end(), m_ghost.get_end()]:
            self.play(emb_point.animate.move_to(point), run_time=3)

        # Set up names
        names = VGroup(
            Text(name, font_size=36)
            for name in [
                "Michael Jordan",
                "Michael Phelps",
                "Alexis Jordan",
            ]
        )
        name_points = [
            sum_point,
            m_vect.get_end(),
            j_vect.get_end(),
        ]
        for name, point in zip(names, name_points):
            name.set_backstroke(BLACK, 3)
            direction = RIGHT + np.sign(point[1]) * UP
            name.next_to(point, direction, buff=0.1)

        # Go through names
        name = names[0].copy()
        name_ghosts = names.copy().set_fill(opacity=0.75).set_stroke(width=0)

        self.play(
            FadeIn(name, 0.5 * UP),
            Rotate(emb_point, TAU, about_point=emb_point.get_center() + 0.15 * DL, run_time=4),
        )
        self.wait()
        self.add(name_ghosts[0])
        self.play(
            Transform(name, names[1]),
            emb_point.animate.move_to(m_vect.get_end()),
            run_time=2,
        )
        self.wait()
        self.add(name_ghosts[1])
        self.play(
            Transform(name, names[2]),
            emb_point.animate.move_to(j_vect.get_end()).set_anim_args(path_arc=30 * DEGREES),
            run_time=2,
        )
        self.add(name_ghosts[2])
        self.wait()

        # Show other names
        other_point = span_line.pfp(0.45)
        other_word = Text("(Other)", font_size=36)
        other_word.set_fill(GREY_B)
        other_word.next_to(other_point, UL, buff=0)

        self.play(
            emb_point.animate.move_to(other_point),
            LaggedStart(
                FadeOut(name),
                FadeIn(other_word),
                lag_ratio=0.5,
            ),
            run_time=3
        )
        self.wait()

        # Show "yes" vs. "no" regions
        regions = FullScreenRectangle().scale(2).replicate(2)
        regions.arrange(LEFT, buff=0)
        regions[0].set_fill(GREEN_B, 0.35)
        regions[1].set_fill(RED, 0.25)
        regions.rotate(span_line.get_angle(), about_point=ORIGIN)
        regions.shift(0.85 * sum_point)

        yes_no_words = VGroup(
            Text("Yes", font_size=72).set_fill(GREEN).to_corner(UR),
            Text("No", font_size=72).set_fill(RED).to_edge(UP).shift(LEFT),
        )

        for region, word in zip(regions, yes_no_words):
            self.play(FadeIn(region), FadeIn(word))
        self.wait()
