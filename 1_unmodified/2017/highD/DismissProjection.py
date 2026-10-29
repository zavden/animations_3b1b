# ==============================================================================
# Scene:      DismissProjection
# Source:     videos/_2017/highD.py (lines 816-970)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DismissProjection.py DismissProjection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DismissProjection(PiCreatureScene):
    CONFIG = { 
        "screen_rect_color" : WHITE,
        "example_vect" : np.array([0.52, 0.26, 0.53, 0.60]),
    }
    def construct(self):
        self.remove(self.pi_creature)
        self.show_all_spheres()
        self.discuss_4d_sphere_definition()
        self.talk_through_animation()
        self.transition_to_next_scene()
        
    def show_all_spheres(self):
        equations = VGroup(*list(map(Tex, [
            "x^2 + y^2 = 1",
            "x^2 + y^2 + z^2 = 1",
            "x^2 + y^2 + z^2 + w^2 = 1",
        ])))
        colors = [YELLOW, GREEN, BLUE]
        for equation, edge, color in zip(equations, [LEFT, ORIGIN, RIGHT], colors):
            equation.set_color(color)
            equation.shift(3*UP)
            equation.to_edge(edge)
        equations[1].shift(LEFT)

        spheres = VGroup(
            self.get_circle(equations[0]),
            self.get_sphere_screen(equations[1], DOWN),
            self.get_sphere_screen(equations[2], DOWN),
        )
        
        for equation, sphere in zip(equations, spheres):
            self.play(
                Write(equation),
                LaggedStartMap(ShowCreation, sphere),
            )
        self.wait()

        self.equations = equations
        self.spheres = spheres

    def get_circle(self, equation):
        result = VGroup(
            NumberPlane(
                x_radius = 2.5,
                y_radius = 2,
            ).fade(0.4),
            Circle(color = YELLOW, radius = 1),
        )
        result.scale(0.7)
        result.next_to(equation, DOWN)
        return result

    def get_sphere_screen(self, equation, vect):
        square = Rectangle()
        square.set_width(equation.get_width())
        square.stretch_to_fit_height(3)
        square.next_to(equation, vect)
        square.set_color(self.screen_rect_color)
        return square

    def discuss_4d_sphere_definition(self):
        sphere = self.spheres[-1]
        equation = self.equations[-1]

        sphere_words = OldTexText("``4-dimensional sphere''")
        sphere_words.next_to(sphere, DOWN+LEFT, buff = LARGE_BUFF)
        arrow = Arrow(
            sphere_words.get_right(), sphere.get_bottom(), 
            path_arc = np.pi/3, 
            color = BLUE
        )
        descriptor = OldTex(
            "\\text{Just lists of numbers like }", 
            "(%.02f \\,, %.02f \\,, %.02f \\,, %.02f \\,)"%tuple(self.example_vect)
        )
        descriptor[1].set_color(BLUE)
        descriptor.next_to(sphere_words, DOWN)
        dot = Dot(descriptor[1].get_top())
        dot.set_fill(WHITE, opacity = 0.75)

        self.play(
            Write(sphere_words),
            ShowCreation(
                arrow,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            run_time = 3,
        )
        self.wait()
        self.play(Write(descriptor, run_time = 2))
        self.wait()
        self.play(
            dot.move_to, equation.get_left(),
            dot.set_fill, None, 0,
            path_arc = -np.pi/12
        )
        self.wait(2)

        self.sphere_words = sphere_words
        self.sphere_arrow = arrow
        self.descriptor = descriptor

    def talk_through_animation(self):
        sphere = self.spheres[-1]

        morty = self.pi_creature
        alt_dims = VGroup(*list(map(TexText, ["5D", "6D", "7D"])))
        alt_dims.next_to(morty.eyes, UP, SMALL_BUFF)
        alt_dim = alt_dims[0]

        self.play(FadeIn(morty))
        self.play(morty.change, "raise_right_hand", sphere)
        self.wait(3)
        self.play(morty.change, "confused", sphere)
        self.wait(3)
        self.play(
            morty.change, "erm", alt_dims,
            FadeIn(alt_dim)
        )
        for new_alt_dim in alt_dims[1:]:
            self.wait()
            self.play(Transform(alt_dim, new_alt_dim))
        self.wait()
        self.play(morty.change, "concerned_musician")
        self.play(FadeOut(alt_dim))
        self.wait()
        self.play(morty.change, "angry", sphere)
        self.wait(2)

    def transition_to_next_scene(self):
        equation = self.equations[-1]
        self.equations.remove(equation)
        tup = self.descriptor[1]
        self.descriptor.remove(tup)

        equation.generate_target()
        equation.target.center().to_edge(UP)
        tup.generate_target()
        tup.target.next_to(equation.target, DOWN)
        tup.target.set_color(WHITE)

        self.play(LaggedStartMap(FadeOut, VGroup(*[
            self.equations, self.spheres,
            self.sphere_words, self.sphere_arrow,
            self.descriptor,
            self.pi_creature
        ])))
        self.play(*list(map(MoveToTarget, [equation, tup])))
        self.wait()

    ###

    def create_pi_creature(self):
        return Mortimer().scale(0.8).to_corner(DOWN+RIGHT)
