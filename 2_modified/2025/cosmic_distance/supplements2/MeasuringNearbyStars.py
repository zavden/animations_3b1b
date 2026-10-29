# ==============================================================================
# Scene:      MeasuringNearbyStars
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 800-1074)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MeasuringNearbyStars.py MeasuringNearbyStars -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - HYG_Data.gz is read from Data/ next to this file (before: Grant's Dropbox) and is a synthetic catalog with a plausible H-R diagram.
#   - FadeOut(glows) -> FadeOut(glow): `glows` does not exist in the original (typo, the variable is called `glow`).
#
# Placeholder assets (not Grant's originals):
#   - Data/HYG_Data.gz (synthetic HYG-style star catalog: absmag and ci columns with main sequence, giants, supergiants and white dwarfs)
#
# Extra packages installed in the venv: pandas
#
# Notes:
#   Synthetic data: ~70 000 stars with absmag/ci following a main sequence, giant branches and white dwarfs; it is not the real HYG catalog.
# ==============================================================================

import pandas as pd
import gzip
from manim_imports_ext import *

class MeasuringNearbyStars(InteractiveScene):
    def construct(self):
        # Add the sun
        frame = self.frame
        sun = GlowDot(color=WHITE, radius=0.1)
        sun.center()
        self.add(sun)

        frame.reorient(--270, 63, 0)
        dtheta_tracker = ValueTracker(5 * DEG)
        frame.add_updater(lambda m, dt: m.increment_theta(dtheta_tracker.get_value() * dt))
        self.add(frame)

        # Add the stars
        n_stars = 10000
        n_shown_stars = 1000
        # CHANGE: HYG_Data.gz lived in Grant's Dropbox; now there is a synthetic catalog (Data/HYG_Data.gz) next to this file.
        data_file = str(Path(__file__).parent / 'Data' / 'HYG_Data.gz')
        full_stellar_data, df = self.read_hyg_data(data_file)

        random.shuffle(full_stellar_data)
        stellar_data = full_stellar_data[:n_stars]
        abs_mags = stellar_data[:, 0]
        color_index = stellar_data[:, 1]
        rgbas = self.color_index_to_rgb(color_index)

        opacities = np.ones(n_stars)
        opacities[n_shown_stars:] = 0
        rgbas[n_shown_stars:, 3] = 0

        star_points = np.random.uniform(-1, 1, (n_stars, 3))
        distances = np.random.uniform(0.5, 36, n_stars)**0.5
        star_points *= (distances / np.linalg.norm(star_points, axis=1))[:, np.newaxis]
        stars = GlowDots(star_points, color=WHITE)

        radii = 0.1 * (abs_mags.max() - abs_mags) / (abs_mags.max() - abs_mags.min())
        stars.set_radii(radii)
        stars.set_opacity(opacities)

        self.add(stars)

        # Show distances to various stars
        last_group = VGroup()
        for n in range(10):
            line = Line(ORIGIN, random.choice(star_points))
            line.set_stroke(BLUE, 2)
            label = DecimalNumber(line.get_length() * 10, num_decimal_places=2, unit="L.Y.", font_size=24)
            label[-1].shift(SMALL_BUFF * RIGHT)
            label.set_color(BLUE)
            label.rotate(frame.get_phi(), RIGHT)
            label.rotate(frame.get_theta() + 2 * DEG, OUT)
            vect = normalize(np.cross(line.get_end(), frame.get_implied_camera_location()))
            label.next_to(line.pfp(0.33), vect, SMALL_BUFF)
            self.play(
                ShowCreation(line),
                FadeIn(label, shift=0.25 * OUT),
                FadeOut(last_group),
            )
            self.wait()
            last_group = VGroup(line, label)
        self.play(FadeOut(last_group))

        # Show the colors
        self.play(stars.animate.set_rgba_array(rgbas))
        self.wait(4)

        # Compile into a H.R. plot
        axes = Axes((0, 1, 0.1), (0, 1, 0.1), width=6, height=6)

        x_axis_label = Text("Color", font_size=36)
        x_axis_label.next_to(axes.x_axis, DOWN, SMALL_BUFF)
        y_axis_label = Text("Absolute\nbrightness", font_size=36)
        y_axis_label.next_to(axes.y_axis, LEFT, SMALL_BUFF)

        rand_x = np.random.random(n_stars)
        rand_y = np.random.random(n_stars)
        random_points = axes.c2p(rand_x, rand_y)

        color_alphas = inverse_interpolate(color_index.min(), color_index.max(), color_index)
        mag_alphas = inverse_interpolate(abs_mags.max(), abs_mags.min(), abs_mags)

        sorted_by_color = axes.c2p(color_alphas, rand_y)
        fully_sorted = axes.c2p(color_alphas, mag_alphas)

        new_radii = 0.5 * (radii + 0.05) / 1.5

        self.play(dtheta_tracker.animate.set_value(0))
        self.play(
            FadeIn(axes),
            frame.animate.to_default_state(),
            stars.animate.set_points(random_points).set_radii(new_radii).set_glow_factor(0).make_3d().set_opacity(0.5),
            FadeOut(sun),
            run_time=3
        )
        self.play(
            stars.animate.set_points(sorted_by_color).set_anim_args(run_time=5, path_arc=30 * DEG),
            Write(x_axis_label, run_time=2),
        )
        self.wait()
        self.play(
            stars.animate.set_points(fully_sorted).set_anim_args(run_time=5).set_opacity(0.25),
            Write(y_axis_label, run_time=2),
        )
        self.wait()

        # Circle the main sequence
        ms_circle = Circle().set_stroke(YELLOW, 2)
        ms_circle.set_shape(4.5, 1)
        ms_circle.rotate(-35 * DEG)
        ms_circle.move_to(axes.c2p(0.3, 0.35))

        ms_label = Text("Main sequence", font_size=30)
        ms_label.next_to(ms_circle.pfp(0.1), RIGHT)

        self.play(
            frame.animate.reorient(0, 0, 0, (-0.75, -1.45, 0.0), 5.71).set_anim_args(run_time=3),
            ShowCreation(ms_circle),
            Write(ms_label)
        )
        self.wait()

        # Name the diagram
        name = Text("Hertzsprung–Russell diagram")
        name.center().to_edge(UP)
        name.fix_in_frame()

        self.play(
            Write(name),
            frame.animate.reorient(0, 0, 0, 0.5 * UP, 9),
            run_time=2,
        )
        self.wait()

        # Move around an example star
        example_star = TrueDot().make_3d()
        glow = self.get_glow(example_star)

        def update_example_star(star):
            color_alpha, mag = axes.p2c(star.get_center())
            bv_index = interpolate(color_index.min(), color_index.max(), color_alpha)
            star.set_rgba_array(self.color_index_to_rgb(np.array([bv_index])))
            star.set_radius(0.25 * mag)

        example_star.add_updater(update_example_star)
        example_star.move_to(axes.c2p(0.5, 0.5))

        self.play(
            FadeOut(ms_label),
            FadeOut(ms_circle),
        )
        self.wait()
        self.play(
            stars.animate.set_opacity(0.02),
            FadeIn(example_star),
            FadeIn(glow),
        )
        for x in [-2.5, 0]:
            self.play(example_star.animate.set_x(x), run_time=1.5)

        for y in [2, 0]:
            self.play(example_star.animate.set_y(y), run_time=2)
        self.wait()

        # Place into the main sequence
        opacities = stars.get_opacities().copy()
        ur_values = np.dot(stars.get_points(), np.array([[1, 1.2, 0]]).T).flatten()
        in_ms = ur_values < -1.3
        opacities[in_ms] = 0.2

        ms_arrow = Arrow(UL, DR).rotate(10 * DEG)
        ms_arrow.set_color(GREY_B)
        ms_arrow.move_to(axes.c2p(0.25, 0.25))

        self.play(
            stars.animate.set_opacity(opacities),
            ShowCreationThenFadeOut(ms_circle),
            FadeIn(ms_label),
            example_star.animate.move_to(axes.c2p(0.1, 0.5)),
            run_time=2
        )
        self.play(GrowArrow(ms_arrow))
        self.wait()
        opacities[in_ms] = 0.025

        # Show radiation and shifting down
        self.play(stars.animate.set_opacity(opacities).set_anim_args(run_time=1))
        self.wait(6)
        self.play(
            example_star.animate.move_to(axes.c2p(0.5, 0.2)).set_anim_args(run_time=15),
        )
        self.wait()

        # Return full diagram
        self.play(
            FadeOut(ms_arrow),
            FadeOut(ms_label),
            FadeOut(example_star),
            # CHANGE: `glows` is not defined (a misspelled variable in the original); the object is called `glow`
            FadeOut(glow),
            stars.animate.set_opacity(0.25),
        )
        self.wait()

        # Scan through color regions
        color_x_tracker = ValueTracker(0)
        opacities = stars.get_opacities().copy()

        def update_opacities(stars):
            mid_x = color_x_tracker.get_value()
            xs = stars.get_points()[:, 0]
            opacities[:] = 0.25 * np.exp(-15 * (xs - mid_x)**2) + 0.01
            stars.set_opacity(opacities)

        stars.add_updater(update_opacities)
        self.wait()
        for x in [-2.5, 1.5, 0]:
            self.play(color_x_tracker.animate.set_value(x), run_time=5)
        self.wait()

        stars.clear_updaters()
        self.play(stars.animate.set_opacity(0.25))
        self.wait()

        # Highlight other regions

    def read_hyg_data(self, file_path):
        """
        Read HYG Database from a gzipped file into a numpy array

        Parameters:
        file_path (str): Path to the HYG_Data.gz file

        Returns:
        numpy.ndarray: Array containing the stellar data
        pd.DataFrame: Original dataframe for reference if needed
        """
        # Read the gzipped CSV file
        with gzip.open(file_path, 'rt') as f:
            # Read into pandas first since the file is CSV formatted
            df = pd.read_csv(f)

        # For the H-R diagram, we primarily need:
        # - Color index (B-V)
        # - Absolute magnitude
        # Essential columns for H-R diagram
        essential_cols = ['absmag', 'ci']

        # Create numpy array from essential columns
        stellar_data = df[essential_cols].to_numpy()

        # Remove any rows with NaN values
        stellar_data = stellar_data[~np.isnan(stellar_data).any(axis=1)]

        return stellar_data, df

    def color_index_to_rgb(self, bv_index):
        alpha = inverse_interpolate(-0.2, 2.9, bv_index)
        red = "#FF0000"
        cmap = get_colormap_from_colors(["#0000FF", BLUE, WHITE, YELLOW, ORANGE, RED, * 4 * [red]])
        return cmap(alpha)

    def get_glow(self, star):
        glows = GlowDot().replicate(2)

        def update_glows(glows):
            for dot, delta_t in zip(glows, [0, 1]):
                alpha = (self.time + delta_t) % 2
                if alpha < 1:
                    dot.set_opacity(1)
                    dot.set_radius(interpolate(1, 8, alpha) * star.get_radius())
                else:
                    dot.set_opacity(interpolate(1, 0, alpha - 1))
                dot.set_color(star.get_color())
                dot.move_to(star)

        glows.add_updater(update_glows)
        return glows
