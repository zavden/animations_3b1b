# ==============================================================================
# Scene:      ShowArrayOfEccentricities
# Source:     videos/_2018/dandelin.py (lines 322-442)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowArrayOfEccentricities.py ShowArrayOfEccentricities -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowArrayOfEccentricities(Scene):
    def construct(self):
        eccentricities = np.linspace(0, 0.99, 6)
        eccentricity_labels = VGroup(*list(map(
            DecimalNumber, eccentricities
        )))
        ellipses = self.get_ellipse_row(eccentricities)
        ellipses.set_color_by_gradient(BLUE, YELLOW)
        ellipses.move_to(DOWN)

        for label, ellipse in zip(eccentricity_labels, ellipses):
            label.next_to(ellipse, UP)

        name = OldTexText("Eccentricity")
        name.scale(1.5)
        name.to_edge(UP)
        alt_name = OldTexText("(read ``squishification'')")
        alt_name.set_color(YELLOW)
        alt_name.next_to(name, RIGHT)
        alt_name.shift_onto_screen()
        name.generate_target()
        name.target.next_to(alt_name, LEFT)

        arrows = VGroup(*[
            Arrow(name.get_bottom(), label.get_top())
            for label in eccentricity_labels
        ])
        arrows.set_color_by_gradient(BLUE, YELLOW)

        for label, arrow in zip(eccentricity_labels, arrows):
            label.save_state()
            label.fade(1)
            label.scale(0.1)
            label.move_to(arrow.get_start())

        morty = Mortimer(height=2)
        morty.next_to(alt_name, DOWN)

        self.add(ellipses[0])
        for e1, e2 in zip(ellipses[:-1], ellipses[1:]):
            self.play(ReplacementTransform(
                e1.copy(), e2,
                path_arc=10 * DEGREES
            ))
        self.wait()

        self.play(
            Write(name),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(Restore, eccentricity_labels)
        )
        self.wait()
        self.play(
            Write(alt_name),
            MoveToTarget(name),
            morty.change, "hooray", alt_name,
            VFadeIn(morty),
        )
        self.play(Blink(morty))
        self.play(morty.change, "thinking", ellipses)
        self.wait()
        self.play(Blink(morty))

        for i in 0, -1:
            e_copy = ellipses[i].copy()
            e_copy.set_color(RED)
            self.play(ShowCreation(e_copy))
            self.play(
                ShowCreationThenFadeAround(
                    eccentricity_labels[i],
                ),
                FadeOut(e_copy)
            )
        self.wait()

        circle = ellipses[0]
        group = VGroup(*it.chain(
            eccentricity_labels,
            ellipses[1:],
            arrows,
            name,
            alt_name,
            [morty]
        ))
        self.play(
            LaggedStartMap(FadeOutAndShiftDown, group),
            circle.set_height, 5,
            circle.center,
        )

    def get_ellipse(self, eccentricity, width=2):
        result = Circle(color=WHITE)
        result.set_width(width)
        a = width / 2.0
        c = eccentricity * a
        b = np.sqrt(a**2 - c**2)
        result.stretch(b / a, 1)
        result.shift(c * LEFT)

        result.eccentricity = eccentricity
        return result

    def get_ellipse_row(self, eccentricities, buff=MED_SMALL_BUFF, **kwargs):
        result = VGroup(*[
            self.get_ellipse(e, **kwargs)
            for e in eccentricities
        ])
        result.arrange(RIGHT, buff=buff)
        return result

    def get_eccentricity(self, ellipse):
        """
        Assumes that it's major/minor axes line up
        with x and y axes
        """
        a = ellipse.get_width()
        b = ellipse.get_height()
        if b > a:
            a, b = b, a
        c = np.sqrt(a**2 - b**2)
        return fdiv(c, a)
