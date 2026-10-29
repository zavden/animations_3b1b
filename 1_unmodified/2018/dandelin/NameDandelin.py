# ==============================================================================
# Scene:      NameDandelin
# Source:     videos/_2018/dandelin.py (lines 1242-1286)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameDandelin.py NameDandelin -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameDandelin(Scene):
    CONFIG = {"camera_config": {"background_opacity": 1}}

    def construct(self):
        title = OldTexText(
            "Proof by\\\\",
            "Germinal Pierre Dandelin (1822)"
        )
        title.to_edge(UP)

        portrait = ImageMobject("GerminalDandelin")
        portrait.set_height(5)
        portrait.next_to(title, DOWN)

        google_result = ImageMobject("GoogleDandelin")
        google_result.set_height(4)
        google_result.center()
        google_result.to_corner(DR)

        cmon_google = OldTexText("C'mon Google...")
        cmon_google.set_color(RED)
        cmon_google.next_to(google_result, RIGHT)
        cmon_google.next_to(google_result, UP, aligned_edge=RIGHT)

        dandelion = ImageMobject("DandelionSphere", height=1.5)
        dandelion.to_edge(LEFT, buff=LARGE_BUFF)
        dandelion.shift(UP)
        big_dandelion = dandelion.copy().scale(2)
        big_dandelion.next_to(dandelion, DOWN, buff=0)
        dandelions = Group(dandelion, big_dandelion)

        self.add(title[0])
        self.play(FadeInFromDown(portrait))
        self.play(Write(title[1]))
        self.wait()
        self.play(FadeIn(google_result, LEFT))
        self.play(Write(cmon_google, run_time=1))
        self.wait()

        self.play(LaggedStartMap(
            FadeInFromDown, dandelions,
            lag_ratio=0.7,
            run_time=1
        ))
        self.wait()
