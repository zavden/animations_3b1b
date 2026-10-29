# ==============================================================================
# Scene:      FullLunarEclipseDistance
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 773-811)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/cosmic_distance/planets.py
#
# Run from this folder:
#     manimgl FullLunarEclipseDistance.py FullLunarEclipseDistance -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/cosmic_distance/planets.py -----

# All in Kilometers
EARTH_RADIUS = 6_371


MOON_RADIUS = 1_737.4



# ----- From _2025/cosmic_distance/supplements.py -----

class FullLunarEclipseDistance(InteractiveScene):
    def construct(self):
        # Add terms
        R_e = 1.5
        R_m = R_e * (MOON_RADIUS / EARTH_RADIUS)

        diam_line = Line(R_e * DOWN, R_e * UP)
        start_dot = Dot(R_e * DOWN, radius=0.04)
        end_dot = Dot((R_e + 2 * R_m) * UP, radius=0.04)

        diam_brace = Brace(diam_line, RIGHT)
        diam_brace.add(diam_brace.get_tex(R"2R_E", font_size=36))

        R_m_brace = Brace(Line(diam_line.get_top(), end_dot.get_center()), RIGHT)
        R_m_brace.add(R_m_brace.get_tex(R"2 R_M", font_size=36))

        start_words = Text("Leading edge start")
        end_words = Text("Leading edge end")

        for words, dot in [(start_words, start_dot), (end_words, end_dot)]:
            words.next_to(dot, LEFT, buff=LARGE_BUFF)
            arrow = Arrow(words, dot, buff=0.1)
            words.shift(0.05 * UP)
            words.add(arrow)
            VGroup(words, dot).set_color(TEAL)

        # Animations
        self.play(
            FadeIn(start_words, lag_ratio=0.1),
            FadeIn(start_dot),
        )
        self.wait(2)
        self.play(FadeIn(diam_brace))
        self.wait()
        self.play(
            FadeIn(end_words, lag_ratio=0.1),
            FadeIn(end_dot)
        )
        self.play(FadeIn(R_m_brace))
