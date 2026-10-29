# ==============================================================================
# Scene:      FiguresOfFluidDynamics
# Source:     videos/_2018/turbulence.py (lines 1222-1262)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FiguresOfFluidDynamics.py FiguresOfFluidDynamics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FiguresOfFluidDynamics(Scene):
    def construct(self):
        names = [
            "Leonhard Euler",
            "George Stokes",
            "Hermann von Helmholtz",
            "Lewis Richardson",
            "Geoffrey Taylor",
            "Andrey Kolmogorov",
        ]
        images = Group(*[
            ImageMobject(name.replace(" ", "_"), height=3)
            for name in names
        ])
        images.arrange(RIGHT, buff=MED_SMALL_BUFF)
        image_groups = Group()
        for image, name in zip(images, names):
            name_mob = OldTexText(name)
            name_mob.scale(0.6)
            name_mob.next_to(image, DOWN)
            image_groups.add(Group(image, name_mob))
        image_groups.arrange_in_grid(2, 3)
        image_groups.set_height(FRAME_HEIGHT - 1)

        self.play(LaggedStartMap(
            FadeInFromDown, image_groups,
            lag_ratio=0.5,
            run_time=3
        ))
        self.wait()
        to_fade = image_groups[:-1]
        to_fade.generate_target()
        to_fade.target.space_out_submobjects(3)
        to_fade.target.shift(3 * UL)
        to_fade.target.fade(1)
        self.play(
            MoveToTarget(to_fade, remover=True),
            image_groups[-1].set_height, 5,
            image_groups[-1].center,
        )
        self.wait()
