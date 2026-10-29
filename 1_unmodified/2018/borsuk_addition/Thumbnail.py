# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/borsuk_addition.py (lines 1211-1236)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/fourier.py, _2018/lost_lecture.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy
# -*- coding: utf-8 -*-
import scipy.integrate
import warnings


# ----- From _2018/lost_lecture.py -----

class ShowEmergingEllipse(Scene):
    CONFIG = {
        "circle_radius": 3,
        "circle_color": BLUE,
        "num_lines": 150,
        "lines_stroke_width": 1,
        "eccentricity_vector": 2 * RIGHT,
        "ghost_lines_stroke_color": GREY_B,
        "ghost_lines_stroke_width": 0.5,
        "ellipse_color": PINK,
    }

    def construct(self):
        circle = self.get_circle()
        e_point = self.get_eccentricity_point()
        e_dot = Dot(e_point, color=YELLOW)
        lines = self.get_lines()
        ellipse = self.get_ellipse()

        fade_rect = FullScreenFadeRectangle()

        line = lines[len(lines) // 5]
        line_dot = Dot(line.get_center(), color=YELLOW)
        line_dot.scale(0.5)

        ghost_line = self.get_ghost_lines(line)
        ghost_lines = self.get_ghost_lines(lines)

        rot_words = OldTexText("Rotate $90^\\circ$ \\\\ about center")
        rot_words.next_to(line_dot, RIGHT)

        elbow = self.get_elbow(line)

        eccentric_words = OldTexText("``Eccentric'' point")
        eccentric_words.next_to(circle.get_center(), DOWN)

        ellipse_words = OldTexText("Perfect ellipse")
        ellipse_words.next_to(ellipse, UP, SMALL_BUFF)

        for text in rot_words, ellipse_words:
            text.add_to_back(text.copy().set_stroke(BLACK, 5))

        shuffled_lines = VGroup(*lines)
        random.shuffle(shuffled_lines.submobjects)

        self.play(ShowCreation(circle))
        self.play(
            FadeIn(e_dot, LEFT),
            Write(eccentric_words, run_time=1)
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, shuffled_lines),
            Animation(VGroup(e_dot, circle)),
            FadeOut(eccentric_words)
        )
        self.add(ghost_lines)
        self.add(e_dot, circle)
        self.wait()
        self.play(
            FadeIn(fade_rect),
            Animation(line),
            GrowFromCenter(line_dot),
            FadeInFromDown(rot_words),
        )
        self.wait()
        self.add(ghost_line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            Animation(rot_words),
            ShowCreation(elbow)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeOut(line_dot),
            FadeOut(rot_words),
            FadeOut(elbow),
            Animation(line),
            Animation(ghost_line)
        )
        self.play(
            LaggedStartMap(MoveToTarget, lines, run_time=4),
            Animation(VGroup(e_dot, circle))
        )
        self.wait()
        self.play(
            ShowCreation(ellipse),
            FadeInFromDown(ellipse_words)
        )
        self.wait()

    def get_circle(self):
        circle = self.circle = Circle(
            radius=self.circle_radius,
            color=self.circle_color
        )
        return circle

    def get_eccentricity_point(self):
        return self.circle.get_center() + self.eccentricity_vector

    def get_lines(self):
        center = self.circle.get_center()
        radius = self.circle.get_width() / 2
        e_point = self.get_eccentricity_point()
        lines = VGroup(*[
            Line(
                e_point,
                center + rotate_vector(radius * RIGHT, angle)
            )
            for angle in np.linspace(0, TAU, self.num_lines)
        ])
        lines.set_stroke(width=self.lines_stroke_width)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        return lines

    def get_ghost_lines(self, lines):
        return lines.copy().set_stroke(
            color=self.ghost_lines_stroke_color,
            width=self.ghost_lines_stroke_width
        )

    def get_elbow(self, line):
        elbow = VGroup(Line(UP, UL), Line(UL, LEFT))
        elbow.set_stroke(width=1)
        elbow.scale(0.2, about_point=ORIGIN)
        elbow.rotate(
            line.get_angle() - 90 * DEGREES,
            about_point=ORIGIN
        )
        elbow.shift(line.get_center())
        return elbow

    def get_ellipse(self):
        center = self.circle.get_center()
        e_point = self.get_eccentricity_point()
        radius = self.circle.get_width() / 2

        # Ellipse parameters
        a = radius / 2
        c = get_norm(e_point - center) / 2
        b = np.sqrt(a**2 - c**2)

        result = Circle(radius=b, color=self.ellipse_color)
        result.stretch(a / b, 0)
        result.move_to(Line(center, e_point))
        return result


