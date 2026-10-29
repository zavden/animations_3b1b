# ==============================================================================
# Scene:      ComplexNumberPreview
# Source:     videos/_2020/ldm.py (lines 460-482)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexNumberPreview.py ComplexNumberPreview -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexNumberPreview(Scene):
    def construct(self):
        plane = ComplexPlane(axis_config={"stroke_width": 4})
        plane.add_coordinates()

        z = complex(2, 1)
        dot = Dot()
        dot.move_to(plane.n2p(z))
        label = OldTex("2+i")
        label.set_color(YELLOW)
        dot.set_color(YELLOW)
        label.next_to(dot, UR, SMALL_BUFF)
        label.set_stroke(BLACK, 5, background=True)

        line = Line(plane.n2p(0), plane.n2p(z))
        arc = Arc(start_angle=0, angle=np.log(z).imag, radius=0.5)

        self.add(plane)
        self.add(line, arc)
        self.add(dot)
        self.add(label)

        self.embed()
