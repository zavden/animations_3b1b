# ==============================================================================
# Scene:      SphereExample100
# Source:     videos/_2022/visual_proofs/lies.py (lines 388-390)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SphereExample100.py SphereExample100 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve t_range=(0, PI/2) -> (0, PI/2, 0.01): requires 3 values
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2022/visual_proofs/make_lies_images.py
#   - _lib/assets/raster_images/SimpleSphereQuestion.png
# ==============================================================================

from manim_imports_ext import *

EQUATOR_STYLE = dict(stroke_color=TEAL, stroke_width=2)


def get_sphere_slices(radius=1.0, n_slices=20):
    delta_theta = TAU / n_slices
    north_slices = Group(*(
        ParametricSurface(
            uv_func=lambda u, v: [
                radius * math.sin(v) * math.cos(u),
                radius * math.sin(v) * math.sin(u),
                radius * math.cos(v),
            ],
            u_range=[theta, theta + delta_theta],
            v_range=[0, PI / 2],
            resolution=(4, 25),
        )
        for theta in np.arange(0, TAU, delta_theta)
    ))
    north_slices.set_x(0)
    color_slices(north_slices)

    equator = Circle(**EQUATOR_STYLE)
    equator.insert_n_curves(100)
    equator.match_width(north_slices)
    equator.move_to(ORIGIN)
    equator.apply_depth_test()

    return Group(north_slices, get_south_slices(north_slices, dim=2), equator)


def get_flattened_slices(radius=1.0, n_slices=20, straightened=True):
    slc = ParametricSurface(
        # lambda u, v: [u * v, 1 - v, 0],
        lambda u, v: [u * math.sin(v * PI / 2), 1 - v, 0],
        u_range=[-1, 1],
        v_range=[0, 1],
        resolution=(4, 25),
    )
    slc.set_width(TAU / n_slices, stretch=True)
    slc.set_height(radius * PI / 2)
    north_slices = slc.get_grid(1, n_slices, buff=0)
    north_slices.move_to(ORIGIN, DOWN)
    color_slices(north_slices)
    equator = Line(
        north_slices.get_corner(DL), north_slices.get_corner(DR),
        **EQUATOR_STYLE,
    )

    return Group(north_slices, get_south_slices(north_slices, dim=1), equator)


def color_slices(slices, colors=(BLUE_D, BLUE_E)):
    for slc, color in zip(slices, it.cycle([BLUE_D, BLUE_E])):
        slc.set_color(color)
    return slices


def get_south_slices(north_slices, dim):
    ss = north_slices.copy().stretch(-1, dim, about_point=ORIGIN)
    for slc in ss:
        slc.reverse_points()
    return ss