class Thumbnail(ShowEmergingEllipse):
    CONFIG = {
        "num_lines": 50,
    }

    def construct(self):
        background = ImageMobject("Feynman_teaching")
        background.set_width(FRAME_WIDTH)
        background.scale(1.05)
        background.to_corner(UR, buff=0)
        background.shift(2 * UP)

        self.add(background)

        circle = self.get_circle()
        circle.set_stroke(width=6)
        circle.set_height(6.5)
        circle.to_corner(UL)
        circle.set_fill(BLACK, 0.9)
        lines = self.get_lines()
        lines.set_stroke(YELLOW, 5)
        lines.set_color_by_gradient(YELLOW, RED)
        ghost_lines = self.get_ghost_lines(lines)
        for line in lines:
            line.rotate(90 * DEGREES)
        ellipse = self.get_ellipse()
        ellipse.set_stroke(BLUE, 6)
        sun = ImageMobject("sun", height=0.5)
        sun.move_to(self.get_eccentricity_point())

        circle_group = VGroup(circle, ghost_lines, lines, ellipse, sun)
        self.add(circle_group)

        l1 = Line(
            circle.point_from_proportion(0.175),
            6.25 * RIGHT + 0.75 * DOWN
        )
        l2 = Line(
            circle.point_from_proportion(0.75),
            6.25 * RIGHT + 2.5 * DOWN
        )
        l2a = VMobject().pointwise_become_partial(l2, 0, 0.56)
        l2b = VMobject().pointwise_become_partial(l2, 0.715, 1)
        expand_lines = VGroup(l1, l2a, l2b)

        expand_lines.set_stroke("RED", 5)
        self.add(expand_lines)
        self.add(circle_group)

        small_group = circle_group.copy()
        small_group.scale(0.2)
        small_group.stretch(1.35, 1)
        small_group.move_to(6.2 * RIGHT + 1.6 * DOWN)
        for mob in small_group:
            if isinstance(mob, VMobject) and mob.get_stroke_width() > 1:
                mob.set_stroke(width=1)
        small_group[0].set_fill(opacity=0.25)
        self.add(small_group)

        title = OldTexText(
            "Feynman's \\\\", "Lost \\\\", "Lecture",
            alignment=""
        )
        title.scale(2.4)
        for part in title:
            part.add_to_back(
                part.copy().set_stroke(BLACK, 12).set_fill(BLACK, 1)
            )
        title.to_corner(UR)
        title[2].to_edge(RIGHT)
        title[1].shift(0.9 * RIGHT)
        title.shift(0.5 * LEFT)
        self.add(title)



# ----- From _2018/fourier.py -----

USE_ALMOST_FOURIER_BY_DEFAULT = True


NUM_SAMPLES_FOR_FFT = 1000


DEFAULT_COMPLEX_TO_REAL_FUNC = lambda z : z.real


