# ==============================================================================
# Scene:      CareerFairBooths
# Source:     videos/outside_videos/talent.py (lines 196-229)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CareerFairBooths.py CareerFairBooths -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/outside_videos/talent/booth.svg
#   - _lib/assets/svg_images/booth.svg
#
# Notes:
#   booth.svg is a placeholder SVG generated with _lib/assets/generated/outside_videos/talent/make_talent_svgs.py and copied to _lib/assets/svg_images/ because the code calls SVGMobject('booth').
# ==============================================================================

from manim_imports_ext import *

class CareerFairBooths(InteractiveScene):
    def construct(self):
        # Add booths
        fair_words = Text("Virtual Career Fair", font_size=72)
        fair_words.to_edge(UP)

        booth = SVGMobject('booth')
        booth.set_height(1.35)
        booths = booth.get_grid(3, 2, h_buff=3.5, v_buff=0.75)
        booths.next_to(fair_words, DOWN, buff=LARGE_BUFF)
        for booth in booths:
            booth.set_color(random_bright_color(hue_range=(0.1, 0.2)))

        self.add(fair_words, booths)

        # Show job types
        job_types = BulletedList(
            "Senior roles",
            "New careers",
            "Internships",
            "Part-time",
            buff=0.75
        )
        job_types.move_to(booths).shift(0.5 * UP)

        for n, booth in enumerate(booths):
            booth.generate_target()
            booth.target.shift((-1)**(n + 1) * RIGHT)

        self.play(
            LaggedStartMap(FadeIn, job_types, lag_ratio=0.5, run_time=4),
            LaggedStartMap(MoveToTarget, booths, run_time=4)
        )
        self.wait()
