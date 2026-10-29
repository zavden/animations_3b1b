# ==============================================================================
# Scene:      CurvesDefiningFonts
# Source:     videos/_2021/newton_fractal.py (lines 497-637)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CurvesDefiningFonts.py CurvesDefiningFonts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CurvesDefiningFonts(Scene):
    def construct(self):
        # Setup
        frame = self.camera.frame

        chars = OldTexText("When a computer\\\\renders text...")[0]
        chars.set_width(FRAME_WIDTH - 3)
        filled_chars = chars.copy()
        filled_chars.insert_n_curves(50)
        chars.set_stroke(WHITE, 0.5)
        chars.set_fill(opacity=0.0)

        dot_groups = VGroup()
        line_groups = VGroup()
        for char in chars:
            dots = VGroup()
            lines = VGroup()
            for a1, h, a2 in char.get_bezier_tuples():
                for pair in (a1, h), (h, a2):
                    lines.add(Line(
                        *pair,
                        stroke_width=0.25,
                        # dash_length=0.0025,
                        stroke_color=YELLOW,
                    ))
                for point in (a1, h, a2):
                    dots.add(Dot(point, radius=0.005))
            dot_groups.add(dots)
            line_groups.add(lines)

        dot_groups.set_fill(BLUE, opacity=0)

        self.play(ShowIncreasingSubsets(filled_chars, run_time=1, rate_func=linear))
        self.wait()

        # Zoom in on one letter
        char_index = 2
        char = chars[char_index]
        lines = line_groups[char_index]
        dots = dot_groups[char_index]
        char.refresh_bounding_box()
        frame.generate_target()
        frame.target.set_height(char.get_height() * 2)
        frame.target.move_to(char.get_bottom(), DOWN)
        frame.target.shift(0.1 * char.get_height() * DOWN)
        self.play(
            MoveToTarget(frame),
            filled_chars.animate.set_opacity(0.2),
            FadeIn(chars),
            ShowCreation(line_groups, rate_func=linear),
            dot_groups.animate.set_opacity(1),
            run_time=5,
        )
        for group in (line_groups, dot_groups):
            group.remove(*group[0:char_index - 1])
            group.remove(*group[char_index + 2:])
        self.wait()

        # Pull out one curve
        char.become(CurvesAsSubmobjects(char))

        index = 26
        curve = char[index]
        sublines = lines[2 * index:2 * index + 2]
        subdots = dots[3 * index:3 * index + 3]

        curve_group = VGroup(curve, sublines, subdots)
        curve_group.set_stroke(background=True)
        curve_group.generate_target()
        curve_group.save_state()
        curve_group.target.scale(3)
        curve_group.target.next_to(frame.get_top(), DOWN, buff=0.15)
        curve_group.target.shift(0.3 * LEFT)
        for dot in curve_group.target[2]:
            dot.scale(1 / 2)

        labels = VGroup(*(
            OldTex(f"P_{i}").set_height(0.05)
            for i in range(3)
        ))
        for label, dot, vect in zip(labels, curve_group.target[2], [LEFT, UP, UP]):
            label.insert_n_curves(20)
            label.next_to(dot, vect, buff=0.025)
            label.match_color(dot)

        self.play(
            MoveToTarget(curve_group),
            *(
                GrowFromPoint(label, curve_group.get_center())
                for label in labels
            )
        )

        equation = OldTex(
            "(1-t)^{2} P_0 +2(1-t)t P_1 +t^2 P_2",
            tex_to_color_map={
                "P_0": BLUE,
                "P_1": BLUE,
                "P_2": BLUE,
            }
        )
        equation.set_height(0.07)
        equation.next_to(curve_group, RIGHT, buff=0.25)
        equation.insert_n_curves(20)

        poly_label = Text("Polynomial")
        poly_label.insert_n_curves(20)
        poly_label.set_width(2)
        poly_label.apply_function(
            lambda p: [
                p[0],
                p[1] - 0.2 * p[0]**2,
                p[2],
            ]
        )
        poly_label.rotate(30 * DEGREES)
        poly_label.match_height(curve_group)
        poly_label.scale(0.8)
        poly_label.move_to(curve, DR)
        poly_label.shift(0.01 * UL)

        self.play(
            ShowCreationThenDestruction(curve.copy().set_color(PINK), run_time=2),
            Write(poly_label, stroke_width=0.5)
        )
        self.play(
            LaggedStart(*(
                TransformFromCopy(
                    labels[i],
                    equation.get_part_by_tex(f"P_{i}").copy(),
                    remover=True
                )
                for i in range(3)
            )),
            FadeIn(equation, rate_func=squish_rate_func(smooth, 0.5, 1)),
            run_time=2,
        )
        self.wait()
        self.add(curve_group.copy())
        self.play(Restore(curve_group))
        self.wait()
