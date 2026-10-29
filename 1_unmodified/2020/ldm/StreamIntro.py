# ==============================================================================
# Scene:      StreamIntro
# Source:     videos/_2020/ldm.py (lines 5-36)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StreamIntro.py StreamIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StreamIntro(Scene):
    def construct(self):
        # Add logo
        logo = Logo()
        spikes = VGroup(*[
            spike
            for layer in logo.spike_layers
            for spike in layer
        ])
        self.add(*logo.family_members_with_points())

        # Add label
        label = OldTexText("The lesson will\\\\begin shortly")
        label.scale(2)
        label.next_to(logo, DOWN)
        self.add(label)

        self.camera.frame.move_to(DOWN)

        for spike in spikes:
            point = spike.get_start()
            spike.angle = angle_of_vector(point)

        anims = []
        for spike in spikes:
            anims.append(Rotate(
                spike, spike.angle * 28 * 2,
                about_point=ORIGIN,
                rate_func=linear,
            ))
        self.play(*anims, run_time=60 * 5)
        self.wait(20)
