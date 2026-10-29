# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2023/moser_reboot/main.py (lines 8-49)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - Placeholder cautionary_tale.svg ('A Cautionary Tale' text as a single path) in _lib/assets/svg_images/ (make_moser_reboot_assets.py); the code finds it by name, unchanged
# ==============================================================================

from manim_imports_ext import *

class Introduction(InteractiveScene):
    def construct(self):
        # Title
        tale = SVGMobject("cautionary_tale.svg")
        tale.set_fill(GREY_A, 1)
        tale.set_stroke(GREY_A, 2)
        tale.set_width(7)
        tale.center()
        tale.use_winding_fill(False)
        paths = VGroup(*(
            VMobject().set_points(path)
            for path in tale[0].get_subpaths()
        ))
        paths.set_fill(opacity=0)
        paths.set_stroke(width=0)
        paths.sort(lambda p: np.dot(p, RIGHT))
        rect = FullScreenRectangle()
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 0)
        rect.move_to(tale, LEFT)

        self.add(tale)
        self.play(
            rect.animate.next_to(tale, RIGHT, buff=LARGE_BUFF).set_anim_args(rate_func=linear),
            Write(paths, stroke_width=5),
            run_time=3,
        )
        self.remove(rect, paths)
        self.wait()

        # Name
        name = TexText(
            R"Moser's Circle Problem",
            font_size=72,
        )
        name.to_edge(UP)

        self.play(
            FadeOut(tale),
            FadeIn(name, UP)
        )
        self.wait(2)
