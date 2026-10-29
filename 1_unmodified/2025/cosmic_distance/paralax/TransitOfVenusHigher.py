# ==============================================================================
# Scene:      TransitOfVenusHigher
# Source:     videos/_2025/cosmic_distance/paralax.py (lines 613-614)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitOfVenusHigher.py TransitOfVenusHigher -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransitOfVenus(InteractiveScene):
    path_y = -1
    include_image = False

    def construct(self):
        # Add image (just for development)
        if self.include_image:
            path = self.file_writer.get_output_file_rootname()
            im_path = Path(path.parent.parent, "Paul Animations/6. Transit Of Venus/New Transit of Venus scenes/JustSun.tif")
            image.set_height(FRAME_HEIGHT)
            self.add(image)

        # Add venus
        path = Line(3 * LEFT, 3 * RIGHT)
        path.set_y(self.path_y)
        path.set_stroke(BLACK, 2)

        venus = Dot(radius=0.05).set_fill(BLACK)
        venus.move_to(path.get_start())
        venus.set_fill(border_width=1)
        venus.set_anti_alias_width(5)
        self.add(venus)

        # Show transit
        venus.move_to(path.get_start())
        velocity = 0.25
        venus.clear_updaters()
        venus.add_updater(lambda m, dt: m.shift(dt * velocity * RIGHT))
        wait_time = 1.0
        copies = VGroup()
        self.add(copies)
        for _ in range(int(path.get_length() / velocity / wait_time)):
            self.wait(wait_time)
            copies.add(venus.copy().clear_updaters())

        self.remove(venus)
        self.play(Transform(copies, VGroup(path)))
        self.wait()


class TransitOfVenusHigher(TransitOfVenus):
    path_y = +0.5
