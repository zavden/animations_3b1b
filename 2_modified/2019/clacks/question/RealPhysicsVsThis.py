# ==============================================================================
# Scene:      RealPhysicsVsThis
# Source:     videos/_2019/clacks/question.py (lines 1320-1333)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RealPhysicsVsThis.py RealPhysicsVsThis -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Explicitly pass WHITE to set_color, keeping Cairo's default value.
# ==============================================================================

from manim_imports_ext import *

class RealPhysicsVsThis(Scene):
    def construct(self):
        physics = OldTexText("Real physics")
        this = OldTexText("This process")
        # CHANGE: pass Cairo's former default color explicitly.
        this.set_color(WHITE)
        physics.to_edge(LEFT)
        this.next_to(physics)
        self.add(physics, this)
        self.play(
            this.shift, FRAME_WIDTH * RIGHT,
            rate_func=rush_into,
            run_time=3,
        )
        self.wait()
