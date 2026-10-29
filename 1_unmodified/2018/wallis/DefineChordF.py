# ==============================================================================
# Scene:      DefineChordF
# Source:     videos/_2018/wallis.py (lines 2385-2540)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineChordF.py DefineChordF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineChordF(Scene):
    def construct(self):
        radius = 2.5

        full_chord_f = OldTexText(
            "``", "Chord(", "$f$", ")", "''", arg_separator="")
        full_chord_f.set_color_by_tex("$f$", YELLOW)
        full_chord_f.to_edge(UP)
        chord_f = full_chord_f[1:-1]
        chord_f.generate_target()

        circle = Circle(radius=2.5)
        circle.set_color(RED)
        radius_line = Line(circle.get_center(), circle.get_right())
        one_label = OldTex("1")
        one_label.next_to(radius_line, DOWN, SMALL_BUFF)

        chord = Line(*[circle.point_from_proportion(f) for f in [0, 1. / 3]])
        chord.set_color(YELLOW)
        chord_third = OldTexText("Chord(", "$1/3$", ")", arg_separator="")
        chord_third.set_color_by_tex("1/3", YELLOW)
        for term in chord_third, chord_f.target:
            term.next_to(chord.get_center(), UP, SMALL_BUFF)
            chord_angle = chord.get_angle() + np.pi
            term.rotate(chord_angle, about_point=chord.get_center())

        brace = Brace(Line(ORIGIN, TAU * UP / 3), RIGHT, buff=0)
        brace.generate_target()
        brace.target.stretch(0.5, 0)
        brace.target.apply_complex_function(np.exp)
        VGroup(brace, brace.target).scale(radius)
        brace.next_to(circle.get_right(), RIGHT, SMALL_BUFF, DOWN)
        brace.scale(0.5, about_edge=DOWN)
        brace.target.move_to(brace, DR)
        brace.target.shift(2 * SMALL_BUFF * LEFT)

        f_label = OldTex("f")
        f_label.set_color(YELLOW)
        point = circle.point_from_proportion(1.0 / 6)
        f_label.move_to(point + 0.4 * (point - circle.get_center()))

        third_label = OldTex("\\frac{1}{3}")
        third_label.scale(0.7)
        third_label.move_to(f_label)
        third_label.match_color(f_label)

        alphas = np.linspace(0, 1, 4)
        third_arcs = VGroup(*[
            VMobject().pointwise_become_partial(circle, a1, a2)
            for a1, a2 in zip(alphas, alphas[1:])
        ])
        third_arcs.set_color_by_gradient(BLUE, PINK, GREEN)

        # Terms for sine formula
        origin = circle.get_center()
        height = DashedLine(origin, chord.get_center())
        half_chords = VGroup(
            Line(chord.get_start(), chord.get_center()),
            Line(chord.get_end(), chord.get_center()),
        )
        half_chords.set_color_by_gradient(BLUE, PINK)
        alt_radius_line = Line(origin, chord.get_end())
        alt_radius_line.set_color(WHITE)
        angle_arc = Arc(
            radius=0.3,
            angle=TAU / 6,
        )
        angle_arc.shift(origin)
        angle_label = OldTex("\\frac{f}{2}", "2\\pi")
        angle_label[0][0].set_color(YELLOW)
        angle_label.scale(0.6)
        angle_label.next_to(angle_arc, RIGHT, SMALL_BUFF, DOWN)
        angle_label.shift(SMALL_BUFF * UR)

        circle_group = VGroup(
            circle, chord, radius_line, one_label,
            brace, f_label, chord_f,
            half_chords, height,
            angle_arc, angle_label,
        )

        formula = OldTex(
            "= 2 \\cdot \\sin\\left(\\frac{f}{2} 2\\pi \\right)",
            "= 2 \\cdot \\sin\\left(f \\pi \\right)",
        )
        for part in formula:
            part[7].set_color(YELLOW)

        # Draw circle and chord
        self.add(radius_line, circle, one_label)
        self.play(Write(full_chord_f))
        self.play(ShowCreation(chord))
        self.play(
            MoveToTarget(chord_f),
            FadeOut(VGroup(full_chord_f[0], full_chord_f[-1]))
        )
        self.play(GrowFromEdge(brace, DOWN))
        self.play(MoveToTarget(brace, path_arc=TAU / 3))
        self.play(Write(f_label))
        self.wait(2)

        # Show third
        self.remove(chord_f, f_label)
        self.play(
            ReplacementTransform(chord_f.copy(), chord_third),
            ReplacementTransform(f_label.copy(), third_label),
        )
        chord_copies = VGroup()
        last_chord = chord
        for color in PINK, BLUE:
            chord_copy = last_chord.copy()
            old_color = chord_copy.get_color()
            self.play(
                Rotate(chord_copy, -TAU / 6, about_point=last_chord.get_end()),
                UpdateFromAlphaFunc(
                    chord_copy,
                    lambda m, a: m.set_stroke(
                        interpolate_color(old_color, color, a))
                )
            )
            chord_copy.reverse_points()
            last_chord = chord_copy
            chord_copies.add(chord_copy)
        self.wait()
        self.play(
            FadeOut(chord_copies),
            ReplacementTransform(chord_third, chord_f),
            ReplacementTransform(third_label, f_label),
        )

        # Show sine formula
        top_chord_f = chord_f.copy()
        top_chord_f.generate_target()
        top_chord_f.target.rotate(-chord_angle)
        top_chord_f.target.center().to_edge(UP, buff=LARGE_BUFF)
        top_chord_f.target.shift(3 * LEFT)
        formula.next_to(top_chord_f.target, RIGHT)

        self.play(
            ShowCreation(height),
            FadeIn(half_chords),
            ShowCreation(angle_arc),
            Write(angle_label)
        )
        self.wait()
        self.play(
            MoveToTarget(top_chord_f),
            circle_group.shift, 1.5 * DOWN,
        )
        self.play(Write(formula[0], run_time=1))
        self.wait()
        self.play(ReplacementTransform(
            formula[0].copy(), formula[1],
            path_arc=45 * DEGREES
        ))
        self.wait()
