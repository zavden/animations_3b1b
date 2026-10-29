# ==============================================================================
# Scene:      TalentContactCard
# Source:     videos/outside_videos/talent.py (lines 232-265)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TalentContactCard.py TalentContactCard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TalentContactCard(InteractiveScene):
    def construct(self):
        words = VGroup(
            VGroup(
                Text("Interested in joining?"),
                Text("Reach out to explore if your company is a good fit")
            ),
            VGroup(
                Text("Find a job through this page?"),
                Text("Let us know, we’d love to hear your story!")
            ),
        )
        for group in words:
            group[0].scale(1.25)
            group[1].scale(0.75)
            group[1].set_color(GREY_B)
            group.arrange(DOWN, buff=0.5)
        words.arrange(DOWN, buff=1.25)

        address = Text("talent@3blue1brown.com", font_size=48)
        address.set_color(BLUE)
        address.next_to(words, UP, LARGE_BUFF)

        # Test
        self.add(words[0][0])
        self.play(
            FadeIn(words[0][1], lag_ratio=0.1, run_time=1.5),
            FadeIn(address, 0.5 * UP),
        )
        self.play(LaggedStart(
            FadeIn(words[1][0]),
            FadeIn(words[1][1], lag_ratio=0.1, run_time=2)
        ))
        self.wait()
