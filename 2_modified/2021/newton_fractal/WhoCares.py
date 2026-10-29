# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2021/newton_fractal.py (lines 329-384)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RealNewtonStill.png (placeholder; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        screen = self.screen
        screen.set_height(4, about_edge=UL)
        screen.set_fill(BLACK, 1)
        image = ImageMobject("RealNewtonStill")
        image.replace(screen)

        self.add(screen)
        self.add(image)

        self.wait()
        self.play(LaggedStart(
            PiCreatureSays(
                self.students[1], "Ooh, quintics...",
                target_mode="thinking",
                look_at=self.screen,
                bubble_config={
                    "direction": LEFT,
                    "width": 4,
                    "height": 2,
                }
            ),
            self.teacher.change("happy"),
            self.students[0].change("thinking", screen),
            self.students[2].change("sassy", screen),
            lag_ratio=0.1,
        ))
        self.wait(3)
        self.play(LaggedStart(
            PiCreatureSays(
                self.students[2], "Who cares?",
                target_mode="tired",
                bubble_config={
                    "direction": LEFT,
                    "width": 4,
                    "height": 3,
                }
            ),
            self.teacher.change("guilty"),
            self.students[0].change("confused", screen),
            RemovePiCreatureBubble(
                self.students[1],
                look_at=self.students[2].eyes,
                target_mode="erm",
            ),
            lag_ratio=0.1,
        ))
        self.wait(2)
        self.teacher_says(
            "Who doesn't",
            target_mode="hooray",
            bubble_config={"height": 3, "width": 4},
            added_anims=[self.change_students("pondering", "pondering", "confused")]
        )
        self.wait(3)
