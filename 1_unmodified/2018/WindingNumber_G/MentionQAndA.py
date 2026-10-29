# ==============================================================================
# Scene:      MentionQAndA
# Source:     videos/_2018/WindingNumber_G.py (lines 2933-2962)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl MentionQAndA.py MentionQAndA -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class MentionQAndA(Scene):
    def construct(self):
        title = OldTexText("Q\\&A with ", "Ben", "and", "Sridhar\\\\", "at", "Patreon")
        title.set_color_by_tex_to_color_map({
            "Ben" : MAROON,
            "Sridhar" : YELLOW,
        })
        patreon_logo = VGroup(*PatreonLogo().family_members_with_points())
        patreon_logo.sort()
        patreon_logo.replace(title.get_parts_by_tex("Patreon"))
        patreon_logo.scale(1.3, about_edge = LEFT)
        patreon_logo.shift(0.5*SMALL_BUFF*DOWN)
        title.submobjects[-1] = patreon_logo

        title.to_edge(UP)
        self.add(title)

        questions = VGroup(*list(map(TexText, [
            "If you think of the current videos as short stories, \\\\ what is the novel that you want to write?",
            "How did you get into mathematics?",
            "What motivated you to join 3b1b?",
            "$\\vdots$",
        ])))
        questions.arrange(DOWN, buff = 0.75)
        questions.next_to(title, DOWN, LARGE_BUFF)

        self.play(LaggedStartMap(FadeIn, questions, run_time = 3))
        self.wait(2)
        self.play(FadeOut(questions))
        self.wait()
