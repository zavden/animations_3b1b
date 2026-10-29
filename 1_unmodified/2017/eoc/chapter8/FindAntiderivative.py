# ==============================================================================
# Scene:      FindAntiderivative
# Source:     videos/_2017/eoc/chapter8.py (lines 1795-1970)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl FindAntiderivative.py FindAntiderivative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

class Antiderivative(PiCreatureScene):
    def construct(self):
        functions = self.get_functions("t^2", "2t")
        alt_functions = self.get_functions("???", "t(8-t)")
        top_arc, bottom_arc = arcs = self.get_arcs(functions)
        derivative, antiderivative = self.get_arc_labels(arcs)
        group = VGroup(functions, arcs, derivative, antiderivative)

        self.add(functions, top_arc, derivative)
        self.wait()
        self.play(
            ShowCreation(bottom_arc),
            Write(antiderivative),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)
        for pair in reversed(list(zip(functions, alt_functions))):
            self.play(
                Transform(*pair),
                self.pi_creature.change_mode, "pondering"
            )
        self.wait(2)

        self.pi_creature_says(
            "But first!", 
            target_mode = "surprised",
            look_at = 50*OUT,
            added_anims = [group.to_edge, LEFT],
            run_time = 1,
        )
        self.wait()

    def get_functions(self, left_tex, right_tex):
        left = OldTex(left_tex)
        left.shift(2*LEFT)
        left.set_color(DISTANCE_COLOR)
        right = OldTex(right_tex)
        right.shift(2*RIGHT)
        right.set_color(VELOCITY_COLOR)
        result = VGroup(left, right)
        result.shift(UP)
        return result

    def get_arcs(self, functions):
        f1, f2 = functions
        top_line = Line(f1.get_corner(UP+RIGHT), f2.get_corner(UP+LEFT))
        bottom_line = Line(f1.get_corner(DOWN+RIGHT), f2.get_corner(DOWN+LEFT))
        top_arc = Arc(start_angle = 5*np.pi/6, angle = -2*np.pi/3)
        bottom_arc = top_arc.copy()
        bottom_arc.rotate(np.pi)
        arcs = VGroup(top_arc, bottom_arc)
        arcs.set_width(top_line.get_width())
        for arc in arcs:
            arc.add_tip()
        top_arc.next_to(top_line, UP)
        bottom_arc.next_to(bottom_line, DOWN)
        bottom_arc.set_color(MAROON_B)

        return arcs

    def get_arc_labels(self, arcs):
        top_arc, bottom_arc = arcs
        derivative = OldTexText("Derivative")
        derivative.next_to(top_arc, UP)
        antiderivative = OldTexText("``Antiderivative''")
        antiderivative.next_to(bottom_arc, DOWN)
        antiderivative.set_color(bottom_arc.get_color())

        return VGroup(derivative, antiderivative)


