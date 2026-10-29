# ==============================================================================
# Scene:      LogoGeneration
# Source:     videos/_2018/dandelin.py (lines 7-40)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl LogoGeneration.py LogoGeneration -w -m --fps 15
#
# Why it does not render:
#   Animation of the 3b1b channel logo (logo.spike_layers / logo.iris_background): the logo is a brand asset that is deliberately not reproduced (LogoGenerationTemplate only draws a placeholder circle), so the scene has nothing to animate.
# ==============================================================================

from manim_imports_ext import *

class LogoGeneration(LogoGenerationTemplate):
    CONFIG = {
        "random_seed": 2,
    }

    def get_logo_animations(self, logo):
        layers = logo.spike_layers
        for layer in layers:
            random.shuffle(layer.submobjects)
            for spike in layer:
                spike.save_state()
                spike.scale(0.5)
                spike.apply_complex_function(np.log)
                spike.rotate(-90 * DEGREES, about_point=ORIGIN)
                spike.set_fill(opacity=0)

        return [
            FadeIn(
                logo.iris_background,
                rate_func=squish_rate_func(smooth, 0.25, 1),
                run_time=3,
            ),
            AnimationGroup(*[
                LaggedStartMap(
                    Restore, layer,
                    run_time=3,
                    path_arc=180 * DEGREES,
                    rate_func=squish_rate_func(smooth, a / 3.0, (a + 0.9) / 3.0),
                    lag_ratio=0.8,
                )
                for layer, a in zip(layers, [0, 2, 1, 0])
            ]),
            Animation(logo.pupil),
        ]
