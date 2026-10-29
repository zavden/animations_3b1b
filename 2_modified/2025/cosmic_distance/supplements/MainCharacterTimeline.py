# ==============================================================================
# Scene:      MainCharacterTimeline
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 206-447)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MainCharacterTimeline.py MainCharacterTimeline -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses labeled placeholder portraits (in _lib/assets/raster_images/); the originals are photos/paintings that are not in the repo.
#
# Placeholder assets (not Grant's originals):
#   - Placeholder portraits in raster_images: Head_of_Aristotle, Eratosthenes, Kepler, Copernicus, TychoBrahe, JamesCook, EdmondHalley, OleRomer, ChristiaanHuygens, FriedrichBessel, HenriettaLeavitt, EdwinHubble (.png)
# ==============================================================================

from manim_imports_ext import *

class MainCharacterTimeline(InteractiveScene):
    def construct(self):
        # Add the timeline
        frame = self.frame

        timeline = NumberLine(
            (-500, 2000, 10),
            tick_size=0.05,
            longer_tick_multiple=2,
            big_tick_spacing=100,
            unit_size=1 / 50
        )
        numbers =timeline.add_numbers(
            range(-500, 2100, 100),
            group_with_commas=False,
            font_size=20,
            buff=0.15
        )
        for number in numbers[:5]:
            number.remove(number[0])
            bce = Text("BCE")
            bce.set_height(0.75 * number.get_height())
            bce.next_to(number, RIGHT, buff=0.05, aligned_edge=DOWN)
            number.add(bce)
            number.shift(0.15 * LEFT)

        self.add(timeline)
        frame.move_to(timeline.n2p(-175))

        # Characters
        characters = [
            ("Aristotle", -384, -322, 0.2, BLUE_D),
            ("Eratosthenes", -276, -194, 0.2, BLUE_B),
            ("Aristarchus", -310, -230, 0.5, BLUE_C),
            ("Kepler", 1571, 1630, 0.2, RED_C),
            ("Copernicus", 1473, 1543, 0.2, RED_A),
            ("Brahe", 1546, 1601, 0.5, RED_E),
            ("James Cook", 1728, 1779, 0.2, GREEN_E),
            ("Edmond Halley", 1656, 1742, 0.5, GREEN_C),
            ("Ole Rømer", 1644, 1710, 0.2, BLUE_D),
            ("Huygens", 1629, 1695, 0.5, BLUE_C),
            ("Friedrich Bessel", 1784, 1846, 0.2, GREEN_B),
            ("Henrietta Leavitt", 1868, 1921, 0.5, RED_D),
            ("Edwin Hubble", 1889, 1953, 0.2, RED_C),
        ]
        character_labels = VGroup()
        for name, start, end, offset, color in characters:
            line = Line(timeline.n2p(start), timeline.n2p(end))
            line.set_stroke(color, 2)
            line.shift(offset * UP)
            # name_mob = Text(name, font_size=24)
            name_mob = Text(name, font_size=18)
            name_mob.set_color(color)
            name_mob.next_to(line, UP, buff=0.05)
            dashes = VGroup(
                DashedLine(line.get_start(), timeline.n2p(start), dash_length=0.01),
                DashedLine(line.get_end(), timeline.n2p(end), dash_length=0.01),
            )
            dashes.set_stroke(color, 1.5)
            line_group = VGroup(line, name_mob, dashes)
            character_labels.add(line_group)

        images = Group(
            ImageMobject("Head_of_Aristotle"),
            ImageMobject("Eratosthenes"),
            Square().set_opacity(0),
            ImageMobject("Kepler"),
            ImageMobject("Copernicus"),
            ImageMobject("TychoBrahe"),
            ImageMobject("JamesCook"),
            ImageMobject("EdmondHalley"),
            ImageMobject("OleRomer"),
            ImageMobject("ChristiaanHuygens"),
            ImageMobject("FriedrichBessel"),
            ImageMobject("HenriettaLeavitt"),
            ImageMobject("EdwinHubble"),
        )
        for image, character_label in zip(images, character_labels):
            image.set_height(2.0)
            image.next_to(character_label, UP)

        # Add greeks
        frame.set_height(5).move_to(timeline.n2p(-250))
        frame.set_y(0.5)
        self.play(
            FadeIn(character_labels[0], lag_ratio=0.1),
        )
        self.wait()
        self.play(
            FadeIn(character_labels[1], lag_ratio=0.1),
            FadeIn(images[1], 0.5 * UP),
            frame.animate.set_height(6).match_x(timeline.n2p(-175)).set_anim_args(run_time=3),
        )
        self.wait()
        self.play(
            FadeIn(character_labels[2], lag_ratio=0.1),
            FadeOut(images[1], 0.5 * RIGHT),
        )
        self.wait()

        # Up to Kepler
        kepler_label, copernicus_label, brahe_label = character_labels[3:6]
        kepler_image, copernicus_image, brahe_image = images[3:6]
        self.play(
            frame.animate.match_x(timeline.n2p(1600)),
            UpdateFromAlphaFunc(frame, lambda m, a: m.set_height(interpolate(6, 12, there_and_back(a)))),
            run_time=3,
        )
        self.play(
            FadeIn(kepler_label, lag_ratio=0.1),
            FadeIn(kepler_image, 0.5 * UP),
        )
        self.wait()
        self.play(
            FadeIn(copernicus_label, lag_ratio=0.1),
            FadeIn(copernicus_image, 0.5 * UP),
        )
        self.wait()
        self.play(
            FadeIn(brahe_label, lag_ratio=0.1),
            FadeIn(brahe_image, 0.5 * UP),
            copernicus_image.animate.scale(0.5, about_edge=DL).shift(0.25 * RIGHT),
            kepler_image.animate.scale(0.5, about_edge=DR).shift(0.25 * DR),
        )
        self.wait()
        self.play(
            brahe_image.animate.scale(0.5, about_edge=DOWN),
            kepler_image.animate.shift(0.2 * LEFT),
        )

        # Cook and Halley
        cook_label, halley_label, romer_label = character_labels[6:9]
        cook_image, halley_image, romer_image = images[6:9]
        romer_image.scale(0.75, about_point=romer_label.get_top())
        self.play(
            frame.animate.match_x(cook_label).set_anim_args(run_time=2),
            FadeIn(cook_label, lag_ratio=0.1),
            FadeIn(cook_image, 0.5 * UP),
            images[3:6].animate.set_opacity(0.25),
            character_labels[3:6].animate.set_opacity(0.25),
        )
        self.wait()
        self.play(
            FadeIn(halley_label, lag_ratio=0.1),
            FadeIn(halley_image, 0.5 * UP),
            cook_image.animate.scale(0.5, about_point=cook_label.get_corner(UR)).shift(0.1 * LEFT),
        )
        self.wait()

        # Romer and Huygens
        romer_label, huygens_label = character_labels[8:10]
        romer_image, huygens_image = images[8:10]
        huygens_image.set_height(1.5).next_to(huygens_label, UP, SMALL_BUFF).shift(0 * LEFT)

        halley_label.target = halley_label.generate_target()
        halley_label.target.rotate(PI, RIGHT, about_edge=DOWN)
        halley_label.target[1].rotate(PI, RIGHT)
        self.play(
            FadeIn(romer_label, lag_ratio=0.1),
            FadeIn(romer_image, 0.5 * UP),
            FadeOut(halley_image),
            MoveToTarget(halley_label),
            cook_image.animate.set_opacity(0.25).match_x(cook_label),
        )
        self.wait()
        self.play(
            FadeIn(huygens_label, lag_ratio=0.1),
            FadeIn(huygens_image, 0.5 * UP),
            romer_image.animate.set_height(1.5).next_to(romer_label, UR, 0).shift(0.25 * LEFT),
            FadeOut(kepler_image),
            FadeOut(cook_image),
            FadeOut(cook_label),
        )
        self.wait()

        # Point out Venus
        venus_points = Group(TrueDot(timeline.n2p(year), color=YELLOW).make_3d() for year in [1761, 1769])
        venus_words = Text("Transit of Venus\nObservations", font_size=30)
        venus_words.next_to(venus_points, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        venus_words.set_color(YELLOW)
        venus_arrows = VGroup(
            Arrow(venus_words["r"][0].get_top(), dot.get_center(), buff=0.1, thickness=1.5).set_color(YELLOW)
            for dot in venus_points
        )
        venus_words.shift(0.1 * DL)

        self.play(
            Write(venus_words),
            FadeIn(venus_points),
            ShowCreation(venus_arrows),
        )
        self.wait()

        # Bessel
        bessel_label = character_labels[10]
        bessel_image = images[10]

        star_words = Text("Measurement of\n61 Cygni", font_size=24)
        star_words.set_color(YELLOW)
        star_point = TrueDot(timeline.n2p(1838), color=YELLOW).make_3d()
        star_words.next_to(star_point, DOWN, buff=0.75)
        star_arrow = Arrow(star_words, star_point, buff=0.1, thickness=2).set_color(YELLOW)

        self.play(
            frame.animate.match_x(bessel_label),
            FadeOut(venus_words),
            FadeOut(venus_arrows),
            venus_points.animate.set_opacity(0.5),
            Write(star_words),
            ShowCreation(star_arrow),
            FadeIn(star_point),
            huygens_image.animate.set_opacity(0.5),
            FadeOut(romer_image),
        )
        self.play(
            FadeIn(bessel_label, lag_ratio=0.1),
            FadeIn(bessel_image, 0.5 * UP),
        )
        self.wait()

        # Add Leavitt and Hubble
        leavitt_label, hubble_label = labels = character_labels[11:13]
        leavitt_image, hubble_image = imgs = images[11:13]
        for image, label in zip(imgs, labels):
            image.set_height(1.5)
            image.next_to(label, UP, SMALL_BUFF)
        hubble_image.match_x(hubble_label.get_right()).shift(0.3 * RIGHT)

        self.play(
            bessel_image.animate.set_opacity(0.25).scale(0.5, about_edge=DOWN),
            FadeOut(star_words),
            FadeOut(star_arrow),
            FadeIn(leavitt_label, lag_ratio=0.1),
            FadeIn(leavitt_image, 0.5 * UP),
            frame.animate.match_x(leavitt_label).set_height(5.0).set_anim_args(run_time=2),
        )
        self.wait()
        self.play(
            FadeIn(hubble_label, lag_ratio=0.1),
            FadeIn(hubble_image, 0.5 * UP),
        )
        self.wait()
