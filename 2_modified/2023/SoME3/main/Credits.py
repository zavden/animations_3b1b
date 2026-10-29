# ==============================================================================
# Scene:      Credits
# Source:     videos/_2023/SoME3/main.py (lines 419-447)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Credits.py Credits -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - Placeholder LOGO_stacked_w_registration_white.svg ('Jane Street' text as outlines, white) at the root of _lib/assets/svg_images/ (make_some3_assets.py); the scene asks for it by Grant's Dropbox path and manim_imports_ext finds it by name
# ==============================================================================

from manim_imports_ext import *

class Credits(InteractiveScene):
    def construct(self):
        # Credits
        credit_words = [
            ("Community management and logistics", "James Schloss"),
            ("Web development", "Frédéric Crozatier"),
            ("Guest judging, advising, and funding", "Jane Street"),
        ]
        credits = VGroup(*(
            VGroup(
                Text(role, font_size=36, fill_color=GREY_B),
                Text(name, font_size=48),
            ).arrange(DOWN)
            for role, name in credit_words
        ))
        credits.arrange(DOWN, buff=1.0)
        credits.to_edge(UP)

        logo = SVGMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/SoME3/main/images/janestreet_logo/LOGO_stacked_w_registration_white.svg")
        logo.set_height(1.75)
        logo.move_to(credits[2][1], UP)
        logo.shift(0.5 * DOWN)
        credits[2].replace_submobject(1, logo)

        for credit in credits:
            for part in credit.family_members_with_points():
                part.set_stroke(color=part.get_fill_color(), width=0.5, background=True)
            self.play(FadeIn(credit[0]), Write(credit[1]))
            self.wait()
