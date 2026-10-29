# ==============================================================================
# Scene:      BlackScholes
# Source:     videos/_2019/diffyq/part2/staging.py (lines 200-259)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BlackScholes.py BlackScholes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BrownianMotion(Scene):
    CONFIG = {
        "wait_time": 60,
        "L": 3,  # Box in [-L, L] x [-L, L]
        "n_particles": 100,
        "m1": 1,
        "m2": 100,
        "r1": 0.05,
        "r2": 0.5,
        "max_v": 5,
        "random_seed": 2,
    }

    def construct(self):
        self.add_title()
        self.add_particles()
        self.wait(self.wait_time)

    def add_title(self):
        square = Square(side_length=2 * self.L)
        title = OldTexText("Brownian motion")
        title.scale(1.5)
        title.next_to(square, UP)

        self.add(square)
        self.add(title)

    def add_particles(self):
        m1 = self.m1
        m2 = self.m2
        r1 = self.r1
        r2 = self.r2
        L = self.L
        max_v = self.max_v
        n_particles = self.n_particles

        lil_particles = VGroup(*[
            self.get_particle(m1, r1, L, max_v)
            for k in range(n_particles)
        ])
        big_particle = self.get_particle(m2, r2, L=r2, max_v=0)
        big_particle.set_fill(YELLOW, 1)

        for p in lil_particles:
            if self.are_colliding(p, big_particle):
                lil_particles.remove(p)
        all_particles = VGroup(big_particle, *lil_particles)
        all_particles.add_updater(self.update_particles)

        path = self.get_traced_path(big_particle)

        self.add(all_particles)
        self.add(path)

        self.particles = all_particles
        self.big_particle = big_particle
        self.path = path

    def get_particle(self, m, r, L, max_v):
        dot = Dot(radius=r)
        dot.set_fill(WHITE, 0.7)
        dot.mass = m
        dot.radius = r
        dot.center = op.add(
            np.random.uniform(-L + r, L - r) * RIGHT,
            np.random.uniform(-L + r, L - r) * UP
        )
        dot.move_to(dot.center)
        dot.velocity = rotate_vector(
            np.random.uniform(0, max_v) * RIGHT,
            np.random.uniform(0, TAU),
        )
        return dot

    def are_colliding(self, p1, p2):
        d = get_norm(p1.get_center() - p2.get_center())
        return (d < p1.radius + p2.radius)

    def get_traced_path(self, particle):
        path = VMobject()
        path.set_stroke(BLUE, 3)
        path.start_new_path(particle.get_center())

        buff = 0.02

        def update_path(path):
            new_point = particle.get_center()
            if get_norm(new_point - path.get_last_point()) > buff:
                path.add_line_to(new_point)

        path.add_updater(update_path)
        return path

    def update_particles(self, particles, dt):
        for p1 in particles:
            p1.center += p1.velocity * dt

            # Check particle collisions
            buff = 0.01
            for p2 in particles:
                if p1 is p2:
                    continue
                v = p2.center - p1.center
                dist = get_norm(v)
                r_sum = p1.radius + p2.radius
                diff = dist - r_sum
                if diff < 0:
                    unit_v = v / dist
                    p1.center += (diff - buff) * unit_v / 2
                    p2.center += -(diff - buff) * unit_v / 2
                    u1 = p1.velocity
                    u2 = p2.velocity
                    m1 = p1.mass
                    m2 = p2.mass
                    v1 = (
                        (m2 * (u2 - u1) + m1 * u1 + m2 * u2) /
                        (m1 + m2)
                    )
                    v2 = (
                        (m1 * (u1 - u2) + m1 * u1 + m2 * u2) /
                        (m1 + m2)
                    )
                    p1.velocity = v1
                    p2.velocity = v2

            # Check edge collisions
            r1 = p1.radius
            c1 = p1.center
            for i in [0, 1]:
                if abs(c1[i]) + r1 > self.L:
                    c1[i] = np.sign(c1[i]) * (self.L - r1)
                    p1.velocity[i] *= -1 * op.mul(
                        np.sign(p1.velocity[i]),
                        np.sign(c1[i])
                    )

        for p in particles:
            p.move_to(p.center)
        return particles


class AltBrownianMotion(BrownianMotion):
    CONFIG = {
        "wait_time": 20,
        "n_particles": 100,
        "m2": 10,
    }


class BlackScholes(AltBrownianMotion):
    def construct(self):
        # For some reason I'm amused by the thought
        # Of this graph perfectly matching the Brownian
        # Motion y-coordiante
        self.add_title()
        self.add_particles()
        self.particles.set_opacity(0)
        self.remove(self.path)
        self.add_graph()
        self.wait(self.wait_time)

    def add_title(self):
        title = OldTexText("Black-Scholes equations")
        title.scale(1.5)
        title.next_to(2 * UP, UP)

        equation = OldTex(
            "{\\partial V \\over \\partial t}", "+",
            "\\frac{1}{2} \\sigma^2 S^2",
            "{\\partial^2 V \\over \\partial S^2}", "+",
            "rS", "{\\partial V \\over \\partial S}",
            "-rV", "=", "0",
        )
        equation.scale(0.8)
        equation.next_to(title, DOWN)

        self.add(title)
        self.add(equation)
        self.title = title
        self.equation = equation

    def add_graph(self):
        axes = Axes(
            x_min=-1,
            x_max=20,
            y_min=0,
            y_max=10,
            axis_config={
                "unit_size": 0.5,
            },
        )
        axes.set_height(4)
        axes.move_to(DOWN)

        def get_graph_point():
            return axes.c2p(
                self.get_time(),
                5 + 2 * self.big_particle.get_center()[1]
            )

        graph = VMobject()
        graph.match_style(self.path)
        graph.start_new_path(get_graph_point())
        graph.add_updater(
            lambda g: g.add_line_to(get_graph_point())
        )

        self.add(axes)
        self.add(graph)
