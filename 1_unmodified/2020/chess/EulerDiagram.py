# ==============================================================================
# Scene:      EulerDiagram
# Source:     videos/_2020/chess.py (lines 4517-4564)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EulerDiagram.py EulerDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_coords(n, min_dim=3):
    bits = "{0:b}".format(n)
    bits = (min_dim - len(bits)) * '0' + bits
    return np.array(list(map(int, bits)))


def get_bit_string(bit_coords):
    result = VGroup(*[Integer(int(b)) for b in bit_coords])
    result.arrange(RIGHT, buff=SMALL_BUFF)
    result.set_stroke(BLACK, 4, background=True)
    return result


class EulerDiagram(Scene):
    def construct(self):
        colors = [RED, GREEN, BLUE]
        vects = compass_directions(3, UP)
        circles = VGroup(*[
            Circle(
                radius=2,
                fill_color=color,
                stroke_color=color,
                fill_opacity=0.5,
                stroke_width=3,
            ).shift(1.2 * vect)
            for vect, color in zip(vects, colors)
        ])
        bit_coords = list(map(int_to_bit_coords, range(8)))
        bit_strings = VGroup(*map(get_bit_string, bit_coords))
        bit_strings.center()
        r1 = 2.2
        r2 = 1.4
        bit_strings[0].next_to(circles[0], LEFT).shift(UP)
        bit_strings[1].shift(r1 * vects[0])
        bit_strings[2].shift(r1 * vects[1])
        bit_strings[3].shift(r2 * (vects[0] + vects[1]))
        bit_strings[4].shift(r1 * vects[2])
        bit_strings[5].shift(r2 * (vects[0] + vects[2]))
        bit_strings[6].shift(r2 * (vects[1] + vects[2]))

        self.add(circles)

        for circle in circles:
            circle.save_state()

        for coords, bstring in zip(bit_coords[1:], bit_strings[1:]):
            for circ, coord in zip(circles, reversed(coords)):
                circ.generate_target()
                if coord:
                    circ.target.become(circ.saved_state)
                else:
                    circ.target.set_opacity(0.1)
            self.play(
                FadeIn(bstring),
                *map(MoveToTarget, circles),
                run_time=0.25,
            )
            self.wait(0.75)
        self.wait()
        self.play(FadeIn(bit_strings[0], DOWN))
        self.wait()
