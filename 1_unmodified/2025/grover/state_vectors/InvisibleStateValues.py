# ==============================================================================
# Scene:      InvisibleStateValues
# Source:     videos/_2025/grover/state_vectors.py (lines 2013-2056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InvisibleStateValues.py InvisibleStateValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BitString(VGroup):
    def __init__(self, value, length=4, buff=SMALL_BUFF):
        self.length = length
        bit_mob = Integer(0)
        super().__init__(bit_mob.copy() for n in range(length))
        self.arrange(RIGHT, buff=buff)
        self.set_value(value)

    def set_value(self, value):
        bits = bin(value)[2:].zfill(self.length)
        for mob, bit in zip(self, bits):
            mob.set_value(int(bit))


class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)


class InvisibleStateValues(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        n = 5
        values = np.random.uniform(-1, 1, 2**n)
        vect = DecimalMatrix(values.reshape(-1, 1), decimal_config=dict(include_sign=True))
        vect.set_height(FRAME_HEIGHT - 1)
        indices = VGroup(BitString(k, 5) for k in range(2**n))
        for index, elem in zip(indices, vect.elements):
            index.match_height(elem)
            index.set_color(GREY_C)
            index.next_to(vect, LEFT, SMALL_BUFF)
            index.match_y(elem)

        rects = VGroup(SurroundingRectangle(elem, buff=0.05) for elem in vect.elements)
        rects.set_stroke(YELLOW, 1)

        frame.set_height(2, about_edge=UP)
        self.add(vect, indices)
        self.play(
            LaggedStartMap(ShowCreation, rects, lag_ratio=0.25),
            frame.animate.to_default_state(),
            run_time=5,
        )

        rects.target = rects.generate_target()
        rects.target.set_stroke(WHITE, 1)
        rects.target.set_fill(GREY_D, 1)
        self.play(MoveToTarget(rects, lag_ratio=0.1, run_time=3))
        self.wait()

        # Shrink down
        group = Group(indices, vect, Point(), rects)
        self.play(group.animate.set_height(4).move_to(4 * RIGHT), run_time=2)
        self.wait()

        # Revealed value
        value = KetGroup(BitString(13, 5))
        value.move_to(group)

        self.clear()
        self.add(value)
        self.wait()
