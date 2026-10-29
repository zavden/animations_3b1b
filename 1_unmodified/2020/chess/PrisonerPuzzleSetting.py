# ==============================================================================
# Scene:      PrisonerPuzzleSetting
# Source:     videos/_2020/chess.py (lines 338-394)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrisonerPuzzleSetting.py PrisonerPuzzleSetting -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PrisonerPuzzleSetting(PiCreatureScene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E
        }
    }

    def create_pi_creatures(self):
        p1 = PiCreature(color=BLUE_C, height=2)
        p2 = PiCreature(color=RED, height=2)
        warden = PiCreature(color=GREY_BROWN, height=2.5)
        warden.flip()
        result = VGroup(p1, p2, warden)
        result.arrange(RIGHT, buff=2, aligned_edge=DOWN)
        warden.shift(RIGHT)
        result.center().to_edge(DOWN, buff=1.5)
        return result

    def construct(self):
        pis = self.pi_creatures
        p1, p2, warden = self.pi_creatures

        names = VGroup(
            OldTexText("Prisoner 1\\\\(you)"),
            OldTexText("Prisoner 2"),
            OldTexText("Warden"),
        )
        for name, pi in zip(names, pis):
            name.match_color(pi.body)
            name.next_to(pi, DOWN)

        question = OldTexText(
            "Why do mathematicians\\\\always set their puzzles\\\\in prisons?",
            alignment=""
        )
        question.to_corner(UR)

        self.remove(warden)
        warden.look_at(p2.eyes)
        self.play(
            LaggedStartMap(FadeIn, pis[:2], run_time=1.5, lag_ratio=0.3),
            LaggedStartMap(FadeIn, names[:2], run_time=1.5, lag_ratio=0.3),
        )
        self.play(
            p1.change, "sad",
            p2.change, "pleading", warden.eyes
        )
        self.play(
            FadeIn(warden),
            FadeIn(names[2]),
        )
        self.play(warden.change, "conniving", p2.eyes)
        self.wait()
        self.play(FadeIn(question, lag_ratio=0.1))
        self.wait(3)
        self.play(FadeOut(question))
        self.wait(2)
