# ==============================================================================
# Scene:      IMOGoldOrganizations
# Source:     videos/_2025/guest_videos/misc_animations.py (lines 158-185)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IMOGoldOrganizations.py IMOGoldOrganizations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IMOGoldOrganizations(InteractiveScene):
    def construct(self):
        # Test
        orgs = VGroup(
            Text("Google DeepMind"),
            Text("OpenAI"),
            Text("Harmonic"),
            Text("ByteDance"),
        )
        orgs.scale(1.5)
        orgs.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        orgs.to_edge(LEFT, buff=1)
        top_brace = Brace(orgs[:2], RIGHT)
        low_brace = Brace(orgs[2:], RIGHT)
        top_text = top_brace.get_text("Natural language", buff=0.5).set_color(BLUE_A)
        low_text = low_brace.get_text("Lean", buff=0.5).set_color(YELLOW_B)

        self.play(LaggedStartMap(FadeIn, orgs, shift=DOWN, lag_ratio=0.15))
        self.wait()
        self.play(LaggedStart(
            GrowFromCenter(top_brace),
            FadeIn(top_text, RIGHT),
            orgs[:2].animate.match_color(top_text),
            GrowFromCenter(low_brace),
            FadeIn(low_text, RIGHT),
            orgs[2:].animate.match_color(low_text),
        ))
        self.wait()
