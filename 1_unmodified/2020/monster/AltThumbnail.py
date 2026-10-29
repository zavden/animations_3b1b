# ==============================================================================
# Scene:      AltThumbnail
# Source:     videos/_2020/monster.py (lines 212-261)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltThumbnail.py AltThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


class AltThumbnail(ThreeDScene):
    def construct(self):
        lines = VGroup(*(Line(DOWN, UP) for x in range(2)))
        lines.set_height(FRAME_HEIGHT)
        lines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        lines.set_stroke(GREY_B, 3)
        self.add(lines)

        mob_width = FRAME_WIDTH / 3 - 1

        titles = VGroup(Text("Symmetry"), Text("Abstraction"), Text("Monsters"))
        titles.set_width(mob_width + 0.5)
        for title, x in zip(titles, [-1, 0, 1]):
            title.set_x(x * FRAME_WIDTH / 3)
            title.to_edge(UP)
        self.add(titles)

        cube = Cube()
        cubes = Group(cube)
        for axis in [[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1]]:
            for angle in [60 * DEGREES]:
                cubes.add(cube.copy().rotate(angle, axis))

        cubes.rotate(95 * DEGREES, RIGHT)
        cubes.rotate(30 * DEGREES, UP)
        cubes.set_width(mob_width)
        cubes.match_x(titles[0])
        cubes.set_y(-0.5)
        cubes.set_color(BLUE_D)
        cubes.set_shadow(0.65)
        cubes.set_gloss(0.5)

        self.add(cubes)

        eq = OldTex("f(gh)", "=", "(fg)h")
        eq[1].rotate(90 * DEGREES)
        eq.arrange(DOWN)

        eq.match_height(cubes)
        eq.center()
        eq.match_y(cubes)
        self.add(eq)

        monster = get_monster()
        monster.set_fill(GREY_BROWN)
        monster.set_gloss(0.5)
        monster.set_width(mob_width)
        monster.match_x(titles[2])
        monster.match_y(cubes)
        self.add(monster)
