# ==============================================================================
# Scene:      OneIn200HasDisease
# Source:     videos/_2018/eop/chapter1/show_uncertainty_disease.py (lines 60-104)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/eop_constants.py
#
# Run from this folder:
#     manimgl OneIn200HasDisease.py OneIn200HasDisease -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/eop_constants.py -----

SICKLY_GREEN = "#9BBD37"



# ----- From _2018/eop/chapter1/show_uncertainty_disease.py -----

class OneIn200HasDisease(Scene):
    def construct(self):
        title = OldTexText("1 in 200")
        title.to_edge(UP)
        creature = PiCreature()

        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(20)
            ]).arrange(DOWN, SMALL_BUFF)
            for x in range(10)
        ]).arrange(RIGHT, SMALL_BUFF)
        all_creatures.set_height(FRAME_HEIGHT * 0.8)
        all_creatures.next_to(title, DOWN)
        randy = all_creatures[0][0]
        all_creatures[0].remove(randy)
        randy.change_mode("sick")
        randy.set_color(SICKLY_GREEN)
        randy.save_state()
        randy.set_height(3)
        randy.center()
        randy.change_mode("plain")
        randy.set_color(BLUE)

        self.add(randy)

        #p_sick = OldTex("p(","\\text{sick}",") = 0.5\%")
        #p_sick.set_color_by_tex("sick", SICKLY_GREEN)
        #p_sick.next_to(randy, RIGHT+UP)
        #self.add(p_sick)
        self.wait()
        
        self.play(
            randy.change_mode, "sick",
            randy.set_color, SICKLY_GREEN
        )
        self.play(Blink(randy))
        self.play(randy.restore)
        self.wait()
        self.play(
            Write(title),
            LaggedStartMap(FadeIn, all_creatures, run_time = 3)
        )
        self.wait()
