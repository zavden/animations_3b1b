# ==============================================================================
# Scene:      ThinkBackToHowAmazingThisIs
# Source:     videos/_2018/basel/basel2.py (lines 3796-3901)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThinkBackToHowAmazingThisIs.py ThinkBackToHowAmazingThisIs -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - camera.rotation_mobject does not exist (not even in manim_3feb): the zoom out is a dummy point moved OUT by a ContinualMovement that drives the GL frame height
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class ThinkBackToHowAmazingThisIs(ThreeDScene):
    CONFIG = {
        "x_radius" : 100,
        "max_shown_n" : 20,
    }
    def construct(self):
        self.show_sum()
        self.show_giant_circle()

    def show_sum(self):
        number_line = NumberLine(
            x_min = -self.x_radius, 
            x_max = self.x_radius,
            numbers_to_show = list(range(-self.max_shown_n, self.max_shown_n)),
        )
        number_line.add_numbers()
        number_line.shift(2*DOWN)

        positive_dots, negative_dots = [
            VGroup(*[
                Dot(number_line.number_to_point(u*x))
                for x in range(1, int(self.x_radius), 2)
            ])
            for u in (1, -1)
        ]
        dot_pairs = it.starmap(VGroup, list(zip(positive_dots, negative_dots)))

        # Decimal
        decimal = DecimalNumber(0, num_decimal_places = 6)
        decimal.to_edge(UP)
        terms = [2./(n**2) for n in range(1, 100, 2)]
        partial_sums = np.cumsum(terms)

        # pi^2/4 label
        brace = Brace(decimal, DOWN)
        pi_term = OldTex("\pi^2 \over 4")
        pi_term.next_to(brace, DOWN)

        term_mobjects = VGroup()
        for n in range(1, self.max_shown_n, 2):
            p_term = OldTex("\\left(\\frac{1}{%d}\\right)^2"%n)
            n_term = OldTex("\\left(\\frac{-1}{%d}\\right)^2"%n)
            group = VGroup(p_term, n_term)
            group.scale(0.7)
            p_term.next_to(number_line.number_to_point(n), UP, LARGE_BUFF)
            n_term.next_to(number_line.number_to_point(-n), UP, LARGE_BUFF)
            term_mobjects.add(group)
        term_mobjects.set_color_by_gradient(BLUE, YELLOW)
        plusses = VGroup(*[
            VGroup(*[
                OldTex("+").next_to(
                    number_line.number_to_point(u*n), UP, buff = 1.25,
                )
                for u in (-1, 1)
            ])
            for n in range(0, self.max_shown_n, 2)
        ])

        # CHANGE: camera.rotation_mobject does not exist (not even in manim_3feb): the zoom out is a dummy point moved OUT by a ContinualMovement that drives the GL frame height
        zoom_point = VectorizedPoint()
        zoom_out = ContinualMovement(zoom_point, direction = OUT, rate = 0.4)
        def update_decimal(decimal):
            z = zoom_point.get_center()[2]
            # the old camera had a 3D position (camera.rotation_mobject); moving it OUT is a zoom out of the frame here
            self.frame.set_height(FRAME_HEIGHT * (1 + z/20.0))
            decimal.set_height(max(0.07*z, 1e-2))
            decimal.move_to(0.7*z*UP)
        scale_decimal = Mobject.add_updater(decimal, update_decimal)


        self.add(number_line, *dot_pairs)
        self.add(zoom_out, scale_decimal)

        tuples = list(zip(term_mobjects, plusses, partial_sums))
        run_time = 1
        for term_mobs, plus_pair, partial_sum in tuples:
            self.play(
                FadeIn(term_mobs),
                Write(plus_pair, run_time = 1),
                ChangeDecimalToValue(decimal, partial_sum),
                run_time = run_time
            )
            self.wait(run_time)
            run_time *= 0.9
        self.play(ChangeDecimalToValue(decimal, np.pi**2/4, run_time = 5))
        zoom_out.begin_wind_down()
        self.wait()
        self.remove(zoom_out, scale_decimal)
        self.play(*list(map(FadeOut, it.chain(
            term_mobjects, plusses, 
            number_line.numbers, [decimal]
        ))))

        self.number_line = number_line

    def show_giant_circle(self):
        self.number_line.insert_n_curves(10000)
        everything = VGroup(*self.mobjects)
        circle = everything.copy()
        circle.move_to(ORIGIN)
        circle.apply_function(
            lambda x_y_z : complex_to_R3(7*np.exp(complex(0, 0.0315*x_y_z[0])))
        )
        circle.rotate(-TAU/4, about_point = ORIGIN)
        circle.center()

        self.play(Transform(everything, circle, run_time = 6))
