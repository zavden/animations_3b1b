# ==============================================================================
# Scene:      LabelIo
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 297-328)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LabelIo.py LabelIo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - JovianSystem.png is looked up next to this file (before: Grant's Dropbox) and is a placeholder image.
#
# Placeholder assets (not Grant's originals):
#   - JovianSystem.png (labeled placeholder image; the scene loads it but does not show it)
# ==============================================================================

from manim_imports_ext import *

class LabelIo(InteractiveScene):
    def construct(self):
        # Background
        # CHANGE: JovianSystem.png lived in Grant's Dropbox; now there is a placeholder image next to this file.
        im = ImageMobject(str(Path(__file__).parent / 'JovianSystem.png'))
        im.set_height(FRAME_HEIGHT)
        # self.add(im)
        # self.add(NumberPlane().fade(0.25))

        # Ellipse
        orbit = Circle()
        orbit.set_shape(2.75, 0.7)
        orbit.scale(2)  # For new edit
        orbit.rotate(10 * DEG)
        point = Point()
        point.move_to(orbit.get_start())

        label = Text("Io", font_size=36)
        buff = 0.05

        def update_label(label):
            coords = point.get_center()
            dist = get_norm(coords)
            label.move_to((dist + buff) * coords / dist)
            return label

        label.add_updater(update_label)

        self.add(label)
        for _ in range(3):
            self.play(
                MoveAlongPath(point, orbit, run_time=7, rate_func=linear),
            )