def get_fourier_graph(
    axes, time_func, t_min, t_max,
    n_samples = NUM_SAMPLES_FOR_FFT,
    complex_to_real_func = lambda z : z.real,
    color = RED,
    ):
    # N = n_samples
    # T = time_range/n_samples
    time_range = float(t_max - t_min)
    time_step_size = time_range/n_samples
    time_samples = np.vectorize(time_func)(np.linspace(t_min, t_max, n_samples))
    fft_output = np.fft.fft(time_samples)
    frequencies = np.linspace(0.0, n_samples/(2.0*time_range), n_samples//2)
    #  #Cycles per second of fouier_samples[1]
    # (1/time_range)*n_samples
    # freq_step_size = 1./time_range
    graph = VMobject()
    graph.set_points_smoothly([
        axes.coords_to_point(
            x, complex_to_real_func(y)/n_samples,
        )
        for x, y in zip(frequencies, fft_output[:n_samples//2])
    ])
    graph.set_color(color)
    f_min, f_max = [
        axes.x_axis.point_to_number(graph.get_points()[i])
        for i in (0, -1)
    ]
    graph.underlying_function = lambda f : axes.y_axis.point_to_number(
        graph.point_from_proportion((f - f_min)/(f_max - f_min))
    )
    return graph


def get_fourier_transform(
    func, t_min, t_max, 
    complex_to_real_func = DEFAULT_COMPLEX_TO_REAL_FUNC,
    use_almost_fourier = USE_ALMOST_FOURIER_BY_DEFAULT,
    **kwargs ##Just eats these
    ):
    scalar = 1./(t_max - t_min) if use_almost_fourier else 1.0
    def fourier_transform(f):
        z = scalar*scipy.integrate.quad(
            lambda t : func(t)*np.exp(complex(0, -TAU*f*t)),
            t_min, t_max
        )[0]
        return complex_to_real_func(z)
    return fourier_transform


class Thumbnail(Scene):
    def construct(self):
        title = OldTexText("Fourier\\\\", "Visualized")
        title.set_color(YELLOW)
        title.set_stroke(RED, 2)
        title.scale(2.5)
        title.add_background_rectangle()

        def func(t):
            return np.cos(2*TAU*t) + np.cos(3*TAU*t) + np.cos(5*t)
        fourier = get_fourier_transform(func, -5, 5)

        graph = FunctionGraph(func, (-5, 5, 0.01))
        graph.set_color(BLUE)
        fourier_graph = FunctionGraph(fourier, (0, 6, 0.01))
        fourier_graph.set_color(YELLOW)
        for g in graph, fourier_graph:
            g.stretch_to_fit_height(2)
            g.stretch_to_fit_width(10)
            g.set_stroke(width=6)

        pol_graphs = VGroup()
        for f in np.linspace(1.98, 2.02, 5):
            pol_graph = ParametricCurve(
                lambda t : complex_to_R3(
                    (2+np.cos(2*TAU*t)+np.cos(3*TAU*t))*np.exp(-complex(0, TAU*f*t))
                ),
                t_range=(-5, 5, 0.01),
            )
            pol_graph.match_color(graph)
            pol_graph.set_height(2)
            pol_graphs.add(pol_graph)
        pol_graphs.arrange(RIGHT, buff=LARGE_BUFF)
        pol_graphs.set_color_by_gradient(BLUE_C, TEAL, GREEN)
        pol_graphs.match_width(graph)
        pol_graphs.set_stroke(width=1)

        parts = VGroup(graph, pol_graphs, fourier_graph)
        parts[1].set_width(parts[0].get_width() - 1)
        parts.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=RIGHT
        )
        parts.to_edge(RIGHT)
        self.add(parts)

        words = VGroup(OldTexText("Signal"), OldTexText("Winding"), OldTexText("Transform"))
        for word, part in zip(words, parts):
            word.scale(1.5)
            word.next_to(part, LEFT)
            word.to_edge(LEFT, MED_LARGE_BUFF)

        self.add(words)

        rect = SurroundingRectangle(pol_graphs[2])
        rect.set_stroke(RED, 2)
        dot = Dot(fourier_graph.pfp(2 / 6), color=RED)
        dot.set_stroke(BLACK, 3, background=True)
        dot.shift(0.01 * RIGHT)
        line = Line(dot.get_center(), rect.get_corner(DL), buff=0.1)
        line.match_style(rect)

        self.add(dot, line, rect)



# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


USE_ALMOST_FOURIER_BY_DEFAULT = False


class GaussianDistributionWrapper(Line):
    """
    This is meant to encode a 2d normal distribution as
    a mobject (so as to be able to have it be interpolated
    during animations).  It is a line whose center is the mean
    mu of a distribution, and whose radial vector (center to end)
    is the distribution's standard deviation
    """
    CONFIG = {
        "stroke_width" : 0,
        "mu" : ORIGIN,
        "sigma" : RIGHT,
    }
    def __init__(self, **kwargs):
        Line.__init__(self, ORIGIN, RIGHT, **kwargs)
        self.change_parameters(self.mu, self.sigma)

    def change_parameters(self, mu = None, sigma = None):
        curr_mu, curr_sigma = self.get_parameters()
        mu = mu if mu is not None else curr_mu
        sigma = sigma if sigma is not None else curr_sigma
        self.put_start_and_end_on(mu - sigma, mu + sigma)
        return self

    def get_parameters(self):
        """ Return mu_x, mu_y, sigma_x, sigma_y"""
        center, end = self.get_center(), self.get_end()
        return center, end-center

    def get_random_points(self, size = 1):
        mu, sigma = self.get_parameters()
        return np.array([
            np.array([
                np.random.normal(mu_coord, sigma_coord)
                for mu_coord, sigma_coord in zip(mu, sigma)
            ])
            for x in range(size)
        ])


class ProbabalisticMobjectCloud(ContinualAnimation):
    CONFIG = {
        "fill_opacity" : 0.25,
        "n_copies" : 100,
        "gaussian_distribution_wrapper_config" : {},
        "time_per_change" : 1./60,
        "start_up_time" : 0,
    }
    def __init__(self, prototype, **kwargs):
        digest_config(self, kwargs)
        fill_opacity = self.fill_opacity or prototype.get_fill_opacity()
        if "mu" not in self.gaussian_distribution_wrapper_config:
            self.gaussian_distribution_wrapper_config["mu"] = prototype.get_center()
        self.gaussian_distribution_wrapper = GaussianDistributionWrapper(
            **self.gaussian_distribution_wrapper_config
        )
        self.time_since_last_change = np.inf
        group = VGroup(*[
            prototype.copy().set_fill(opacity = fill_opacity)
            for x in range(self.n_copies)
        ])
        ContinualAnimation.__init__(self, group, **kwargs)
        self.update_mobject(0)

    def update_mobject(self, dt):
        self.time_since_last_change += dt
        if self.time_since_last_change < self.time_per_change:
            return
        self.time_since_last_change = 0

        group = self.mobject
        points = self.gaussian_distribution_wrapper.get_random_points(len(group))
        for mob, point in zip(group, points):
            self.update_mobject_by_point(mob, point)
        return self

    def update_mobject_by_point(self, mobject, point):
        mobject.move_to(point)
        return self


class ProbabalisticDotCloud(ProbabalisticMobjectCloud):
    CONFIG = {
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        dot = Dot(color = self.color)
        ProbabalisticMobjectCloud.__init__(self, dot)


class Thumbnail(Scene):
    def construct(self):
        uncertainty_principle = OldTexText("Uncertainty \\\\", "principle")
        uncertainty_principle[1].shift(SMALL_BUFF*UP)
        quantum = OldTexText("Quantum")
        VGroup(uncertainty_principle, quantum).scale(2.5)
        uncertainty_principle.to_edge(UP, MED_LARGE_BUFF)
        quantum.to_edge(DOWN, MED_LARGE_BUFF)

        arrow = OldTex("\\Downarrow")
        arrow.scale(4)
        arrow.move_to(Line(
            uncertainty_principle.get_bottom(),
            quantum.get_top(),
        ))

        cross = Cross(arrow)
        cross.set_stroke(RED, 20)

        is_word, not_word = is_not = OldTexText("is", "\\emph{NOT}")
        is_not.scale(3)
        is_word.move_to(arrow)
        # is_word.shift(0.6*UP)
        not_word.set_color(RED)
        not_word.set_stroke(RED, 3)
        not_word.rotate(10*DEGREES, about_edge = DOWN+LEFT)
        not_word.next_to(is_word, DOWN, 0.1*SMALL_BUFF)

        dot_cloud = ProbabalisticDotCloud(
            n_copies = 1000,
        )
        dot_gdw = dot_cloud.gaussian_distribution_wrapper
        # dot_gdw.rotate(3*DEGREES)
        dot_gdw.rotate(25*DEGREES)
        # dot_gdw.scale(2)
        dot_gdw.scale(2)
        # dot_gdw.move_to(quantum.get_bottom()+SMALL_BUFF*DOWN)
        dot_gdw.move_to(quantum)



        def get_func(a):
            return lambda t : 0.5*np.exp(-a*t**2)*np.cos(TAU*t)
        axes = Axes(
            x_min = -6, x_max = 6,
            x_axis_config = {"unit_size" : 0.25}
        )
        graphs = VGroup(*[
            axes.get_graph(get_func(a))
            for a in (10, 3, 1, 0.3, 0.1,)
        ])
        graphs.arrange(DOWN, buff = 0.6)
        graphs.to_corner(UP+LEFT)
        graphs.set_color_by_gradient(BLUE_B, BLUE_D)

        frequency_axes = Axes(
            x_min = 0, x_max = 2,
            x_axis_config = {"unit_size" : 1}
        )
        fourier_graphs = VGroup(*[
            get_fourier_graph(
                frequency_axes, graph.underlying_function,
                t_min = -10, t_max = 10,
            )
            for graph in graphs
        ])
        for graph, fourier_graph in zip(graphs, fourier_graphs):
            fourier_graph.pointwise_become_partial(fourier_graph, 0.02, 0.06)
            fourier_graph.scale(3)
            fourier_graph.stretch(3, 1)
            fourier_graph.move_to(graph)
            fourier_graph.to_edge(RIGHT)

        self.add(graphs, fourier_graphs)


        self.add(dot_cloud)
        self.add(
            uncertainty_principle, quantum,
        )
        self.add(arrow, cross)



# ----- From _2018/borsuk_addition.py -----

class Thumbnail(SpecialThreeDScene):
    def construct(self):
        sphere = ParametricSurface(
            func=lambda u, v: 2 * np.array([
                np.cos(v) * np.sin(u) + 0.2 * np.cos(3 * u),
                np.sin(v) * np.sin(u),
                np.cos(u) + 0.2 * np.sin(4 * v) - 0.3 * np.cos(3 * u)
            ]),
            resolution=(24, 48),
            u_min=0.001,
            u_max=PI - 0.001,
            v_min=0,
            v_max=TAU,
        )
        sphere.rotate(70 * DEGREES, DOWN)
        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-90 * DEGREES,
        )
        # randy = Randolph(mode="telepath")
        # eyes = VGroup(randy.eyes, randy.pupils)
        # eyes.scale(3.5)
        # eyes.rotate(90 * DEGREES, RIGHT)
        # eyes.next_to(sphere, OUT, buff=0)

        self.add(sphere)
