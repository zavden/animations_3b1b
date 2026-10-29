# ==============================================================================
# Scene:      Headlines
# Source:     videos/_2026/2025_P6/p6.py (lines 4651-4785)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Headlines.py Headlines -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/AI Evolution Timeline images/fel.png  (placeholder: headline fel)
#   - _lib/assets/raster_images/AI Evolution Timeline images/unit_distance.png  (placeholder: headline unit_distance)
#   - _lib/assets/raster_images/AI Evolution Timeline images/erdos_problems.png  (placeholder: headline erdos_problems)
#   - _lib/assets/raster_images/AI Evolution Timeline images/jacobian.png  (placeholder: headline jacobian)
#   - _lib/assets/raster_images/AI Evolution Timeline images/non-sofic_group.png  (placeholder: headline non-sofic_group)
#   - _lib/assets/raster_images/AI Evolution Timeline images/navier-stokes.png  (placeholder: headline navier-stokes)
#
# Notes:
#   The 6 press headlines are 1200x600 placeholder images (Grant's Dropbox) in _lib/assets/raster_images/AI Evolution Timeline images/. `images_dir = "AI Evolution Timeline images"` is just a relative prefix that ImageMobject resolves against the raster images directory, so no code change was needed.
# ==============================================================================

import tempfile
import os
import random
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


class Headlines(InteractiveScene):
    MARGIN = 0.4
    H_GAP = 0.35
    V_GAP = 0.35
    N_COLS = 2
    N_ROWS = 3

    REVEAL_WIDTH_FRAC = 0.55
    REVEAL_HEIGHT_FRAC = 0.55

    GROW_TIME = 0.8
    BACKSWING_FRACTION = 0.4
    OVERSHOOT_SCALE = 1.12
    SHIFT_TIME = 1.1

    LAG_RATIO = 0.5

    PULSE_AMPLITUDE = 0.01
    PULSE_FREQ_RANGE = (0.25, 0.35)
    BREATHE_TIME = 12

    def scale_to_fit_box(self, mobject, max_width, max_height):
        width_scale = max_width / mobject.get_width()
        height_scale = max_height / mobject.get_height()
        mobject.scale(min(width_scale, height_scale))
        return mobject

    def get_headline_update_func(self, tiny_start, overshoot_target, grid_target,
                                 start_delay, rise_time, settle_time,
                                 breathe_amplitude, breathe_freq):
        rise_end = start_delay + rise_time
        settle_end = rise_end + settle_time

        def update_func(mob, alpha, total_run_time):
            t = alpha * total_run_time

            if t <= start_delay:
                mob.become(tiny_start)
            elif t < rise_end:
                p = (t - start_delay) / rise_time
                mob.interpolate(tiny_start, overshoot_target, rush_from(p))
            elif t < settle_end:
                p = (t - rise_end) / settle_time
                mob.interpolate(overshoot_target, grid_target, smooth(p))
            else:
                breathe_t = t - settle_end
                factor = 1 / (1 + breathe_amplitude * np.sin(TAU * breathe_freq * breathe_t))
                mob.become(grid_target)
                mob.scale(factor, about_point=grid_target.get_center())

        return update_func

    def construct(self):
        # Add a grid of images
        images_dir = "AI Evolution Timeline images"
        image_names = [
            "fel.png",
            "unit_distance.png",
            "erdos_problems.png",
            "jacobian.png",
            "non-sofic_group.png",
            "navier-stokes.png",
        ]

        raw_images = [
            ImageMobject(os.path.join(images_dir, name))
            for name in image_names
        ]

        grid_width = FRAME_WIDTH - 2 * self.MARGIN
        grid_height = FRAME_HEIGHT - 2 * self.MARGIN
        cell_width = (grid_width - (self.N_COLS - 1) * self.H_GAP) / self.N_COLS
        cell_height = (grid_height - (self.N_ROWS - 1) * self.V_GAP) / self.N_ROWS

        cell_centers = []
        for row in range(self.N_ROWS):
            for col in range(self.N_COLS):
                x = -grid_width / 2 + cell_width / 2 + col * (cell_width + self.H_GAP)
                y = grid_height / 2 - cell_height / 2 - row * (cell_height + self.V_GAP)
                cell_centers.append(np.array([x, y, 0.0]))

        reveal_w = FRAME_WIDTH * self.REVEAL_WIDTH_FRAC
        reveal_h = FRAME_HEIGHT * self.REVEAL_HEIGHT_FRAC

        overshoot_targets = []
        grid_targets = []
        for img, center in zip(raw_images, cell_centers):
            reveal = img.copy()
            self.scale_to_fit_box(reveal, reveal_w, reveal_h)
            reveal.move_to(ORIGIN)

            overshoot_targets.append(reveal.copy().scale(self.OVERSHOOT_SCALE))

            grid = img.copy()
            self.scale_to_fit_box(grid, cell_width, cell_height)
            grid.move_to(center)
            grid_targets.append(grid)

        rise_time = self.GROW_TIME * (1 - self.BACKSWING_FRACTION)
        settle_time = self.GROW_TIME * self.BACKSWING_FRACTION + self.SHIFT_TIME
        seq_time = self.GROW_TIME + self.SHIFT_TIME

        n = len(raw_images)
        max_delay = (n - 1) * self.LAG_RATIO * seq_time
        total_run_time = max_delay + seq_time + self.BREATHE_TIME

        # Pop up the headlines
        animations = []
        for i in range(n):
            tiny_start = overshoot_targets[i].copy().scale(0.001 / self.OVERSHOOT_SCALE).set_opacity(0)
            start_delay = i * self.LAG_RATIO * seq_time

            mob = tiny_start.copy()
            self.add(mob)

            update_func = self.get_headline_update_func(
                tiny_start,
                overshoot_targets[i],
                grid_targets[i],
                start_delay,
                rise_time,
                settle_time,
                self.PULSE_AMPLITUDE,
                random.uniform(*self.PULSE_FREQ_RANGE),
            )
            animations.append(
                UpdateFromAlphaFunc(
                    mob,
                    lambda m, a, f=update_func: f(m, a, total_run_time),
                    run_time=total_run_time,
                    rate_func=linear,
                )
            )

        self.play(*animations)
