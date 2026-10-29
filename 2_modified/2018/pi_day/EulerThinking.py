# ==============================================================================
# Scene:      EulerThinking
# Source:     videos/_2018/pi_day.py (lines 747-791)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EulerThinking.py EulerThinking -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/replacement images made by _lib/assets/generated/2018/pi_day/make_pi_day_assets.py (Handmann portrait copy, pixelated/revealed variants, placeholder printed pages)
#
# Notes:
#   Uses MEDIA_DIR (defined in cairo_compat) + file lookup by name in _lib/assets/raster_images.
# ==============================================================================

from manim_imports_ext import *

RESOURCE_DIR = os.path.join(MEDIA_DIR, "3b1b_videos", "π Day 2018", "images")


def get_image(name):
    return ImageMobject(os.path.join(RESOURCE_DIR, name))


class EulerThinking(Scene):
    def construct(self):
        image = get_image("Leonhard_Euler_by_Handmann")
        image.set_height(4)
        image.to_edge(DOWN)
        image.shift(4*LEFT)
        bubble = ThoughtBubble(height = 4.5)
        bubble.next_to(image, RIGHT)
        bubble.to_edge(UP, buff = SMALL_BUFF)
        bubble.shift(0.8*LEFT)
        bubble.set_fill(BLACK, 0.3)

        pi_vs_tau = OldTexText(
            "Should $\\pi$ represent \\\\", "3.1415...", 
            "or", "6.2831...", "?"
        )
        pi_vs_tau.set_color_by_tex_to_color_map({
            "3.14" : GREEN,    
            "6.28" : RED,
        })
        pi_vs_tau.move_to(bubble.get_bubble_center())

        question = OldTex(
            "\\frac{1}{1} + \\frac{1}{4} + \\frac{1}{9} + \\frac{1}{16} + \\cdots = ",
            "\\;???"
        )
        question[0].set_color_by_gradient(BLUE_C, BLUE_B)
        question.move_to(bubble.get_bubble_center())
        question.shift(2*SMALL_BUFF*UP)

        cross = Cross(pi_vs_tau)
        cross.set_stroke(RED, 8)

        self.add(image)
        self.play(
            ShowCreation(bubble),
            Write(pi_vs_tau)
        )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            FadeOut(VGroup(pi_vs_tau, cross)),
            FadeIn(question),
        )
        self.wait()
