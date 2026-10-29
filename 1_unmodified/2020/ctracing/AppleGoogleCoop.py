# ==============================================================================
# Scene:      AppleGoogleCoop
# Source:     videos/_2020/ctracing.py (lines 390-429)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AppleGoogleCoop.py AppleGoogleCoop -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AppleGoogleCoop(Scene):
    def construct(self):
        logos = Group(
            self.get_apple_logo(),
            self.get_google_logo(),
        )
        for logo in logos:
            logo.set_height(2)
        apple, google = logos

        logos.arrange(RIGHT, buff=3)

        arrows = VGroup()
        for vect, u in zip([UP, DOWN], [0, 1]):
            m1, m2 = logos[u], logos[1 - u]
            arrows.add(Arrow(
                m1.get_edge_center(vect),
                m2.get_edge_center(vect),
                path_arc=-90 * DEGREES,
                buff=MED_LARGE_BUFF,
                stroke_width=10,
            ))

        self.play(LaggedStart(
            Write(apple),
            FadeIn(google),
            lag_ratio=0.7,
        ))
        self.wait()
        self.play(ShowCreation(arrows, run_time=2))
        self.wait()

    def get_apple_logo(self):
        result = SVGMobject("apple_logo")
        result.set_color("#b3b3b3")
        return result

    def get_google_logo(self):
        result = ImageMobject("google_logo_black")
        return result
