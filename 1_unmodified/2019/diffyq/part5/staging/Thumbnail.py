# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2019/diffyq/part5/staging.py (lines 1520-1591)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        epii = OldTex(
            "e^{ {i} \\pi} = -1",
            tex_to_color_map={
                "{i}": YELLOW,
                "\\pi": BLUE,
                "-1": GREY_A,
            }
        )
        epii.set_width(8)
        epii.to_edge(UP)
        epii.set_stroke(BLACK, 50, background=True)

        words = VGroup(
            OldTexText("in"),
            OldTexText(
                "in",
                "3.14", " minutes"
            ),
        )
        # words.set_width(FRAME_WIDTH - 4)
        words.set_stroke(BLACK, 6, background=True)
        words.set_width(FRAME_WIDTH - 2)
        words.arrange(DOWN, buff=LARGE_BUFF)
        words.next_to(epii, DOWN, LARGE_BUFF)
        words[1].set_color_by_tex("3.14", YELLOW)
        words.shift(-words[0].get_center())
        words[0].set_opacity(0)

        unit_size = 2.0
        plane = ComplexPlane()
        plane.scale(unit_size)
        plane.shift(1.0 * DOWN)
        plane.add_coordinate_labels([*range(-3, 4), complex(0, -1), complex(0, 1)])

        circle = Circle(
            radius=unit_size,
            color=YELLOW,
        )
        circle.set_stroke(GREY_B, 3)
        arc = Arc(0, PI, radius=unit_size)
        arc.set_stroke(BLUE, 10)
        circle = VGroup(arc.copy().set_stroke(BLACK, 20, background=True), circle, arc)

        circle.move_to(plane.get_origin())
        # half_circle = VMobject()
        # half_circle.pointwise_become_partial(circle, 0, 0.5)
        # half_circle.set_stroke(RED, 6)
        p_vect = Arrow(
            plane.n2p(0),
            plane.n2p(1),
            buff=0,
            fill_color=GREY_A,
            thickness=0.1
        )
        v_vect = Arrow(
            plane.n2p(1),
            plane.n2p(complex(1, 1)),
            buff=0,
            fill_color=YELLOW,
            thickness=0.1
        )
        vects = VGroup(p_vect, v_vect)

        self.add(plane)
        self.add(circle)
        self.add(vects)
        self.add(epii)
        # self.add(words)

        self.embed()