class SphereExample(InteractiveScene):
    radius = 2.0
    n_slices = 20
    slice_stroke_width = 1.0
    # show_true_slices = False
    show_true_slices = True

    def construct(self):
        # Setup
        frame = self.camera.frame
        frame.set_focal_distance(100)
        light = self.camera.light_source
        light.move_to([-10, 2, 5])

        # Create the sphere
        img_path = "/Users/grant/Dropbox/3Blue1Brown/videos/2022/visual_proofs/lies/images/SimpleSphereQuestion.png"
        radius = 2.5
        sphere = TexturedSurface(Sphere(radius=radius), img_path)
        sphere.set_opacity(1.0)
        sphere.rotate(91 * DEGREES, OUT).rotate(80 * DEGREES, LEFT)
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(BLUE_B, 1, 0.5)
        banner = TexturedSurface(Surface(resolution=sphere.resolution), img_path)
        banner.set_width(FRAME_WIDTH)
        banner.set_height(FRAME_WIDTH / 4, stretch=True)
        banner.center()
        banner.set_gloss(0)
        banner.set_reflectiveness(0)
        banner.set_shadow(0)

        self.add(banner)
        self.play(ReplacementTransform(banner, sphere, run_time=2))
        self.play(Write(mesh, run_time=1))
        self.wait()

        # Slice sphere
        slices = get_sphere_slices(n_slices=self.n_slices)
        slices.rotate(90 * DEGREES, OUT).rotate(80 * DEGREES, LEFT)
        slices.scale(radius)
        slice_highlights = slices[0][len(slices[0]) // 4:3 * len(slices[0]) // 4].copy().set_color(YELLOW)
        slice_highlights.scale(1.01, about_point=ORIGIN)

        flat_slices = get_flattened_slices(n_slices=self.n_slices)
        flat_slices.to_edge(RIGHT, buff=1.0)

        self.play(
            FadeIn(slices),
            FadeOut(sphere, lag_ratio=0, scale=0.95),
            FadeOut(mesh, lag_ratio=0, scale=0.95),
        )
        self.play(LaggedStart(*(
            FadeIn(sh, rate_func=there_and_back)
            for sh in slice_highlights
        ), lag_ratio=0.35, run_time=1.5))
        self.remove(slice_highlights)
        self.wait()

        # Unfold sphere
        self.play(slices.animate.scale(1 / radius).to_corner(UL).shift(IN))
        pre_slices = slices.copy()
        self.add(pre_slices, slices)
        for slcs in pre_slices:
            for slc in slcs:
                slc.set_color(interpolate_color(slc.get_color(), BLACK, 0.0))
        flat_slices[2].shift(0.01 * OUT)
        self.play(
            Transform(slices[0], flat_slices[0]),
            Transform(slices[2], flat_slices[2]),
            run_time=2,
        )
        self.wait()
        self.play(
            Transform(
                slices[1], flat_slices[1],
                run_time=2,
            ),
        )
        self.wait()

        # Show width line
        slc = flat_slices[0][0]
        v_tracker = ValueTracker(0)
        width_line = Line(LEFT, RIGHT)
        width_line.set_stroke(RED, 3)

        def update_width_line(width_line, slc=slc, v_tracker=v_tracker):
            v = v_tracker.get_value()
            width_line.set_width(1.2 * slc.get_width() * math.sin(v) + 1e-2)
            width_line.move_to(interpolate(slc.get_top(), slc.get_bottom(), v))

        width_line.add_updater(update_width_line)
        self.add(width_line)
        self.play(v_tracker.animate.set_value(1), run_time=3)
        self.play(v_tracker.animate.set_value(0), run_time=3)
        self.remove(width_line)

        # Interlink
        tri_template = Triangle(start_angle=90 * DEGREES)
        tri_template.set_width(2).set_height(1, stretch=True)
        tri_template.move_to(ORIGIN, DOWN)

        if self.show_true_slices:
            tri_template = VMobject()
            dtheta = TAU / self.n_slices
            # CHANGE: t_range requires (min, max, step)
            curve = ParametricCurve(lambda phi: [-math.sin(phi) * dtheta / 2, PI / 2 - phi, 0], t_range=(0, PI / 2, 0.01))
            curve2 = curve.copy().stretch(-1, 0, about_point=ORIGIN)
            curve2.reverse_points()
            tri_template.append_vectorized_mobject(curve)
            tri_template.add_line_to(curve2.get_start())
            tri_template.append_vectorized_mobject(curve2)

        vslices = VGroup(*(
            VGroup(*(
                tri_template.copy().rotate(rot).replace(slc, stretch=True)
                for slc in hemi
            ))
            for rot, hemi in zip([0, PI], slices)
        ))
        for hemi, vhemi in zip(slices, vslices):
            for slc, vslc in zip(hemi, vhemi):
                vslc.set_fill(slc.get_color(), 1)
                vslc.set_stroke(WHITE, 0)
        slices[2].deactivate_depth_test()
        vslices.add(slices[2].copy())

        vslices[1].move_to(vslices[0][0].get_top(), UL)
        vslices[1].set_stroke(WHITE, self.slice_stroke_width)
        vslices.center()

        self.play(FadeTransformPieces(slices, vslices))
        self.wait()

        if self.show_true_slices:
            self.play(vslices.animate.set_opacity(0.5))

        # Show equator
        circ_label = Text("Circumference")
        circ_label.next_to(vslices[2], DOWN)
        circ_formula = OldTex("2\\pi R")
        circ_formula.next_to(vslices[2], DOWN)
        circ_formula.set_stroke(WHITE, 0)
        equator = pre_slices[2]

        vslices[2].set_stroke()
        self.play(
            Write(circ_label),
            VShowPassingFlash(
                vslices[2].copy().set_stroke(YELLOW, 5).insert_n_curves(20),
                time_width=1.5,
                run_time=1.5,
            ),
            vslices[2].animate.set_color(YELLOW),
        )
        self.play(equator.animate.shift(1.5 * DOWN).set_color(YELLOW))
        self.wait()
        self.play(equator.animate.shift(1.5 * UP))
        self.wait()
        self.play(
            Write(circ_formula),
            circ_label.animate.next_to(circ_formula, DOWN)
        )
        self.wait()

        # Arc height
        edge = Line(vslices.get_corner(DL), vslices[0][0].get_top())
        edge.set_stroke(PINK, 2)
        q_marks = OldTex("???")
        q_marks.next_to(edge.get_center(), LEFT, SMALL_BUFF)
        arc = Arc(0, 90 * DEGREES)
        arc.match_style(edge)
        arc.set_height(pre_slices.get_height() / 2)
        arc.rotate(-10 * DEGREES, LEFT)
        arc.shift(pre_slices[0][0].get_points()[0] - arc.get_end())

        arc_form = OldTex("{\\pi \\over 2} R")
        arc_form.scale(0.5)
        arc_form.next_to(arc.pfp(0.5), RIGHT)
        arc_form2 = arc_form.copy()
        arc_form2.scale(1.5)
        arc_form2.move_to(q_marks, RIGHT)

        self.play(
            ShowCreation(edge),
            Write(q_marks),
        )
        self.play(WiggleOutThenIn(edge, run_time=1))
        self.wait()
        self.play(TransformFromCopy(edge, arc))
        self.play(Write(arc_form))
        self.wait()
        self.play(
            TransformFromCopy(arc_form, arc_form2),
            FadeOut(q_marks, DOWN)
        )
        self.wait()

        # Area
        arc_tex = "{\\pi \\over 2} R"
        circ_tex = "2\\pi R"
        eq_parts = ["\\text{Area}", "=", arc_tex, "\\times", circ_tex, "=", "\\pi^2 R^2"]
        equation = Tex(" ".join(eq_parts), isolate=eq_parts)
        equation.center().to_edge(UP, buff=LARGE_BUFF)
        rect = SurroundingRectangle(equation.select_parts(eq_parts[-1]))
        rect.set_stroke(YELLOW, 2)

        self.play(
            Write(equation.select_parts("\\text{Area}")),
            Write(equation.select_parts("=")[0]),
            Write(equation.select_parts("\\times")),
            TransformFromCopy(arc_form2, equation.select_parts(arc_tex)),
            TransformFromCopy(circ_formula, equation.select_parts(circ_tex)),
        )
        self.wait()
        self.play(
            Write(equation.select_parts("=")[1]),
            Write(equation.select_parts("\\pi^2 R^2")),
        )
        self.play(ShowCreation(rect))
        self.wait()


class SphereExample100(SphereExample):
    n_slices = 100
    slice_stroke_width = 0.1