class FindAntiderivative(Antiderivative):
    def construct(self):
        self.introduce()
        self.first_part()
        self.second_part()
        self.combine()
        self.add_plus_C()

    def introduce(self):
        q_marks, rhs = functions = self.get_functions("???", "t(8-t)")
        expanded_rhs = OldTex("8t - t^2")
        expanded_rhs.move_to(rhs, LEFT)
        expanded_rhs.set_color(rhs.get_color())
        self.v_part1 = VGroup(*expanded_rhs[:2])
        self.v_part2 = VGroup(*expanded_rhs[2:])
        for part in self.v_part1, self.v_part2:
            part.save_state()

        top_arc, bottom_arc = arcs = self.get_arcs(functions)
        derivative, antiderivative = words = self.get_arc_labels(arcs)

        self.add(functions)
        self.play(*list(map(ShowCreation, arcs)))
        for word in words:
            self.play(FadeIn(word, lag_ratio = 0.5))
        self.wait()
        self.change_mode("confused")
        self.wait(2)
        self.play(*[
            ReplacementTransform(
                rhs[i], expanded_rhs[j],
                run_time = 2,
                path_arc = np.pi
            )
            for i, j in enumerate([1, 4, 0, 2, 3, 4])
        ]+[
            self.pi_creature.change_mode, "hesitant"
        ])
        self.wait()

        self.q_marks = q_marks
        self.arcs = arcs
        self.words = words

    def first_part(self):
        four_t_squared, two_t = self.get_functions("4t^2", "2t")
        four = four_t_squared[0]
        four.shift(UP)
        four.set_fill(opacity = 0)
        t_squared = VGroup(*four_t_squared[1:])
        two_t.move_to(self.v_part1, LEFT)

        self.play(self.v_part2.to_corner, UP+RIGHT)
        self.play(
            self.pi_creature.change, "plain", self.v_part1
        )
        self.play(ApplyWave(
            self.q_marks, 
            direction = UP, 
            amplitude = SMALL_BUFF
        ))
        self.wait(2)
        self.play(
            FadeOut(self.q_marks),
            FadeIn(t_squared),
            self.v_part1.shift, DOWN+RIGHT,
        )
        self.play(*[
            ReplacementTransform(
                t_squared[i].copy(), two_t[1-i],
                run_time = 2,
                path_arc = -np.pi/6.
            )
            for i in (0, 1)
        ])
        self.change_mode("thinking")
        self.wait()
        self.play(four.set_fill, YELLOW, 1)
        self.play(four.shift, DOWN)
        self.play(FadeOut(two_t))
        self.play(self.v_part1.restore)
        self.play(four.set_color, DISTANCE_COLOR)
        self.wait(2)

        self.s_part1 = four_t_squared

    def second_part(self):
        self.arcs_copy = self.arcs.copy()
        self.words_copy = self.words.copy()
        part1_group = VGroup(
            self.s_part1, self.v_part1, 
            self.arcs_copy, self.words_copy
        )

        neg_third_t_cubed, three_t_squared = self.get_functions(
            "- \\frac{1}{3} t^3", "3t^2"
        )
        three_t_squared.move_to(self.v_part1, LEFT)
        neg = neg_third_t_cubed[0]
        third = VGroup(*neg_third_t_cubed[1:4])
        t_cubed = VGroup(*neg_third_t_cubed[4:])
        three = three_t_squared[0]
        t_squared = VGroup(*three_t_squared[1:])

        self.play(
            part1_group.scale, 0.5,
            part1_group.to_corner, UP+LEFT,
            self.pi_creature.change_mode, "plain"
        )
        self.play(
            self.v_part2.restore,
            self.v_part2.shift, LEFT
        )
        self.play(FadeIn(self.q_marks))
        self.wait()

        self.play(
            FadeOut(self.q_marks),
            FadeIn(t_cubed),
            self.v_part2.shift, DOWN+RIGHT
        )
        self.play(*[
            ReplacementTransform(
                t_cubed[i].copy(), three_t_squared[j],
                path_arc = -np.pi/6,
                run_time = 2,
            )
            for i, j in [(0, 1), (1, 0), (1, 2)]
        ])
        self.wait()
        self.play(FadeIn(third))
        self.play(FadeOut(three))
        self.wait(2)
        self.play(Write(neg))
        self.play(
            FadeOut(t_squared),
            self.v_part2.shift, UP+LEFT
        )
        self.wait(2)

        self.s_part2 = neg_third_t_cubed

    def combine(self):
        self.play(
            self.v_part1.restore,
            self.v_part2.restore,
            self.s_part1.scale, 2,
            self.s_part1.next_to, self.s_part2, LEFT,
            FadeOut(self.arcs_copy),
            FadeOut(self.words_copy),
            run_time = 2,
        )
        self.change_mode("happy")
        self.wait(2)

    def add_plus_C(self):
        s_group = VGroup(self.s_part1, self.s_part2)
        plus_Cs = [
            OldTex("+%d"%d)
            for d in range(1, 8)
        ]
        for plus_C in plus_Cs:
            plus_C.set_color(YELLOW)
            plus_C.move_to(s_group, RIGHT)
        plus_C = plus_Cs[0]

        self.change_mode("sassy")
        self.wait()
        self.play(
            s_group.next_to, plus_C.copy(), LEFT,
            GrowFromCenter(plus_C),
        )
        self.wait()
        for new_plus_C in plus_Cs[1:]:
            self.play(Transform(plus_C, new_plus_C))
            self.wait()
