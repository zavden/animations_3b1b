# ==============================================================================
# Scene:      GalacticSurveyData
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1302-1366)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GalacticSurveyData.py GalacticSurveyData -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - galactic_data.csv is read from Data/ next to this file (before: Grant's Dropbox) and is synthetic data.
#
# Placeholder assets (not Grant's originals):
#   - Data/galactic_data.csv (synthetic galaxies: objID, ra, dec, redshift, distance_mpc)
#
# Notes:
#   Synthetic data: ~196 000 galaxies in an SDSS-like cone (ra 110-260, dec -3..65), distributed in filaments and clusters out to ~520 Mpc, with z = (H0 d + v_pec)/c, H0 = 70 km/s/Mpc and v_pec ~ N(0, 300 km/s).
# ==============================================================================

from manim_imports_ext import *

class GalacticSurveyData(InteractiveScene):
    def construct(self):
        # Gather data
        frame = self.frame
        # CHANGE: galactic_data.csv lived in Grant's Dropbox; now there are synthetic galaxies (Data/galactic_data.csv) next to this file.
        data_file = str(Path(__file__).parent / 'Data' / 'galactic_data.csv')
        # Columns are 'objID, ra, dec, redshift, distance_mpc'
        data = np.loadtxt(data_file, delimiter=',', skiprows=2)
        right_ascension = data[:, 1]
        declination = data[:, 2]
        distance = data[:, 4]

        cos_ra = np.cos(right_ascension * DEG)
        sin_ra = np.sin(right_ascension * DEG)
        cos_dec = np.cos(90 * DEG - declination * DEG)
        sin_dec = np.sin(90 * DEG - declination * DEG)

        cartesian = np.array([cos_dec * sin_ra, sin_dec * sin_ra, cos_ra]).T
        cartesian *= distance[:, np.newaxis]

        # Add dots
        dots = DotCloud(cartesian)
        dots.get_width()
        dots.get_height()
        dots.set_color(WHITE)
        dots.set_glow_factor(0.5)

        dots.clear_updaters()
        radii = np.random.random(len(distance))**2
        rad_factor = ValueTracker(0.003)
        dots.f_always.set_radii(lambda: max((rad_factor.get_value() * frame.get_height()**0.9), 0.1) * radii)

        self.add(dots)

        # Zoom out
        # frame.rleorient(-30, 146, 0, (1.89, 0.98, -10.17), 10.71)
        height_tracker = ValueTracker(10)
        angle_tracker = ValueTracker(np.array([-30, 146, 0]))
        center_tracker = ValueTracker(np.array([1.89, 0.98, -10.17]))

        frame.reorient(-22, 151, 0, (0.73, 0.79, -2.36), 13.45)
        self.play(
            frame.animate.reorient(-12, 129, 0, (-18.76, 7.73, -104.01), 439.75),
            rad_factor.animate.set_value(0.0025),
            run_time=12
        )
        self.wait()
        self.play(
            frame.animate.reorient(-115, 86, 0, ORIGIN, 1200),
            rad_factor.animate.set_value(0.002),
            run_time=10
        )
        self.play(
            frame.animate.reorient(107, 87, 0),
            run_time=15,
        )
        self.play(
            frame.animate.reorient(17, 100, 0, (-69.76, -40.26, -81.8), 186.35),
            rad_factor.animate.set_value(0.003),
            run_time=10,
        )
        self.play(
            frame.animate.reorient(-84, 85, 0, ORIGIN, 1100),
            rad_factor.animate.set_value(0.002),
            run_time=10,
        )
