# ==============================================================================
# Scene:      MotivateRootsOfUnity
# Source:     videos/_2022/puzzles/subsets.py (lines 2368-2545)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MotivateRootsOfUnity.py MotivateRootsOfUnity -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ComplexPlane(axis_config=dict(unit_size=...)) clashes with Axes' unit_size (TypeError): width/height = 6*unit, 4*unit is given
# ==============================================================================

from manim_imports_ext import *

class MotivateRootsOfUnity(InteractiveScene):
    def construct(self):
        # Add generating function
        pieces = ["f(x)", "="]
        n_range = list(range(0, 7))
        for n in n_range:
            pieces.extend([f"c_{{{n}}}", f"x^{{{n}}}", "+"])
        pieces.extend(["\\cdots"])
        polynomial = OldTex("".join(pieces), isolate=pieces)
        polynomial.to_edge(UP)

        exp_parts = VGroup(*(
            polynomial.get_part_by_tex(f"x^{{{n}}}")
            for n in n_range
        ))

        self.add(polynomial)

        # Add f(-1)
        m1_pieces = [
            p.replace("(x)", "x").replace("x", "\\left(-1\\right)")
            for p in pieces
        ]
        fm1 = OldTex("".join(m1_pieces), isolate=pieces)
        fm1.set_color_by_tex("-1", GREY_B)
        fm1[0].set_color(WHITE)
        fm1[0][2:4].set_color(GREY_B)
        fm1.next_to(polynomial, DOWN, MED_LARGE_BUFF)
        fm1.set_width(polynomial.get_width() + 1.0)
        fm1_powers = fm1[3::3]
        # fm1_coefs = fm1[2::3]

        short_fm1 = Tex(
            "f({-1}) = c_0 - c_1 + c_2 - c_3 + c_4 - c_5 + c_6 - c_7 + c_8 - \\cdots",
            tex_to_color_map={"{-1}": GREY_B}
        )
        short_fm1.scale(fm1[0].get_height() / short_fm1[:5].get_height())
        short_fm1.next_to(fm1, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        # Real number line
        line = NumberLine((-4, 4), unit_size=2)
        line.move_to(2 * DOWN)
        line.add_numbers()

        morty = Mortimer(height=1.5)
        morty.next_to(line, UP, SMALL_BUFF).to_edge(RIGHT, buff=1.5)

        self.play(
            Transform(polynomial.copy(), fm1, lag_ratio=0.01, run_time=2, remover=True),
            Write(line),
            PiCreatureSays(
                morty, OldTexText("Visualize the\\\\rotations", font_size=36),
                bubble_config=dict(width=3, height=2)
            ),
        )
        self.add(fm1)
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("pondering", fm1).shift(UP),
            line.animate.shift(UP),
            FadeOut(VGroup(morty.bubble, morty.bubble.content), 0.5 * UP),
        )

        # Show oscillation
        v1 = Arrow(line.n2p(0), line.n2p(1), buff=0, color=BLUE)
        vm1 = Arrow(line.n2p(0), line.n2p(-1), buff=0, color=RED)
        vect = v1.copy()
        neg1_powers = [
            Tex(f"(-1)^{{{n}}}")
            for n in range(8)
        ]
        for n, neg1_power in enumerate(neg1_powers):
            v = [v1, vm1][n % 2]
            neg1_power.next_to(v, UP)

        power = neg1_powers[0].copy()

        for n in range(7):
            self.play(
                FlashAround(fm1_powers[n]),
                fm1_powers[n].animate.set_color([BLUE, RED][n % 2])
            )
            if n == 0:
                self.play(
                    FadeTransform(fm1_powers[n].copy(), vect),
                    FadeTransform(fm1_powers[n].copy(), power),
                    morty.change("surprised").shift(2 * RIGHT).set_opacity(0),
                )
                self.remove(morty)
            else:
                self.play(
                    Transform(vect, [v1, vm1][n % 2], path_arc=PI),
                    Transform(power, neg1_powers[n], path_arc=PI / 2),
                )
            self.wait()
        self.play(
            Write(fm1[-2:]),
            FadeOut(power),
        )
        self.wait()
        self.play(FadeIn(short_fm1, lag_ratio=0.5, run_time=2))
        self.wait()

        # Bring in complex plane
        plane_unit = 1.75
        # CHANGE: axis_config=dict(unit_size=...) clashes with the unit_size that Axes computes; the size is given with width/height
        plane = ComplexPlane(
            (-3, 3), (-2, 2),
            width=6 * plane_unit,
            height=4 * plane_unit,
        )
        plane.move_to(line.n2p(0) - plane.n2p(0))
        plane.add_coordinate_labels(font_size=24)

        plane_label = Text("Complex plane", font_size=36)
        plane_label.set_backstroke()
        plane_label.next_to(plane.get_corner(UL), DR, SMALL_BUFF)

        self.add(plane, polynomial, vect)
        sf = plane_unit / line.get_unit_size()
        self.play(
            Write(plane, lag_ratio=0.01),
            FadeOut(fm1),
            FadeOut(short_fm1),
            line.animate.scale(sf).set_opacity(0),
            vect.animate.set_color(YELLOW).scale(sf, about_edge=LEFT),
        )
        self.remove(line)
        self.play(Write(plane_label))
        self.wait()

        # Preview roots of unity
        unit_circle = Circle(radius=plane_unit)
        unit_circle.move_to(plane.n2p(0))
        unit_circle.set_stroke(GREY, 2)

        points = [
            plane.n2p(np.exp(complex(0, angle)))
            for angle in np.arange(0, TAU, TAU / 5)
        ]
        dots = GlowDots(points)

        pentagon = Polygon(*points)
        pentagon.set_stroke(TEAL, 1)
        pentagon.set_fill(TEAL, 0.25)
        pentagon.save_state()
        pentagon.set_opacity(0)

        self.add(pentagon, unit_circle, vect, dots)
        self.play(
            ShowCreation(unit_circle),
            ShowCreation(dots)
        )
        self.wait()
        self.play(pentagon.animate.restore())
        self.wait()

        last_rect = VMobject()
        for n in range(14):
            if n == 0:
                continue
            if n < len(exp_parts):
                exp_part = exp_parts[n]
            else:
                exp_part = polynomial[-3:]
            rect = SurroundingRectangle(exp_part, buff=0.05)
            rect.round_corners()
            rect.set_stroke(YELLOW, 2)
            self.play(
                FadeOut(last_rect),
                ShowCreation(rect),
                ApplyMethod(
                    vect.put_start_and_end_on,
                    plane.n2p(0), points[n % 5],
                    path_arc=TAU / 5,
                )
            )
            last_rect = rect
            self.wait()
