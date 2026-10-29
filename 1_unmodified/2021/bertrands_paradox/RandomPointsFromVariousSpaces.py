# ==============================================================================
# Scene:      RandomPointsFromVariousSpaces
# Source:     videos/_2021/bertrands_paradox.py (lines 346-484)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomPointsFromVariousSpaces.py RandomPointsFromVariousSpaces -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomPointsFromVariousSpaces(Scene):
    def construct(self):
        # Interval
        interval = UnitInterval()
        interval.add_numbers()
        top_words = OldTexText("Choose a random$^{*}$ ", "number between 0 and 1")
        top_words.to_edge(UP)
        subwords = OldTexText(
            "($^{*}$Implicitly: According to a \\emph{uniform} distribution)",
            color=GREY_A,
            tex_to_color_map={"\\emph{uniform}": YELLOW},
            font_size=36
        )
        subwords.next_to(top_words, DOWN, buff=MED_LARGE_BUFF)

        dots = DotCloud([
            interval.n2p(random.random())
            for x in range(100)
        ])
        dots.set_radius(0.5)
        dots.set_glow_factor(10)
        dots.set_color(YELLOW)
        dots.add_updater(lambda m: m)
        turn_animation_into_updater(
            ShowCreation(dots, rate_func=linear, run_time=10)
        )

        self.add(interval, dots)
        self.play(Write(top_words, run_time=1))
        self.wait(2)
        self.play(FadeIn(subwords, 0.5 * DOWN))
        self.wait(6)

        # Circle
        circle = Circle()
        circle.set_stroke(BLUE, 2)
        circle.set_height(5)
        circle.next_to(subwords, DOWN, buff=MED_LARGE_BUFF)
        dots.clear_updaters()
        dots.generate_target(use_deepcopy=True)
        dots.target.set_points([
            circle.pfp(interval.p2n(p))
            for p in dots.get_points()
        ])
        dots.target.set_radius(0)

        circle_words = Text("point on a circle")
        circle_words.move_to(top_words[1], UL)
        circle_words.set_color(BLUE)
        top_words[0].generate_target()
        VGroup(top_words[0].target, circle_words).set_x(0)

        self.play(
            MoveToTarget(dots, run_time=1),
            TransformFromCopy(
                Line(interval.n2p(0), interval.n2p(1)).set_stroke(GREY_B, 1),
                circle,
                run_time=1,
            ),
            FadeOut(interval),
            FadeOut(top_words[1], UP),
            FadeIn(circle_words, UP),
            MoveToTarget(top_words[0]),
        )

        dots.set_points([
            circle.pfp(random.random())
            for x in range(25)
        ])
        dots.set_radius(0.5)
        dots.set_glow_factor(5)
        dots.add_updater(lambda m: m)
        self.add(dots)
        self.play(ShowCreation(dots, rate_func=linear, run_time=2))

        # Sphere
        sphere_words = Text("point on a sphere")
        sphere_words.move_to(circle_words, LEFT)
        sphere_words.set_color(BLUE)

        sphere = Sphere()
        sphere.set_color(BLUE_D)
        sphere.set_opacity(0.5)
        sphere.set_shadow(0.5)
        sphere.set_gloss(0.5)
        sphere.set_reflectiveness(0.5)
        sphere.replace(circle)
        sphere.rotate(0.05 * PI)
        sphere.rotate(0.4 * PI, LEFT)
        sphere.set_sort_to_camera()

        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(WHITE, 1, 0.5)

        self.play(
            FadeOut(dots),
            FadeOut(circle, run_time=2),
            ShowCreation(sphere, run_time=2),
            ShowCreation(mesh, lag_ratio=0.1, run_time=2),
            FadeOut(circle_words, UP),
            FadeIn(sphere_words, UP),
        )

        dots.set_points([
            random.choice(sphere.get_points())
            for x in range(100)
        ])
        dots.set_radius(0.25)
        self.play(ShowCreation(dots, run_time=10, rate_func=linear))

        # Ambiguity
        underline = Underline(
            subwords.get_part_by_tex("uniform"),
            buff=0
        )
        underline.set_stroke(YELLOW, width=[0, 2, 2, 2, 0])
        underline.scale(1.25)
        underline.insert_n_curves(50)
        question = Text("Is this well-defined?")
        question.to_edge(RIGHT).shift(UP)
        arrow = Arrow(underline, question, buff=0.1)
        arrow.set_color(YELLOW)

        turn_animation_into_updater(
            ShowCreation(dots, run_time=10, rate_func=lambda t: 0.5 + 0.5 * t),
        )

        dots.clear_updaters()
        dots.set_points(dots.get_points()[12:16])
        dots.set_radius(0.5)
        dots.add_updater(lambda m: m)

        self.play(
            ShowCreation(underline),
            ShowCreation(arrow),
            FadeIn(question, shift=0.5 * DR),
            ShowCreation(dots, run_time=4, rate_func=linear)
        )
        self.wait()
