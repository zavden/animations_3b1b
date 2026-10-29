# ==============================================================================
# Scene:      GroupsBeyondActions
# Source:     videos/_2020/monster.py (lines 2923-2955)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroupsBeyondActions.py GroupsBeyondActions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroupsBeyondActions(Scene):
    def construct(self):
        groups = OldTexText("Groups")
        sym_acts = OldTexText("Symmetric\\\\Actions")
        others = OldTexText("Other things\\\\which ``multiply''")
        VGroup(groups, sym_acts, others).scale(1.5)
        line = Line(UP, DOWN)

        sym_acts.set_color(BLUE)
        others.set_color(interpolate_color(GREY_BROWN, WHITE, 0.5))

        VGroup(
            groups, line, sym_acts
        ).arrange(DOWN, buff=MED_LARGE_BUFF)

        line.add_updater(lambda m: m.put_start_and_end_on(
            groups.get_bottom() + 0.3 * DOWN,
            sym_acts.get_top() + 0.3 * UP,
        ))

        others.move_to(sym_acts)
        others.to_edge(RIGHT)
        others_line = Line(groups.get_bottom(), others.get_top(), buff=0.3)

        self.add(groups, line, sym_acts)
        self.wait()
        self.play(
            sym_acts.to_edge, LEFT, LARGE_BUFF,
            FadeIn(others, 2 * UL),
            ShowCreation(others_line),
            run_time=2,
        )
        self.wait()
