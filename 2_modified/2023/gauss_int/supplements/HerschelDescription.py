# ==============================================================================
# Scene:      HerschelDescription
# Source:     videos/_2023/gauss_int/supplements.py (lines 731-795)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HerschelDescription.py HerschelDescription -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Images of Saturn's moons (not in the repo) replaced with placeholder spheres
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Mimas.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Enceladus.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Tethys.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Dione.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Rhea.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Titan.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/Iapetus.png  (placeholder: shaded gray sphere; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HerschelDescription(InteractiveScene):
    def construct(self):
        # Positions
        positions = VGroup(
            Text("Mathematician"),
            Text("Scientist"),
            Text("Inventor"),
        )
        positions.scale(1.5)
        positions.to_edge(RIGHT, buff=1.5)

        last = VGroup()
        for position in positions:
            self.play(
                FadeIn(position, 0.5 * UP),
                FadeOut(last, 0.5 * UP),
            )
            self.wait(0.5)
            last = position
        self.wait()
        self.play(FadeOut(positions[-1]))

         # Contributions
        contributions = VGroup(
            Text("Chemistry"),
            Text("Astronomy"),
            Text("Photography"),
            Text("Botany"),
        )
        contributions.scale(1.25)
        contributions.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        contributions.move_to(3 * RIGHT)
        self.play(ShowIncreasingSubsets(contributions, rate_func=linear, run_time=3))
        self.play(LaggedStartMap(FadeOut, contributions, lag_ratio=0.5, run_time=3))
        self.wait()

        # Moons
        desc = TexText(R"He named many of \\ Saturn's moons")
        desc.move_to(3.5 * RIGHT).to_edge(UP)
        moon_names = VGroup(
            Text("Mimas"),
            Text("Enceladus"),
            Text("Tethys"),
            Text("Dione"),
            Text("Rhea"),
            Text("Titan"),
            Text("Iapetus"),
        )
        moon_names.set_color(GREY_B)
        moon_names.scale(0.75)
        moon_names.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        moons = Group()
        for name in moon_names:
            image = ImageMobject(name.get_string())
            image.set_height(1.25 * name.get_height())
            image.next_to(name, LEFT, buff=0.2)
            moons.add(Group(image, name))

        moons.next_to(desc, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(desc),
            LaggedStartMap(FadeIn, moons, shift=0.5 * DOWN, lag_ratio=0.5, run_time=3)
        )
        self.wait()
