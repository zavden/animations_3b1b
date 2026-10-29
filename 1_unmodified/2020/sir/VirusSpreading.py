# ==============================================================================
# Scene:      VirusSpreading
# Source:     videos/_2020/sir.py (lines 3050-3099)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VirusSpreading.py VirusSpreading -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VirusSpreading(Scene):
    def construct(self):
        virus = SVGMobject(file_name="virus")
        virus.set_fill(RED_E, 1)
        virus.set_stroke([RED, WHITE], width=0)
        height = 3
        virus.set_height(height)

        self.play(DrawBorderThenFill(virus))

        viruses = VGroup(virus)

        for x in range(8):
            height *= 0.8
            anims = []
            new_viruses = VGroup()
            for virus in viruses:
                children = [virus.copy(), virus.copy()]
                for child in children:
                    child.set_height(height)
                    child.set_color(interpolate_color(
                        RED_E,
                        GREY_D,
                        0.7 * random.random(),
                    ))
                    child.shift([
                        (random.random() - 0.5) * 3,
                        (random.random() - 0.5) * 3,
                        0,
                    ])
                    anims.append(TransformFromCopy(virus, child))
                    new_viruses.add(child)
            new_viruses.center()
            self.remove(viruses)
            self.play(*anims, run_time=0.5)
            viruses.set_submobjects(list(new_viruses))
        self.wait()

        # Eliminate
        for virus in viruses:
            virus.generate_target()
            virus.target.scale(3)
            virus.target.set_color(WHITE)
            virus.target.set_opacity(0)

        self.play(LaggedStartMap(
            MoveToTarget, viruses,
            run_time=8,
            lag_ratio=3 / len(viruses)
        ))
