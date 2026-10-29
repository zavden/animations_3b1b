# ==============================================================================
# Scene:      WriteClassicalBigO
# Source:     videos/_2025/grover/runtime.py (lines 472-498)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteClassicalBigO.py WriteClassicalBigO -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteClassicalBigO(InteractiveScene):
    def construct(self):
        # Background
        self.add(FullScreenRectangle().set_fill(GREY_E))

        # Terms
        avg = TexText(R"Avg: $\displaystyle \frac{1}{2} N$")
        arrow = Tex(R"\longrightarrow")
        big_o = Tex(R"\mathcal{O}(N)")
        group = VGroup(avg, arrow, big_o)
        group.arrange(RIGHT, SMALL_BUFF)
        group.scale(1.25)
        group.to_edge(UP, buff=MED_SMALL_BUFF)

        avg.save_state()
        avg.set_x(0)

        self.play(Write(avg))
        self.wait()
        self.play(Restore(avg))
        self.play(
            Write(arrow),
            TransformFromCopy(avg[-1], big_o[2], path_arc=45 * DEG),
            Write(big_o[:2]),
            Write(big_o[3:]),
        )
        self.wait()
