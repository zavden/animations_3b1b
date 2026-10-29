# ==============================================================================
# Scene:      NorthEastTraveler
# Source:     videos/_2025/grover/clarification.py (lines 848-968)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NorthEastTraveler.py NorthEastTraveler -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NorthEastTraveler(InteractiveScene):
    def construct(self):
        # Add compass
        compass = self.get_compass()
        compass.move_to(5 * RIGHT + 2.5 * UP)
        self.add(compass)

        # Show travler
        randy = Randolph(height=1, mode="tease")
        vel_vect = Vector(2 * RIGHT, thickness=4, color=YELLOW)
        vel_vect.move_to(randy.get_bottom(), LEFT)
        travler = VGroup(randy, vel_vect)
        travler.rotate(45 * DEG) 
        travler.move_to(4 * LEFT + 2 * DOWN)

        self.add(travler)
        self.play(travler.animate.shift(3 * UR), run_time=5, rate_func=linear)

        # Show components
        components = VGroup(
            Vector(math.sqrt(2) * UP).shift(math.sqrt(2) * RIGHT).set_fill(GREEN),
            Vector(math.sqrt(2) * RIGHT).set_fill(RED)
        )
        components.shift(vel_vect.get_start() - components[1].get_start())
        labels = VGroup(
            Text("North").next_to(components[0], RIGHT, buff=-0.05),
            Text("East").next_to(components[1], DOWN, SMALL_BUFF),
        )

        for component, label in zip(components, labels):
            label.scale(0.75)
            label.match_color(component)
            self.play(
                GrowArrow(component),
                FadeIn(label)
            )
        self.wait()

        # Show sum
        sum_expr = VGroup(labels[0].copy(), Tex(R"+", font_size=24), labels[1].copy())
        sum_expr.arrange(RIGHT, buff=SMALL_BUFF)
        sum_expr.next_to(vel_vect.get_end(), UP)
        self.play(
            TransformFromCopy(labels, sum_expr[0::2]),
            Write(sum_expr[1])
        )
        self.wait()

        # Do a 90 degree rotation
        north_group = VGroup(components[0], labels[0])
        east_group = VGroup(components[1], labels[1])
        self.play(
            FadeOut(sum_expr),
            north_group.animate.shift(DR).fade(0.5),
            east_group.animate.shift(DR).fade(0.5),
        )
        self.wait()

        self.add(travler.copy().fade(0.75))
        t_rot_marks = self.show_90_degree_rotation(travler, 45 * DEG, about_point=vel_vect.get_start())
        self.wait()

        self.play(
            north_group.animate.set_fill(opacity=1).shift(UR),
            FadeOut(t_rot_marks)
        )
        n_rot_marks = self.show_90_degree_rotation(components[0], 90 * DEG, about_point=components[0].get_start())
        self.wait()
        self.play(
            east_group.animate.set_fill(opacity=1).shift(DR + DOWN)
        )
        e_rot_marks = self.show_90_degree_rotation(components[1], 0, about_point=components[1].get_start())

        self.add(components.copy().set_opacity(0.5))
        self.play(components[1].animate.shift(vel_vect.get_start() - components[1].get_start()))
        self.play(components[0].animate.shift(components[1].get_end() - components[0].get_start()))
        self.wait()
        self.play(LaggedStart(*(
            Rotate(mob, -90 * DEG, about_point=vel_vect.get_start(), run_time=6, rate_func=there_and_back_with_pause)
            for mob in [travler, *components]
        ), lag_ratio=0.05))

    def get_compass(self):
        spike = Triangle()
        spike.set_shape(0.25, 1)
        spike.move_to(ORIGIN, DOWN)
        spikes = VGroup(
            spike.copy().rotate(x * TAU / 4, about_point=ORIGIN)
            for x in range(4)
        )
        lil_spikes = spikes.copy().rotate(45 * DEG).scale(0.75)
        dot = Circle(radius=0.25)
        compass = VGroup(spikes, lil_spikes, dot)
        compass.set_stroke(width=0)
        compass.set_fill(GREY_D, 1)
        compass.set_shading(0.5, 0.5, 1)

        labels = VGroup(map(Text, "NWSE"))
        labels.scale(0.5)
        for label, spike, vect in zip(labels, spikes, compass_directions(4, start_vect=UP)):
            label.next_to(spike, np.round(vect), SMALL_BUFF)
        compass.add(labels)

        return compass

    def show_90_degree_rotation(self, mobject, start_angle, about_point, radius=1.5):
        arc = Arc(start_angle, 90 * DEG, arc_center=about_point, radius=radius)
        arc.add_tip(width=0.2, length=0.2)
        arc.set_color(YELLOW)
        label = Tex(R"90^\circ")
        midpoint = arc.pfp(0.5)
        label.next_to(midpoint, normalize(midpoint - about_point))

        self.play(LaggedStart(
            ShowCreation(arc),
            FadeIn(label),
            Rotate(mobject, 90 * DEG, about_point=about_point),
            lag_ratio=0.5
        ))

        return VGroup(arc, label)
