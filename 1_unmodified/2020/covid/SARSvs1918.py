# ==============================================================================
# Scene:      SARSvs1918
# Source:     videos/_2020/covid.py (lines 1267-1306)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SARSvs1918.py SARSvs1918 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SARSvs1918(Scene):
    def construct(self):
        titles = VGroup(
            OldTexText("2002 SARS outbreak"),
            OldTexText("1918 Spanish flu"),
        )
        images = Group(
            ImageMobject("sars_icon"),
            ImageMobject("spanish_flu"),
        )
        for title, vect, color, image in zip(titles, [LEFT, RIGHT], [YELLOW, RED], images):
            image.set_height(4)
            image.move_to(vect * FRAME_WIDTH / 4)
            image.to_edge(UP)
            title.scale(1.25)
            title.next_to(image, DOWN, MED_LARGE_BUFF)
            title.set_color(color)
            title.underline = Underline(title)
            title.underline.set_stroke(WHITE, 1)
            title.add_to_back(title.underline)

        titles[1].underline.match_y(titles[0].underline)

        n_cases_labels = VGroup(
            OldTexText("8,096 cases"),
            OldTexText("$\\sim$513{,}000{,}000 cases"),
        )

        for n_cases_label, title in zip(n_cases_labels, titles):
            n_cases_label.scale(1.25)
            n_cases_label.next_to(title, DOWN, MED_LARGE_BUFF)

        for image, title, label in zip(images, titles, n_cases_labels):
            self.play(
                FadeIn(image, DOWN),
                Write(title),
                run_time=1,
            )
            self.play(FadeIn(label, UP))
            self.wait()
