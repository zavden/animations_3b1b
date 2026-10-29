# ==============================================================================
# Scene:      SunInTheSky
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 34-166)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SunInTheSky.py SunInTheSky -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The images are looked up next to this file (Path(__file__).parent) instead of next to Grant's video output; they are placeholder images.
#
# Placeholder assets (not Grant's originals):
#   - Paul Animations/.../JustSunBackgroundRemoved.png and JustSun.tif (derived from raster_images/sun.png, which the lib already ships) and supplements/SunAndThumb.jpg (sky with sun and thumb, placeholder)
# ==============================================================================

from manim_imports_ext import *

class SunInTheSky(InteractiveScene):
    def construct(self):
        # Add pictures
        frame = self.frame
        # CHANGE: the images lived in folders next to Grant's video output; now they are next to this file (placeholder images).
        base_path = Path(__file__).parent
        pure_sun = ImageMobject(str(Path(base_path, 'Paul Animations/6. Transit Of Venus/New Transit of Venus scenes/JustSunBackgroundRemoved.png')))
        clean_sun = ImageMobject(str(Path(base_path, 'Paul Animations/6. Transit Of Venus/New Transit of Venus scenes/JustSun.tif')))
        sky_image = ImageMobject(str(Path(base_path, 'supplements/SunAndThumb.jpg')))
        sky_image.set_height(FRAME_HEIGHT)
        for sun in pure_sun, clean_sun:
            sun.set_height(0.23)
            sun.move_to([-0.63, 1.36, 0.])

        # Add angle measure
        sun_arc_minutes = 32
        sun_disk = Circle(radius=0.086)
        sun_disk.move_to(pure_sun.get_center() + 0.0055 * RIGHT + 0.002 * UP)

        protractor = NumberLine([0, 60 * 10])
        protractor.rotate(90 * DEG)
        protractor.scale(sun_disk.get_height() / protractor.get_unit_size() / sun_arc_minutes)
        protractor.next_to(sun_disk, RIGHT, buff=0.15, aligned_edge=DOWN)

        protractor.ticks.align_to(protractor.get_center(), RIGHT)
        protractor.ticks.set_width(0.005, about_edge=RIGHT, stretch=True)
        protractor.ticks[::60].set_width(0.02, about_edge=RIGHT, stretch=True)

        deg_labels = VGroup(
            Tex(Rf"{n}^\circ", font_size=2).next_to(protractor.n2p(60 * n), RIGHT, buff=0.01)
            for n in range(5)
        )
        protractor.add(deg_labels)

        # Zoom in
        self.add(sky_image)
        self.add(clean_sun)
        self.add(protractor)

        self.play(
            frame.animate.set_height(1.75 * pure_sun.get_height()).move_to(pure_sun).shift([0.1, 0.08, 0]),
            FadeIn(protractor, time_span=(2.5, 3.5)),
            FadeIn(pure_sun, time_span=(3, 4)),
            FadeIn(clean_sun, time_span=(4, 5)),
            FadeOut(sky_image, time_span=(3, 4)),
            run_time=5,
        )
        self.wait()

        # Show height of sun
        sun_label = Text(f"{sun_arc_minutes} arc-minutes").scale(1 / 24)
        sun_label.set_color(YELLOW)
        point = protractor.n2p(sun_arc_minutes)
        sun_label.next_to(point, RIGHT, buff=0.01)

        dash_length = 0.0025
        dashed_line = DashedLine(point, point + 2 * sun_disk.get_width() * LEFT, dash_length=dash_length)
        dashed_line.set_stroke(YELLOW, 2)
        dashed_lines = VGroup(
            dashed_line.copy().align_to(protractor.n2p(0), DOWN),
            dashed_line,
        )

        self.play(
            FadeIn(sun_label),
            ShowCreation(dashed_lines),
        )
        self.wait()

        # Zoom into Venus
        venus = Dot(radius=0.25 * protractor.get_unit_size()).set_fill(BLACK)
        venus.set_stroke(BLACK, 2)
        venus.set_anti_alias_width(6)
        venus.move_to(sun_disk)
        venus.align_to(protractor.n2p(8), DOWN)

        venus_line = dashed_lines[0].copy()
        venus_line.set_stroke(TEAL)
        venus_line.match_y(venus)

        venus.save_state()
        venus.shift(0.5 * sun_disk.get_width() * LEFT)
        self.play(
            Restore(venus),
            frame.animate.reorient(0, 0, 0, (-0.5, 1.37, 0.0), 0.29),
            FadeIn(venus_line, time_span=(3, 4)),
            run_time=4
        )
        self.wait()

        # Shift up and down
        labels = VGroup(
            Text("Northern Hemisphere\nObservation"),
            Text("Sourthern Hemisphere\nObservation"),
        )
        labels.scale(1 / 36)
        labels.next_to(venus, UP, buff=protractor.get_unit_size())
        labels.set_fill(BLACK)
        shift_value = 0.5 * protractor.get_unit_size() * DOWN
        labels[1].shift(shift_value)

        self.play(FadeIn(labels[0]))
        for n in range(4):
            index = n % 2
            sign = -(2 * index - 1)

            self.play(
                FadeOut(labels[index]),
                FadeIn(labels[1 - index]),
                VGroup(venus, venus_line).animate.shift(sign * shift_value)
            )
            self.wait()

        # Have lines go over appropriate parts of the disk (7 plays)
        prop1 = 312.9 / 360
        prop2 = prop1 + 3 / 360
        p1 = sun_disk.pfp(prop1)
        p2 = sun_disk.pfp(prop2)
        lines = VGroup(
            DashedLine(point + 0.675 * sun_disk.get_width() * RIGHT, [protractor.n2p(0)[0], point[1], 0], dash_length=0.5 * dash_length).set_stroke(TEAL, 1)
            for point in [p1, p2]
        )

        self.play(
            FadeOut(pure_sun),
            FadeOut(clean_sun),
            FadeOut(venus_line),
            FadeOut(venus),
            FadeOut(labels),
            FadeIn(lines),
            sun_label.animate.scale(0.5, about_edge=LEFT),
            deg_labels[0].animate.scale(0.5, about_edge=LEFT),
        )
        self.wait()
