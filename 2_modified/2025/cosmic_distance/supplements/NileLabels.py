# ==============================================================================
# Scene:      NileLabels
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 623-665)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NileLabels.py NileLabels -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Nile.png is looked up next to this file (before: Grant's video output folder) and is a placeholder map.
#
# Placeholder assets (not Grant's originals):
#   - Nile.png (schematic map of the Nile and the delta, placeholder)
# ==============================================================================

from manim_imports_ext import *

class NileLabels(InteractiveScene):
    def construct(self):
        # Add image
        # CHANGE: Nile.png lived next to Grant's video output; now there is a placeholder map next to this file.
        image_path = Path(__file__).parent / "Nile.png"
        image = ImageMobject(image_path)
        image.set_height(FRAME_HEIGHT)

        # Mark points
        alex_point = TrueDot((-5.61, -0.8, 0.0), color=MAROON_D, radius=0.1).make_3d()
        syene_point = TrueDot((2.78, 1.12, 0.0), color=BLUE_D, radius=0.1).make_3d()
        for dot in alex_point, syene_point:
            dot.set_shading(0.25, 0.1, 0.1)
        alex_label = Text("Alexandria", font_size=60, font="CMU Serif").match_color(alex_point)
        alex_label.next_to(alex_point, DR, SMALL_BUFF)
        syene_label = Text("Syene", font_size=60, font="CMU Serif").match_color(syene_point)
        syene_label.next_to(syene_point, UP, SMALL_BUFF)

        line = Line(alex_point, syene_point, buff=0)
        line.insert_n_curves(20)
        # line.set_stroke([MAROON_D, BLUE_D])
        line.set_stroke(GREY_A, 3)

        line_label = TexText(R"$\approx$ 5,000 Stadia")
        line_label.next_to(line.get_center(), UP, SMALL_BUFF)
        line_label.rotate(line.get_angle(), about_point=line.get_center())
        line_label.set_fill(border_width=2)

        group = VGroup(alex_label, syene_label, line_label)
        group.set_fill(border_width=3)
        group.set_backstroke(BLACK, 5)

        self.play(
            FadeIn(alex_point),
            FadeIn(alex_label, lag_ratio=0.1),
        )
        self.play(
            ShowCreation(line, run_time=2),
            FadeIn(syene_point, time_span=(1, 2)),
            FadeIn(syene_label, lag_ratio=0.1, time_span=(1, 2)),
        )
        self.wait()
        self.play(Write(line_label))
        self.wait()
