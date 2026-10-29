# ==============================================================================
# Scene:      DontWorryAboutDetails
# Source:     videos/_2021/newton_fractal.py (lines 922-1007)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DontWorryAboutDetails.py DontWorryAboutDetails -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RasterizingBezier_1.png y RasterizingBezier_2.png (placeholder; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class DontWorryAboutDetails(TeacherStudentsScene):
    CONFIG = {
        "background_color": BLACK,
    }

    def construct(self):
        screen = self.screen
        screen.set_height(4, about_edge=UL)
        screen.set_fill(BLACK, 1)
        image1, image2 = [
            ImageMobject(f"RasterizingBezier_{i}").replace(screen)
            for i in range(1, 3)
        ]

        frame = self.camera.frame
        frame.save_state()
        frame.replace(image1)

        self.add(screen, image1)

        self.play(Restore(frame))

        # Student asks about what the function is.
        self.student_says(
            OldTexText("Wait, what is that\\\\function exactly?"),
            look_at=image1,
            index=2,
            added_anims=[
                self.students[0].change("confused", image1),
                self.students[1].change("confused", image1),
            ]
        )
        self.play(self.teacher.change("tease"))
        self.wait(2)
        self.play(
            self.students[0].change("maybe", image1),
        )
        self.play(
            self.students[1].change("erm", image1),
        )
        self.wait(3)

        self.teacher_says(
            OldTexText("Just some\\\\polynomial"),
            bubble_config={
                "width": 4,
                "height": 3,
            },
            added_anims=[self.change_students("confused", "maybe", "pondering")]
        )
        self.wait()
        self.look_at(image1)
        self.play(
            frame.animate.replace(image1),
            RemovePiCreatureBubble(self.teacher),
            run_time=2
        )
        self.wait()

        # Image 2
        self.remove(image1)
        self.add(image2)
        self.play(Restore(frame))

        self.play_all_student_changes(
            "confused",
            look_at=image1,
        )
        self.teacher_says(
            OldTex("P(x) = 0"),
            target_mode="tease",
            bubble_config={
                "width": 3,
                "height": 3,
            }
        )
        self.wait(4)
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand", look_at=image1),
            self.change_students(
                *3 * ["pondering"],
                look_at=image1,
            ),
            FadeOut(image2),
        )
        self.wait(4)
