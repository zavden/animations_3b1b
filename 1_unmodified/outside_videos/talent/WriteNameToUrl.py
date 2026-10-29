# ==============================================================================
# Scene:      WriteNameToUrl
# Source:     videos/outside_videos/talent.py (lines 55-76)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteNameToUrl.py WriteNameToUrl -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteNameToUrl(InteractiveScene):
    def construct(self):
        # Test
        full_name = Text("3b1b Talent", font_size=90)
        url = Text("3b1b.co/talent", font_size=90)
        url.shift((full_name["3"].get_y(UP) - url["3"].get_y(UP)) * UP)
        VGroup(full_name, url).set_backstroke(BLACK, 10)

        back_rect = BackgroundRectangle(url)
        back_rect.set_fill(BLACK, 0.9)
        back_rect.set_z_index(-1)

        self.play(Write(full_name, stroke_color=WHITE, run_time=2))
        self.wait()
        self.play(LaggedStart(
            FadeIn(back_rect),
            ReplacementTransform(full_name["3b1b"], url["3b1b"]),
            Write(url[".co/"].set_stroke(behind=True), stroke_color=WHITE),
            ReplacementTransform(full_name["Talent"], url["talent"]),
            lag_ratio=0.25,
        ))
        self.wait()
