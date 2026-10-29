# ==============================================================================
# Scene:      Test
# Source:     videos/_2018/turbulence.py (lines 351-354)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Test.py Test -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DoublePendulum(VMobject):
    CONFIG = {
        "start_angles": [3 * PI / 7, 3 * PI / 4],
        "color1": BLUE,
        "color2": RED,
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        line1 = Line(ORIGIN, UP)
        dot1 = Dot(color=self.color1)
        dot1.add_updater(lambda d: d.move_to(line1.get_end()))
        line2 = Line(UP, 2 * UP)
        dot2 = Dot(color=self.color2)
        dot2.add_updater(lambda d: d.move_to(line2.get_end()))
        self.add(line1, line2, dot1, dot2)

        # Largely copied from https://scipython.com/blog/the-double-pendulum/
        # Pendulum rod lengths (m), bob masses (kg).
        L1, L2 = 1, 1
        m1, m2 = 1, 1
        # The gravitational acceleration (m.s-2).
        g = 9.81

        self.state_vect = np.array([
            self.start_angles[0], 0,
            self.start_angles[1], 0,
        ])
        self.state_vect += np.random.random(4) * 1e-7

        def update(group, dt):
            for x in range(2):
                line1, line2 = group.submobjects[:2]
                theta1, z1, theta2, z2 = group.state_vect

                c, s = np.cos(theta1 - theta2), np.sin(theta1 - theta2)

                theta1dot = z1
                z1dot = (m2 * g * np.sin(theta2) * c - m2 * s * (L1 * (z1**2) * c + L2 * z2**2) -
                         (m1 + m2) * g * np.sin(theta1)) / L1 / (m1 + m2 * s**2)
                theta2dot = z2
                z2dot = ((m1 + m2) * (L1 * (z1**2) * s - g * np.sin(theta2) + g * np.sin(theta1) * c) +
                         m2 * L2 * (z2**2) * s * c) / L2 / (m1 + m2 * s**2)

                group.state_vect += 0.5 * dt * np.array([
                    theta1dot, z1dot, theta2dot, z2dot,
                ])
                group.state_vect[1::2] *= 0.9999

            p1 = L1 * np.sin(theta1) * RIGHT - L1 * np.cos(theta1) * UP
            p2 = p1 + L2 * np.sin(theta2) * RIGHT - L2 * np.cos(theta2) * UP

            line1.put_start_and_end_on(ORIGIN, p1)
            line2.put_start_and_end_on(p1, p2)

        self.add_updater(update)


class DoublePendulums(VGroup):
    def __init__(self, **kwargs):
        colors = [BLUE, RED, YELLOW, PINK, MAROON_B, PURPLE, GREEN]
        VGroup.__init__(
            self,
            *[
                DoublePendulum(
                    color1=random.choice(colors),
                    color2=random.choice(colors),
                )
                for x in range(5)
            ],
            **kwargs,
        )


class Test(Scene):
    def construct(self):
        self.add(DoublePendulums())
        self.wait(30)
