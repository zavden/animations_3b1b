# ==============================================================================
# Scene:      SolarSpectrum
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 1118-1273)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SolarSpectrum.py SolarSpectrum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - solar_spectrum.csv is read from Data/ next to this file (before: Grant's Dropbox) and is a synthetic spectrum.
#
# Placeholder assets (not Grant's originals):
#   - Data/solar_spectrum.csv (synthetic solar spectrum)
#
# Notes:
#   Synthetic spectrum: 5778 K blackbody, 280-2500 nm at 1 nm, columns wavelength/extraterrestrial/global/direct; it includes Fraunhofer lines (H-alpha, H-beta, Na D, Ca H and K, Mg b...) and atmospheric absorption bands (O2, H2O, CO2). The 'gap_points' arrows of the scene are placed by hand for the real spectrum and may not land on the gaps of this one.
# ==============================================================================

from matplotlib import colormaps
from manim_imports_ext import *

class SolarSpectrum(InteractiveScene):
    def construct(self):
        # Get data
        # CHANGE: solar_spectrum.csv lived in Grant's Dropbox; now there is a synthetic spectrum (Data/solar_spectrum.csv) next to this file.
        data_file = str(Path(__file__).parent / 'Data' / 'solar_spectrum.csv')
        self.spectral_cmap = colormaps.get_cmap("Spectral")
        data = np.loadtxt(data_file, delimiter=',')

        wavelength = self.bucket_data(data[:, 0])
        avg_intensity = self.bucket_data(data[:, 1:4].mean(1))

        # Add axes
        axes = Axes((0, 2400, 100), (0, 1, 0.1), height=6, width=11)
        axes.to_corner(UL)

        x_label = Text("Wavelength (nm)", font_size=36)
        x_label.next_to(axes.x_axis.get_end(), UR, buff=SMALL_BUFF)
        x_label.shift_onto_screen(buff=SMALL_BUFF)
        x_coords = VGroup(
            Integer(n, font_size=24).next_to(axes.x_axis.n2p(n), DOWN, MED_SMALL_BUFF)
            for n in range(0, 2800, 400)
        )
        x_label.set_z_index(1)

        self.add(axes)
        self.add(x_label)
        self.add(x_coords)

        # Add lines
        lines = self.get_spectral_lines(axes, wavelength, avg_intensity)

        self.play(LaggedStart(
            (Write(line, stroke_color=WHITE, stroke_width=0.1)
            for line in lines),
            lag_ratio=0.005,
            run_time=5
        ))

        # Show the lump
        def func(wavelen):
            # Not even the right formula...
            T = 1
            c = 1
            h = 1
            freq = c / (wavelen / 2400)
            return (2 * h * freq**5) / (c**2) / (np.exp(h * freq / T) - 1)

        lump = axes.get_graph(func, x_range=(1e-3, 2400, 12))
        lump.set_height(1 * axes.y_axis.get_length(), about_edge=DOWN, stretch=True)

        self.play(VShowPassingFlash(lump, run_time=4, time_width=1.5))

        # Expand
        origin = axes.c2p(0, 0)
        self.play(
            lines.animate.stretch(2, 0, about_point=origin).set_stroke(width=1),
            axes.x_axis.animate.stretch(2, 0, about_point=origin),
            *(
                coord.animate.stretch(2, 0, about_point=origin).stretch(0.5, 0)
                for coord in x_coords
            ),
            run_time=3
        )

        # Highlight gaps
        gap_points = np.array([
            (-3.77, -1.1, 0.0),
            (-2.96, 1.09, 0.0),
            (-2.58, 2.51, 0.0),
            (-1.74, 3.0, 0.0),
        ])
        arrows = VGroup(
            Vector(0.5 * DOWN, thickness=2).set_color(WHITE).move_to(point, DOWN)
            for point in gap_points
        )

        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5))
        self.wait()

        # Show hydrogen spectrum
        spectral_wavelengths = np.array([
            122, 103, 97,  # Lyman
            656, 486, 430, 410,  # Balmer
            1875, 1282, 1094,  # Paschen
        ])
        spectral_lines = self.get_spectral_lines(axes, spectral_wavelengths, np.ones_like(spectral_wavelengths), stroke_width=3)
        for line in spectral_lines:
            line.set_stroke(interpolate_color(line.get_color(), WHITE, 0.25), width=2)
        # spectral_lines.set_height(6, about_edge=DOWN, stretch=True)

        hyd_words = Text("Spectral lines for Hydrogen", font_size=72)
        hyd_words.next_to(spectral_lines, UP, LARGE_BUFF)

        self.play(
            LaggedStartMap(ShowCreation, spectral_lines),
            FadeOut(arrows),
            lines.animate.set_stroke(opacity=0.2),
            self.frame.animate.reorient(0, 0, 0, (3.42, 0.49, 0.0), 12.00).set_anim_args(run_time=2),
            Write(hyd_words, run_time=3),
            x_label.animate.set_x(12.5),
        )
        self.wait()

        # Show red shift
        shift_value = 0.25 * RIGHT
        new_lines = spectral_lines.copy()
        new_lines.shift(shift_value)

        arrow = Vector(5 * RIGHT, thickness=10)
        arrow.move_to(hyd_words, DOWN)

        self.play(FadeOut(hyd_words), lines.animate.set_stroke(opacity=0.1))
        self.play(
            GrowArrow(arrow),
            TransformFromCopy(spectral_lines, new_lines),
            spectral_lines.animate.set_stroke(width=1, opacity=0.5),
        )
        self.wait()

        # Measure the shift
        brace = Brace(VGroup(spectral_lines[3], new_lines[3]), UP, SMALL_BUFF)
        self.play(GrowFromCenter(brace), FadeOut(arrow))
        self.play(
            brace.animate.stretch(3, 0, about_edge=LEFT),
            new_lines.animate.shift(2 * shift_value),
            rate_func=there_and_back,
            run_time=5
        )

    def bucket_data(self, arr, bucket_size=10):  # TODO, change
        full_size = len(arr) - (len(arr) % bucket_size)
        compressed = arr[:full_size].reshape((full_size // bucket_size, bucket_size)).min(1)
        return compressed

    def color_alpha_to_color(self, alpha):
        rgb = np.array(self.spectral_cmap(1 - alpha)[:3])
        brown = np.array([0.55, 0.27, 0.07])
        grey = np.array([0.15, 0.15, 0.15])
        if alpha > 1:
            factor = (np.exp(2 * (1 - alpha)) + 0.2) / 1.2
            rgb = interpolate(grey, rgb, factor)
        elif alpha < 0:
            rgb = interpolate(brown, rgb, np.exp(5 * alpha))
        return Color(rgb=rgb)

    def get_spectral_lines(self, axes, wavelengths, intensities, stroke_width=1):
        color_alpha = inverse_interpolate(380, 780, wavelengths)
        rel_intensities = intensities / intensities.max()
        return VGroup(
            Line(
                axes.c2p(lam, 0),
                axes.c2p(lam, y),
                stroke_color=self.color_alpha_to_color(ca),
                stroke_width=stroke_width
            )
            for lam, y, ca in zip(wavelengths, rel_intensities, color_alpha)
        )
