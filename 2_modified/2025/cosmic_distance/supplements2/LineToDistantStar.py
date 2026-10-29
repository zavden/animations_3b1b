# ==============================================================================
# Scene:      LineToDistantStar
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 1086-1115)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LineToDistantStar.py LineToDistantStar -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GalaxyStill.png is looked up next to this file (before: Grant's video output folder) and is a procedural placeholder galaxy.
#
# Placeholder assets (not Grant's originals):
#   - GalaxyStill.png (face-on spiral galaxy, procedural)
# ==============================================================================

from manim_imports_ext import *

class LineToDistantStar(InteractiveScene):
    def construct(self):
        # Add Galaxy
        # CHANGE: GalaxyStill.png lived next to Grant's video output; now there is a placeholder galaxy next to this file.
        path = os.path.join(os.path.dirname(__file__), "GalaxyStill.png")
        galaxy = ImageMobject(path)
        galaxy.set_height(FRAME_HEIGHT)
        galaxy.center()
        self.add(galaxy)

        # Draw line
        sun_point = (-0.08, -0.74, 0.0)
        star_point = (0.6, 1.54, 0.0)
        line = Line(sun_point, star_point)
        line.set_stroke(TEAL, 4)
        line_label = TexText(R"$\sim$60,000 Light Years", font_size=36)
        line_label.next_to(line.get_center(), RIGHT)
        line_label.set_color(TEAL)
        line_label.set_backstroke(BLACK, 3)

        star = GlowDot(star_point, color=WHITE)
        star.f_always.set_radius(lambda: 0.1 * (2 + math.sin(self.time)))

        self.play(
            ShowCreation(line),
            FadeIn(line_label, lag_ratio=0.1, time_span=(1, 3)),
            galaxy.animate.set_opacity(0.75),
            FadeIn(star),
            run_time=3,
        )
        self.wait(12)
