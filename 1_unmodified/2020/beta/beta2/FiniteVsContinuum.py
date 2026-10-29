# ==============================================================================
# Scene:      FiniteVsContinuum
# Source:     videos/_2020/beta/beta2.py (lines 1394-1535)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl FiniteVsContinuum.py FiniteVsContinuum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

def get_die_faces():
    dot = Dot()
    dot.set_width(0.15)
    dot.set_color(BLUE_B)

    square = Square()
    square.round_corners(0.25)
    square.set_stroke(WHITE, 2)
    square.set_fill(GREY_E, 1)
    square.set_width(0.6)

    edge_groups = [
        (ORIGIN,),
        (UL, DR),
        (UL, ORIGIN, DR),
        (UL, UR, DL, DR),
        (UL, UR, ORIGIN, DL, DR),
        (UL, UR, LEFT, RIGHT, DL, DR),
    ]

    arrangements = VGroup(*[
        VGroup(*[
            dot.copy().move_to(square.get_bounding_box_point(ec))
            for ec in edge_group
        ])
        for edge_group in edge_groups
    ])
    square.set_width(1)

    faces = VGroup(*[
        VGroup(square.copy(), arrangement)
        for arrangement in arrangements
    ])
    faces.arrange(RIGHT)

    return faces



# ----- From _2020/beta/beta2.py -----

class FiniteVsContinuum(Scene):
    def construct(self):
        # Title
        f_title = OldTexText("Discrete context")
        f_title.set_height(0.5)
        f_title.to_edge(UP)
        f_underline = Underline(f_title)
        f_underline.scale(1.3)
        f_title.add(f_underline)
        self.add(f_title)

        # Equations
        dice = get_die_faces()[::2]
        cards = [PlayingCard(letter + "H") for letter in "A35"]

        eqs = VGroup(
            self.get_union_equation(dice),
            self.get_union_equation(cards),
        )
        for eq in eqs:
            eq.set_width(FRAME_WIDTH - 1)
        eqs.arrange(DOWN, buff=LARGE_BUFF)
        eqs.next_to(f_underline, DOWN, LARGE_BUFF)

        anims = []
        for eq in eqs:
            movers = eq.mob_copies1.copy()
            for m1, m2 in zip(movers, eq.mob_copies2):
                m1.generate_target()
                m1.target.replace(m2)
            eq.mob_copies2.set_opacity(0)
            eq.add(movers)

            self.play(FadeIn(eq[0]))

            anims.append(FadeIn(eq[1:]))
            anims.append(LaggedStartMap(
                MoveToTarget, movers,
                path_arc=30 * DEGREES,
                lag_ratio=0.1,
            ))
        self.wait()
        for anim in anims:
            self.play(anim)

        # Continuum label
        c_title = OldTexText("Continuous context")
        c_title.match_height(f_title)
        c_underline = Underline(c_title)
        c_underline.scale(1.25)

        self.play(
            Write(c_title, run_time=1),
            ShowCreation(c_underline),
            eqs[0].shift, 0.5 * UP,
            eqs[1].shift, UP,
        )

        # Range sum
        c_eq = OldTex(
            "P\\big(", "x \\in [0.65, 0.75]", "\\big)",
            "=",
            "\\sum_{x \\in [0.65, 0.75]}",
            "P(", "x", ")",
        )
        c_eq.set_color_by_tex("P", YELLOW)
        c_eq.set_color_by_tex(")", YELLOW)
        c_eq.next_to(c_underline, DOWN, LARGE_BUFF)
        c_eq.to_edge(LEFT)

        equals = c_eq.get_part_by_tex("=")
        equals.shift(SMALL_BUFF * RIGHT)
        e_cross = Line(DL, UR)
        e_cross.replace(equals, dim_to_match=0)
        e_cross.set_stroke(RED, 5)

        self.play(FadeIn(c_eq))
        self.wait(2)
        self.play(ShowCreation(e_cross))
        self.wait()

    def get_union_equation(self, mobs):
        mob_copies1 = VGroup()
        mob_copies2 = VGroup()
        p_color = YELLOW

        # Create mob_set
        brackets = OldTex("\\big\\{\\big\\}")[0]
        mob_set = VGroup(brackets[0])
        commas = VGroup()
        for mob in mobs:
            mc = mob.copy()
            mc.match_height(mob_set[0])
            mob_copies1.add(mc)
            comma = OldTex(",")
            commas.add(comma)
            mob_set.add(mc)
            mob_set.add(comma)

        mob_set.remove(commas[-1])
        commas.remove(commas[-1])
        mob_set.add(brackets[1])
        mob_set.arrange(RIGHT, buff=0.15)
        commas.set_y(mob_set[1].get_bottom()[1])

        mob_set.scale(0.8)

        # Create individual probabilities
        probs = VGroup()
        for mob in mobs:
            prob = OldTex("P(", "x = ", "00", ")")
            index = prob.index_of_part_by_tex("00")
            mc = mob.copy()
            mc.replace(prob[index])
            mc.scale(0.8, about_edge=LEFT)
            mc.match_y(prob[-1])
            mob_copies2.add(mc)
            prob.replace_submobject(index, mc)
            prob[0].set_color(p_color)
            prob[1].match_y(mc)
            prob[-1].set_color(p_color)
            probs.add(prob)

        # Result
        lhs = VGroup(
            OldTex("P\\big(", color=p_color),
            OldTex("x \\in"),
            mob_set,
            OldTex("\\big)", color=p_color),
        )
        lhs.arrange(RIGHT, buff=SMALL_BUFF)
        group = VGroup(lhs, OldTex("="))
        for prob in probs:
            group.add(prob)
            group.add(OldTex("+"))
        group.remove(group[-1])

        group.arrange(RIGHT, buff=0.2)
        group.mob_copies1 = mob_copies1
        group.mob_copies2 = mob_copies2

        return group
