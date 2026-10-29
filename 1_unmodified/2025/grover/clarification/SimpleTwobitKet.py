# ==============================================================================
# Scene:      SimpleTwobitKet
# Source:     videos/_2025/grover/clarification.py (lines 971-975)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl SimpleTwobitKet.py SimpleTwobitKet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

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



# ----- From _2025/grover/clarification.py -----

class SimpleTwobitKet(InteractiveScene):
    def construct(self):
        group = KetGroup(BitString(2, 2))
        group.scale(2)
        self.add(group)
