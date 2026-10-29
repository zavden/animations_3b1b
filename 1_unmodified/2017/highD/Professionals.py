# ==============================================================================
# Scene:      Professionals
# Source:     videos/_2017/highD.py (lines 638-761)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Professionals.py Professionals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Professionals(PiCreatureScene):
    def construct(self):
        self.introduce_characters()
        self.add_equation()
        self.analogies()

    def introduce_characters(self):
        titles = VGroup(*list(map(TexText, [
            "Mathematician",
            "Computer scientist",
            "Physicist",
        ])))
        self.remove(*self.pi_creatures)
        for title, pi in zip(titles, self.pi_creatures):
            title.next_to(pi, DOWN)
            self.play(
                Animation(VectorizedPoint(pi.eyes.get_center())),
                FadeIn(pi),
                Write(title, run_time = 1),
            )
        self.wait()

    def add_equation(self):
        quaternion = OldTex(
            "\\frac{1}{2}", "+", 
            "0", "\\textbf{i}", "+",
            "\\frac{\\sqrt{6}}{4}", "\\textbf{j}", "+",
            "\\frac{\\sqrt{6}}{4}", "\\textbf{k}",
        )
        quaternion.scale(0.7)
        quaternion.next_to(self.mathy, UP)
        quaternion.set_color_by_tex_to_color_map({
            "i" : RED,
            "j" : GREEN,
            "k" : BLUE,
        })

        array = OldTex("[a_1, a_2, \\dots, a_{100}]")
        array.next_to(self.compy, UP)

        kets = OldTex(
            "\\alpha",
            "|\\!\\uparrow\\rangle + ",
            "\\beta",
            "|\\!\\downarrow\\rangle"
        )
        kets.set_color_by_tex_to_color_map({
            "\\alpha" : GREEN,
            "\\beta" : RED,
        })
        kets.next_to(self.physy, UP)


        terms = VGroup(quaternion, array, kets)
        for term, pi in zip(terms, self.pi_creatures):
            self.play(
                Write(term, run_time = 1),
                pi.change, "pondering", term
            )
        self.wait(2)

        self.terms = terms

    def analogies(self):
        examples = VGroup()
        plane = ComplexPlane(
            x_radius = 2.5,
            y_radius = 1.5,
        )
        plane.add_coordinates()
        plane.add(Circle(color = YELLOW))
        plane.scale(0.75)
        examples.add(plane)
        examples.add(Circle())
        examples.arrange(RIGHT, buff = 2)
        examples.to_edge(UP, buff = LARGE_BUFF)
        labels = VGroup(*list(map(TexText, ["2D", "3D"])))

        title = OldTexText("Fly by instruments")
        title.scale(1.5)
        title.to_edge(UP)

        for label, example in zip(labels, examples):
            label.next_to(example, DOWN)
            self.play(
                ShowCreation(example),
                Write(label, run_time = 1)
            )
            example.add(label)
            self.wait()
        self.wait()
        self.play(
            FadeOut(examples),
            self.terms.shift, UP,
            Write(title, run_time = 2)
        )
        self.play(*[
            ApplyMethod(
                pi.change, mode, self.terms.get_left(),
                run_time = 2,
                rate_func = squish_rate_func(smooth, a, a+0.5)
            )
            for pi, mode, a in zip(
                self.pi_creatures, 
                ["confused", "sassy", "erm"],
                np.linspace(0, 0.5, len(self.pi_creatures))
            )
        ])
        self.wait()
        self.play(Animation(self.terms[-1]))
        self.wait(2)

    ######

    def create_pi_creatures(self):
        self.mathy = Mathematician()
        self.physy = PiCreature(color = PINK)
        self.compy = PiCreature(color = PURPLE)
        pi_creatures = VGroup(self.mathy, self.compy, self.physy)
        for pi in pi_creatures:
            pi.scale(0.7)
        pi_creatures.arrange(RIGHT, buff = 3)
        pi_creatures.to_edge(DOWN, buff = LARGE_BUFF)
        return pi_creatures
