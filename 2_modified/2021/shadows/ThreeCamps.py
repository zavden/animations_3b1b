# ==============================================================================
# Scene:      ThreeCamps
# Source:     videos/_2021/shadows.py (lines 3817-3904)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeCamps.py ThreeCamps -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Shadows_Integral_Intro.png  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
# ==============================================================================

from manim_imports_ext import *

class ThreeCamps(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        # Setup
        teacher = self.teacher
        students = self.students

        image = ImageMobject("Shadows_Integral_Intro")
        image.center().set_height(FRAME_HEIGHT)
        image.generate_target()
        image.target.replace(self.screen)
        self.screen.set_stroke(WHITE, 1)
        self.screen.save_state()
        self.screen.replace(image).set_stroke(width=0)

        self.play(
            LaggedStart(*(
                student.change("pondering", image.target)
                for student in students
            ), run_time=2, lag_ratio=0.2),
            teacher.change("tease")
        )
        self.wait()

        # Reactions
        phrases = [
            Text("How fun!", font_size=40),
            Text("Wait, what?", font_size=40),
            Text("Okay give\nme a sec...", font_size=35),
        ]
        modes = ["hooray", "erm", "confused"]
        heights = np.linspace(2.0, 2.5, 3)
        for student, phrase, mode, height in zip(reversed(students), phrases, modes, heights):
            self.play(
                PiCreatureSays(
                    student, phrase, target_mode=mode,
                    look_at=image,
                    bubble_config={
                        "direction": LEFT,
                        "width": 3,
                        "height": height,
                    },
                    bubble_type=ThoughtBubble,
                    run_time=2
                )
            )
        self.wait(4)

        # Let's go over the definition
        integral = OldTex("\\int_0^\\pi \\dots d\\theta")
        integral.move_to(self.hold_up_spot, DOWN)
        brace = Brace(integral, UP)
        words = OldTexText("Let's go over the definition", font_size=36)
        words.next_to(brace, UP, SMALL_BUFF)
        words2 = OldTexText("It can't hurt, right?", font_size=36)
        words2.move_to(words)
        VGroup(brace, words, words2).set_color(YELLOW)

        self.play(
            LaggedStart(*(
                FadeOut(VGroup(student.bubble, student.bubble.content))
                for student in reversed(students)
            )),
            LaggedStart(*(
                student.change("pondering", integral)
                for student in students
            )),
            FadeIn(integral, UP),
            teacher.change("raise_right_hand", integral),
        )
        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait(2)
        self.play(
            words.animate.shift(0.75 * UP).set_opacity(0.5),
            FadeIn(words2, 0.2 * UP),
            LaggedStart(
                self.teacher.change("shruggie"),
                self.students[0].change("sassy", words2),
                self.students[1].change("thinking", words2),
                self.students[2].change("well", words2),
            )
        )
        self.wait(2)
        self.play(self.teacher.change("speaking", words2))
        self.wait(3)
