# ==============================================================================
# Scene:      ShowManyGraphs
# Source:     videos/_2021/newton_fractal.py (lines 1010-1390)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl ShowManyGraphs.py ShowManyGraphs -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Coco_logo.png (placeholder; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/quintic/roots_and_coefs.py -----

def roots_to_coefficients(roots):
    n = len(list(roots))
    return [
        ((-1)**(n - k)) * sum(
            np.prod(tup)
            for tup in it.combinations(roots, n - k)
        )
        for k in range(n)
    ] + [1]


def poly(x, coefs):
    return sum(coefs[k] * x**k for k in range(len(coefs)))


def dpoly(x, coefs):
    return sum(k * coefs[k] * x**(k - 1) for k in range(1, len(coefs)))


def find_root(func, dfunc, seed=complex(1, 1), tol=1e-8, max_steps=100):
    # Use newton's method
    last_seed = np.inf
    for n in range(max_steps):
        if abs(seed - last_seed) < tol:
            break
        last_seed = seed
        seed = seed - func(seed) / dfunc(seed)
    return seed


def coefficients_to_roots(coefs):
    if len(coefs) == 0:
        return []
    elif coefs[-1] == 0:
        return coefficients_to_roots(coefs[:-1])
    roots = []
    # Find a root, divide out by (x - root), repeat
    for i in range(len(coefs) - 1):
        root = find_root(
            lambda x: poly(x, coefs),
            lambda x: dpoly(x, coefs),
        )
        roots.append(root)
        new_reversed_coefs, rem = np.polydiv(coefs[::-1], [1, -root])
        coefs = new_reversed_coefs[::-1]
    return roots



# ----- From _2021/newton_fractal.py -----

