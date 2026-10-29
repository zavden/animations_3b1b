# ==============================================================================
# Scene:      LongEddy
# Source:     videos/_2018/turbulence.py (lines 657-660)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LongEddy.py LongEddy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CreationDestructionMobject(VMobject):
    CONFIG = {
        "start_time": 0,
        "frequency": 0.25,
        "max_ratio_shown": 0.3,
        "use_copy": True,
    }

    def __init__(self, template, **kwargs):
        VMobject.__init__(self, **kwargs)
        if self.use_copy:
            self.ghost_mob = template.copy().fade(1)
            self.add(self.ghost_mob)
        else:
            self.ghost_mob = template
            # Don't add
        self.shown_mob = template.deepcopy()
        self.shown_mob.clear_updaters()
        self.add(self.shown_mob)
        self.total_time = self.start_time

        def update(mob, dt):
            mob.total_time += dt
            period = 1.0 / mob.frequency
            unsmooth_alpha = (mob.total_time % period) / period
            alpha = bezier([0, 0, 1, 1])(unsmooth_alpha)
            mrs = mob.max_ratio_shown
            mob.shown_mob.pointwise_become_partial(
                mob.ghost_mob,
                max(interpolate(-mrs, 1, alpha), 0),
                min(interpolate(0, 1 + mrs, alpha), 1),
            )

        self.add_updater(update)


class Eddy(VMobject):
    CONFIG = {
        "cd_mob_config": {
            "frequency": 0.2,
            "max_ratio_shown": 0.3
        },
        "n_spirils": 5,
        "n_layers": 20,
        "radius": 1,
        "colors": [BLUE_A, BLUE_E],
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        lines = self.get_lines()
        # self.add(lines)
        self.add(*[
            CreationDestructionMobject(line, **self.cd_mob_config)
            for line in lines
        ])
        self.randomize_times()

    def randomize_times(self):
        for submob in self.submobjects:
            if hasattr(submob, "total_time"):
                T = 1.0 / submob.frequency
                submob.total_time = T * random.random()

    def get_lines(self):
        a = 0.2
        return VGroup(*[
            self.get_line(r=self.radius * (1 - a + 2 * a * random.random()))
            for x in range(self.n_layers)
        ])

    def get_line(self, r):
        return ParametricCurve(
            lambda t: r * (t + 1)**(-1) * np.array([
                np.cos(TAU * t),
                np.sin(TAU * t),
                0,
            ]),
            t_min=0.1 * random.random(),
            t_max=self.n_spirils,
            stroke_width=1,
            color=interpolate_color(*self.colors, random.random())
        )


class LongEddy(Scene):
    def construct(self):
        self.add(Eddy())
        self.wait(30)
