# ==============================================================================
# Scene:      QuadStack
# Source:     videos/_2026/monthly_mindbenders/quadrilateral_stack.py (lines 33-72)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuadStack.py QuadStack -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def position_blocks_into_tower(blocks, vertices):
    zs = list(map(R3_to_complex, vertices))
    mult = (zs[2] - zs[3]) / (zs[1] - zs[0])
    for block in blocks:
        points = list(map(complex_to_R3, zs))
        block.set_points_as_corners(points + [points[0]])
        zs = [(z - zs[0]) * mult + zs[3] for z in zs]
    return blocks


class QuadStack(InteractiveScene):
    def construct(self):
        # Add quadrilateral
        plane = NumberPlane()
        initial_coords = [(0, 0), (2, 0), (1.5, 1.5), (0, 2)]
        moving_dots = Group(GlowDot(plane.c2p(*coords)) for coords in initial_coords)
        moving_dots.shift(3 * DL)

        def get_points(offset=0):
            n = len(moving_dots)
            return [
                moving_dots[(i + offset) % n].get_center()
                for i in range(n)
            ]

        n_blocks = 100
        tower1 = Square().replicate(n_blocks)
        tower1.set_stroke(WHITE, 2)
        tower2 = tower1.copy()

        tower1.add_updater(lambda m: position_blocks_into_tower(m, get_points()))
        tower2.add_updater(lambda m: position_blocks_into_tower(m, get_points(offset=3)))

        self.disable_interaction(tower1, tower2)

        self.add(*moving_dots)
        self.add(tower1, tower2)

        # Add on 
        self.add(tower1[0])
        for n in range(n_blocks - 1):
            self.play(
                TransformFromCopy(tower1[n], tower1[n + 1]),
                run_time=1 / (n + 1)
            )
        for n in range(n_blocks - 1):
            self.play(
                TransformFromCopy(tower2[n], tower2[n + 1]),
                run_time=1 / (n + 1)
            )