class ShowManyGraphs(Scene):
    def construct(self):
        # Add plots
        root_groups = [
            (-2, 6),
            (-5, 0, 3),
            (-7, -2, 3, 8),
            (-5, 1, 5, complex(0, 1), complex(0, -1)),
        ]
        coef_groups = list(map(roots_to_coefficients, root_groups))
        scalars = [0.5, 0.2, 0.01, -0.01]
        colors = [BLUE_C, BLUE_D, BLUE_B, RED]
        plots = Group(*(
            self.get_plot(coefs, scalar, color)
            for coefs, scalar, color in zip(coef_groups, scalars, colors)
        ))
        plots.arrange_in_grid(v_buff=0.5)
        axes, graphs, root_dots = [
            Group(*(plot[i] for plot in plots))
            for i in range(3)
        ]

        self.play(
            LaggedStartMap(FadeIn, axes, lag_ratio=0.3),
            LaggedStartMap(ShowCreation, graphs, lag_ratio=0.3),
            run_time=3,
        )
        self.play(
            LaggedStart(*(
                FadeIn(dot, scale=0.1)
                for dot in it.chain(*root_dots)
            ), lag_ratio=0.1)
        )

        self.add(plots)
        self.wait()

        quadratic, cubic, quartic, quintic = plots
        for plot in plots:
            plot.save_state()

        # Show quadratic
        kw = {"tex_to_color_map": {
            "{a}": BLUE_B,
            "{b}": BLUE_C,
            "{c}": BLUE_D,
            "{d}": TEAL_E,
            "{e}": TEAL_D,
            "{f}": TEAL_C,
            "{p}": BLUE_B,
            "{q}": BLUE_C,
            "\\text{root}": YELLOW,
            "r_1": YELLOW,
            "r_2": YELLOW,
            "+": WHITE,
            "-": WHITE,
        }}
        quadratic.generate_target()
        quadratic.target.set_height(6)
        quadratic.target.center().to_edge(LEFT)
        equation = OldTex("{a}x^2 + {b}x + {c} = 0", **kw)
        equation.next_to(quadratic.target, UP)
        form = OldTex(
            "r_1, r_2 = {-{b} \\pm \\sqrt{\\,{b}^2 - 4{a}{c}} \\over 2{a}}",
            **kw
        )
        form.next_to(quadratic.target, RIGHT, buff=MED_LARGE_BUFF)
        form_name = Text("Quadratic formula")
        form_name.match_width(form)
        form_name.next_to(form, UP, LARGE_BUFF)

        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(form, RIGHT)
        randy.align_to(quadratic.target, DOWN)
        randy.shift_onto_screen()

        self.play(
            MoveToTarget(quadratic),
            Write(equation),
            *map(FadeOut, plots[1:]),
            FadeIn(randy),
        )
        self.play(randy.change("hooray"))
        self.play(
            TransformMatchingShapes(
                VGroup(*(
                    equation.get_part_by_tex(f"{{{c}}}")
                    for c in "abc"
                )).copy(),
                form,
                lag_ratio=0,
                run_time=2,
            ),
            randy.animate.look_at(form),
            FadeIn(form_name),
            FlashAround(form_name),
        )
        self.play(Blink(randy))
        self.wait()

        # Coco sidenote
        form_group = VGroup(form_name, form)
        form_group.save_state()
        form_group.set_stroke(BLACK, 5, background=True)
        plot_group = Group(quadratic, equation)
        plot_group.save_state()

        self.play(
            plot_group.animate.shift(4 * LEFT).set_opacity(0),
            form_group.animate.to_corner(UR),
            FadeOut(randy),
        )

        pixar_image = ImageMobject("PixarCampus")
        pixar_image.set_height(FRAME_HEIGHT + 4)
        pixar_image.to_corner(UL, buff=0)
        pixar_image.shift(LEFT)
        pixar_image.add_updater(lambda m, dt: m.shift(0.1 * dt * LEFT))

        coco_logo = ImageMobject("Coco_logo")
        coco_logo.set_width(4)
        coco_logo.match_y(form)
        coco_logo.to_edge(RIGHT, buff=LARGE_BUFF)
        arrow = Arrow(form.copy().to_edge(LEFT), coco_logo, buff=0.3, stroke_width=10)

        self.add(pixar_image, *self.mobjects)
        self.play(FadeIn(pixar_image))
        self.wait(6)
        self.add(coco_logo, *self.mobjects)
        self.play(
            FadeOut(pixar_image),
            form_group.animate.to_corner(UL),
            FadeIn(randy),
            ShowCreation(arrow),
            FadeIn(coco_logo),
        )

        over_trillion = OldTex("> 1{,}000{,}000{,}000{,}000")[0]
        over_trillion.next_to(form, RIGHT)
        over_trillion.shift(3 * DOWN)
        form_copies = form[4:].replicate(50)
        self.play(
            ShowIncreasingSubsets(over_trillion, run_time=1),
            randy.change("thinking", over_trillion),
            LaggedStart(*(
                FadeOut(form_copy, 4 * DOWN)
                for form_copy in form_copies
            ), lag_ratio=0.15, run_time=5)
        )
        self.play(
            FadeOut(over_trillion),
            FadeOut(coco_logo),
            FadeOut(arrow),
            randy.change("happy"),
            Restore(form_group),
            Restore(plot_group),
        )

        self.embed()

        # Cubic
        low_fade_rect = BackgroundRectangle(
            Group(quartic, quintic),
            buff=0.01,
            fill_opacity=0.95,
        )
        cubic_eq = OldTex("x^3 + {p}x + {q} = 0", **kw)
        cubic_eq.next_to(cubic, LEFT, LARGE_BUFF, aligned_edge=UP)
        cubic_eq.shift_onto_screen()
        cubic_name = OldTexText("Cubic\\\\", "Formula")
        cubic_name.to_corner(UL)
        cubic_form = OldTex(
            "\\text{root}", "=",
            "\\sqrt[3]{\\,-{{q} \\over 2} + \\sqrt{\\, {{q}^2 \\over 4} + {{p}^3 \\over 27}} }+",
            "\\sqrt[3]{\\,-{{q} \\over 2} - \\sqrt{\\, {{q}^2 \\over 4} + {{p}^3 \\over 27}} }",
            **kw,
        )
        cubic_form.set_width(7)
        cubic_form.next_to(cubic_eq, DOWN, buff=1.25)
        cubic_form.to_edge(LEFT)
        cubic_arrow = Arrow(
            cubic_eq, cubic_form,
            stroke_width=5,
            buff=0.1,
        )

        self.add(*plots, randy)
        self.play(
            Restore(quadratic),
            *map(FadeIn, plots[1:]),
            FadeOut(form),
            FadeOut(form_name),
            FadeOut(equation),
            randy.change("plain"),
        )
        self.play(randy.change("erm", cubic))
        self.wait()
        self.play(
            FadeOut(quadratic),
            FadeIn(low_fade_rect),
            Write(cubic_eq),
            FadeIn(cubic_name),
        )
        self.play(
            ShowCreation(cubic_arrow),
            FadeIn(cubic_form, DOWN),
            randy.change("confused", cubic_name),
        )
        self.play(Blink(randy))

        # Quartic
        quartic_name = OldTexText("Quartic ", "Formula")
        quartic_name.move_to(quartic).to_edge(UP)
        cubic_fade_rect = BackgroundRectangle(cubic, buff=0.01, fill_opacity=0.95)
        quartic_eq = OldTex("{a}x^4 + {b}x^3 + {c}x^2 + {d}x + {e} = 0", **kw)
        quartic_eq.next_to(quartic, UP)

        main_form = OldTex(r"r_{i}&=-\frac{b}{4 a}-S \pm \frac{1}{2} \sqrt{-4 S^{2}-2 p \pm \frac{q}{S}}")
        details = OldTex(r"""
            &\text{Where}\\\\
            p&=\frac{8 a c-3 b^{2}}{8 a^{2}} \qquad \qquad\\\\
            q&=\frac{b^{3}-4 a b c+8 a^{2} d}{8 a^{3}}\\\\
            S&=\frac{1}{2} \sqrt{-\frac{2}{3} p+\frac{1}{3 a}\left(Q+\frac{\Delta_{0}}{Q}\right)}\\\\
            Q&=\sqrt[3]{\frac{\Delta_{1}+\sqrt{\Delta_{1}^{2}-4 \Delta_{0}^{3}}}{2}}\\\\
            \Delta_{0}&=c^{2}-3 b d+12 a e\\\\
            \Delta_{1}&=2 c^{3}-9 b c d+27 b^{2} e+27 a d^{2}-72 a c e\\\\
        """)
        main_form.match_width(quartic_eq)
        main_form.move_to(VGroup(quartic_name, quartic_eq))
        details.scale(0.5)
        details.to_corner(UR)
        details.set_stroke(BLACK, 3, background=True)

        self.play(
            FadeOut(cubic_eq),
            FadeOut(cubic_form),
            FadeOut(cubic_arrow),
            FadeIn(cubic_fade_rect),
            FadeTransform(cubic_name[0], quartic_name[0]),
            FadeTransform(cubic_name[1], quartic_name[1]),
            randy.change("erm", quartic_name),
            low_fade_rect.animate.replace(quintic, stretch=True).scale(1.01),
            FadeIn(quartic_eq),
        )
        self.play(Write(main_form))
        self.wait()
        self.play(
            randy.change("horrified", details),
            Write(details, run_time=5)
        )
        self.play(randy.animate.look_at(details.get_bottom()))
        self.play(Blink(randy))
        self.wait()

        # Quintic
        quintic.generate_target()
        quintic.target.set_height(5)
        quintic.target.to_corner(UL).shift(DOWN)
        quintic_eq = OldTex(
            "{a}x^5 + {b}x^4 + {c}x^3 + {d}x^2 + {e}x + {f}",
            **kw
        )
        quintic_eq.match_width(quintic.target)
        quintic_eq.next_to(quintic.target, UP)
        quintic_name = Text("Quintic formula?", font_size=60)
        quintic_name.move_to(3 * RIGHT)
        quintic_name.to_edge(UP)

        subwords = VGroup(
            OldTexText("There is none.", "$^*$"),
            OldTexText("And there never can be."),
        )

        subwords.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        subwords.next_to(quintic_name, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        footnote = OldTex(
            "^*\\text{Using }",
            "+,\\,",
            "-,\\,",
            "\\times,\\,",
            "/,\\,",
            "\\sqrt[n]{\\quad},\\,",
            "\\text{exp},\\,",
            "\\log,\\,",
            "\\sin,\\,",
            "\\cos,\\,",
            "etc.\\\\",
            font_size=36,
            alignment="",
        )
        footnote.set_color(GREY_A)
        footnote.next_to(subwords, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        footnote.shift_onto_screen(buff=MED_SMALL_BUFF)

        self.play(
            FadeOut(cubic),
            FadeOut(quartic),
            FadeOut(quartic_eq),
            FadeOut(main_form),
            FadeOut(details),
            FadeTransform(quartic_name, quintic_name),
            MoveToTarget(quintic),
            UpdateFromFunc(
                low_fade_rect,
                lambda m: m.replace(quintic, stretch=True),
            ),
            VFadeOut(low_fade_rect),
            randy.change("tease", quintic_name),
            FadeIn(quintic_eq),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeIn(subwords[0][0], 0.5 * DOWN),
            randy.change("erm", subwords),
        )
        self.wait()
        self.play(FadeIn(subwords[1], 0.5 * DOWN))
        self.wait()
        self.play(
            FadeIn(subwords[0][1]),
            LaggedStartMap(FadeIn, footnote, run_time=6, lag_ratio=0.5),
            randy.change("pondering", footnote)
        )
        self.play(Blink(randy))
        self.wait()

    def get_plot(self, coefs, scalar=1.0, color=YELLOW, stroke_width=3, height=3.5, bound=10):
        axes = NumberPlane(
            (-bound, bound, 5), (-bound, bound, 5),
            faded_line_ratio=4,
            background_line_style={
                "stroke_width": 1.0,
                "stroke_color": GREY_A,
            }
        )
        axes.set_height(height)
        axes.add_coordinate_labels(
            x_values=[-5, 0, 5, 10],
            y_values=[-5, 5, 10],
            font_size=16,
            excluding=[],
        )

        def f(x):
            return scalar * poly(x, coefs)

        x_min = binary_search(
            lambda x: abs(f(x)), bound, -bound, 0
        )
        x_max = binary_search(
            lambda x: abs(f(x)), bound, 0, bound,
        )

        graph = axes.get_graph(f, x_range=(x_min, x_max))
        graph.set_stroke(color, stroke_width)

        roots = [
            root.real
            for root in coefficients_to_roots(coefs)
            if np.isclose(root.imag, 0)
        ]

        def get_glow_dot(point):
            result = DotCloud([point] * 10)
            result.set_radii([
                interpolate(0.03, 0.06, t**2)
                for t in np.linspace(0, 1, 10)
            ])
            result.set_opacity(0.2)
            result.set_color(YELLOW)
            return result

        root_dots = Group(*(
            get_glow_dot(axes.c2p(root, 0))
            for root in roots
        ))

        result = Group(axes, graph, root_dots)
        return result
