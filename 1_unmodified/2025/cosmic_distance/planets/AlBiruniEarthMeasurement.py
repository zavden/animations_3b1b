# ==============================================================================
# Scene:      AlBiruniEarthMeasurement
# Source:     videos/_2025/cosmic_distance/planets.py (lines 537-670)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlBiruniEarthMeasurement.py AlBiruniEarthMeasurement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AlBiruniEarthMeasurement(InteractiveScene):
    def construct(self):
        # Add earth and mountain
        radius = 2
        height = 0.3

        earth = Circle(radius=radius)
        earth.set_fill(BLUE_B, 0.5)
        earth.set_stroke(WHITE, 3)
        earth.rotate(90 * DEG)

        earth_pattern = SVGMobject("earth")
        earth_pattern.rotate(90 * DEG)
        earth_pattern.replace(earth)
        earth_pattern.set_fill(Color(hsl=(0.23, 0.5, 0.2)), 1)

        mountain_tip = earth.get_top() + height * UP
        mountain = Polyline(
            earth.pfp(0.02), mountain_tip, earth.pfp(0.98)
        )
        mountain.set_stroke(GREY_B, 4)

        self.add(earth)
        self.add(earth_pattern)
        self.add(mountain)

        # Show line of sight
        theta = math.acos(radius / (radius + height))
        line_length = 3

        line_of_sight = DashedLine(ORIGIN, line_length * RIGHT, dash_length=DEFAULT_DASH_LENGTH / 2)
        line_of_sight.set_stroke(WHITE, 2)
        line_of_sight.rotate(-theta, about_point=ORIGIN)
        line_of_sight.shift(mountain_tip)

        horizontal = Line(mountain_tip, mountain_tip + line_length * RIGHT)
        horizontal.set_stroke(WHITE, 2)
        horizontal_copy = horizontal.copy()

        arc = Arc(0, -theta, arc_center=mountain_tip, radius=0.5)
        theta_label = Tex(R"\theta", font_size=24)
        theta_label.next_to(arc, RIGHT, SMALL_BUFF)

        self.play(ShowCreation(line_of_sight))
        self.wait()
        self.play(ShowCreation(horizontal))
        self.play(
            Rotate(horizontal_copy, -theta, about_point=mountain_tip),
            ShowCreation(arc),
            Write(theta_label)
        )
        self.play(FadeOut(horizontal_copy))
        self.wait()

        # Show radius of the earth
        radius_line = Line(earth.get_center(), earth.get_top())
        radius_line.rotate(-theta, about_point=earth.get_center())
        radius_line.set_stroke(WHITE, 4)
        R_label = Tex(R"R", font_size=36)
        R_label.next_to(radius_line.get_center(), DR, buff=0.05)

        self.play(
            earth_pattern.animate.set_fill(opacity=0.5),
            earth.animate.set_fill(opacity=0.2),
            ShowCreation(radius_line),
            Write(R_label),
        )
        self.wait()

        # Show triangle
        elbow = Elbow(angle=180 * DEG - theta)
        elbow.shift(radius_line.get_end())
        hyp = Line(earth.get_center(), mountain_tip)
        hyp.set_stroke(RED, 3)
        hyp_brace = Brace(hyp, LEFT, buff=0.1)
        hyp_label = hyp_brace.get_tex("R + h", font_size=36)

        self.play(
            ShowCreation(elbow),
            ShowCreation(hyp),
        )
        self.wait()
        self.play(
            GrowFromCenter(hyp_brace),
            Write(hyp_label),
        )
        self.wait()

        # Show angle
        low_arc = Arc(90 * DEG, -theta, arc_center=earth.get_center(), radius=0.5)
        low_theta_label = theta_label.copy()
        low_theta_label.next_to(low_arc.pfp(0.6), UP, buff=0.075)

        self.play(FlashAround(theta_label))
        self.play(
            TransformFromCopy(arc, low_arc),
            TransformFromCopy(theta_label, low_theta_label),
        )
        self.wait()

        # Show the equation
        frame = self.frame
        equation = Tex(R"R = (R + h)\cos(\theta)", font_size=36)
        equation.to_edge(UP, buff=0)

        self.play(
            frame.animate.shift(UP),
            LaggedStart(
                TransformFromCopy(R_label, equation["R"][0]),
                Write(equation["= ("][0]),
                TransformFromCopy(hyp_label, equation["R + h"][0]),
                Write(equation[R")\cos("][0]),
                TransformFromCopy(low_theta_label, equation[R"\theta"][0]),
                Write(equation[")"][-1]),
                lag_ratio=0.25
            )
        )
        self.wait()

        # Simplify
        eq2 = Tex(R"R - R \cos(\theta) = h \cos(\theta)", font_size=36)
        eq3 = Tex(R"R = {h\cos(\theta) \over 1 - \cos(\theta)}", font_size=36)
        eq2.move_to(equation).shift(0.5 * UP)
        eq3.next_to(eq2, DOWN)
        rect = SurroundingRectangle(eq3)
        rect.set_fill(BLACK, 0.8)

        self.play(equation.animate.next_to(eq2, UP), frame.animate.shift(0.5 * UP))
        self.play(TransformMatchingTex(equation.copy(), eq2, path_arc=45 * DEG, lag_ratio=0.01))
        self.wait()
        self.play(TransformMatchingTex(eq2.copy(), eq3, path_arc=45 * DEG, lag_ratio=0.01))
        self.add(rect, eq3)
        self.play(DrawBorderThenFill(rect))
        self.wait()
