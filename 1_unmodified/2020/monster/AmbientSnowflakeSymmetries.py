# ==============================================================================
# Scene:      AmbientSnowflakeSymmetries
# Source:     videos/_2020/monster.py (lines 3162-3188)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AmbientSnowflakeSymmetries.py AmbientSnowflakeSymmetries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_snowflake(height=2):
    snowflake = SVGMobject("snowflake")
    snowflake.set_fill(GREY_C, 1)
    snowflake.set_gloss(1)
    snowflake.set_shadow(0.2)
    snowflake.set_stroke(WHITE, 1)
    snowflake.set_height(height)
    return snowflake


def get_rot_icon(degrees, mobject, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    temp_height = 1.75
    mini_mob.set_height(temp_height)
    mini_mob.set_stroke(width=0)
    mini_mob.center()
    angle = min(degrees * DEGREES, 170 * DEGREES)
    arc1 = Arrow(
        RIGHT, rotate_vector(RIGHT, angle),
        path_arc=angle,
        buff=0
    )
    arc2 = arc1.copy().rotate(PI, about_point=ORIGIN)
    label = Integer(degrees, unit="^\\circ")
    label.set_height(0.25)
    half_vect = rotate_vector(RIGHT, angle / 2)
    label.next_to(half_vect, half_vect, buff=MED_SMALL_BUFF)
    icon = VGroup(mini_mob, arc1, arc2, label)
    icon.scale(mini_mob_height / temp_height)
    return icon


def get_flip_icon(angle, mobject, opacity=0.75, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    mini_mob.set_stroke(width=0)
    mini_mob.set_fill(opacity=opacity)
    mini_mob.set_height(mini_mob_height)
    mini_mob.center()
    sym_line = DashedLine(LEFT, RIGHT)
    sym_line.set_stroke(WHITE, 2)
    sym_line.set_width(1.2 * mini_mob_height)
    sym_line.rotate(angle)
    sym_line.move_to(mini_mob)
    back_line = sym_line.copy()
    back_line.set_stroke(BLACK, 5)
    return VGroup(mini_mob, back_line, sym_line)


class AmbientSnowflakeSymmetries(Scene):
    def construct(self):
        title = OldTex("D_6")
        title.scale(3)
        title.to_edge(LEFT, buff=1)
        title.set_color(BLUE)
        self.add(title)

        snowflake = get_snowflake()
        snowflake.set_height(5)
        snowflake.set_stroke(width=0)
        snowflake.move_to(2 * RIGHT)
        self.add(snowflake)

        for n in range(10):
            if random.choice([True, False]):
                deg = random.choice([-120, -60, 60, 120])
                icon = get_rot_icon(deg, snowflake, snowflake.get_height())
                anim = Rotate(snowflake, deg * DEGREES)
            else:
                deg = random.choice(range(30, 180, 30))
                angle = deg * DEGREES
                icon = get_flip_icon(angle, snowflake, mini_mob_height=snowflake.get_height())
                anim = Rotate(snowflake, PI, axis=rotate_vector(RIGHT, angle))
            icon.shift(snowflake.get_center() - icon[0].get_center())
            self.play(anim, FadeIn(icon[1:]))
            self.play(FadeOut(icon[1:]))
