# ==============================================================================
# Scene:      AskWhatTheParadoxIs
# Source:     videos/_2020/med_test.py (lines 1315-1384)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskWhatTheParadoxIs.py AskWhatTheParadoxIs -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - teacher_says received two strings (old *content API); a single OldTexText with the two parts is passed
# ==============================================================================

from manim_imports_ext import *

class AskWhatTheParadoxIs(TeacherStudentsScene):
    def construct(self):
        # Image
        image = ImageMobject("ppv_image")
        image.replace(self.screen)
        image.set_opacity(0)
        outline = SurroundingRectangle(image, buff=0)
        outline.set_stroke(WHITE, 2)
        outline.set_fill(BLACK, 1)
        image = Group(outline, image)
        image.set_height(3.5, about_edge=UL)

        # What's the paradox?
        self.add(image)
        self.student_says(
            "How's that\\\\a paradox?",
            target_mode="sassy",
            look_at=self.teacher.eyes,
            index=2,
            added_anims=[
                self.students[0].change, "pondering", image,
                self.students[1].change, "pondering", image,
            ]
        )
        self.play(self.teacher.change, 'guilty')
        self.wait(3)

        # Consider test accuracy
        # CHANGE: teacher_says no longer accepts several strings (*content); the OldTexText is built with the two parts
        self.teacher_says(
            OldTexText("Consider the\\\\", "test accuracy")
        )
        self.wait(3)

        # Test accuracy split
        lower_words = self.teacher.bubble.content[1].copy()

        top_words = OldTexText("Test Accuracy", font_size=72)
        top_words.to_corner(UR)
        top_words.shift(LEFT)

        sens_spec = VGroup(
            OldTexText("Sensitivity", color=YELLOW),
            OldTexText("Specificity", color=BLUE_D),
        )
        sens_spec.scale(1)
        sens_spec.arrange(RIGHT, buff=1.0)
        sens_spec.next_to(top_words, DOWN, LARGE_BUFF)
        lines = VGroup(*(
            Line(top_words.get_bottom(), word.get_top(), buff=0.1, color=word.get_color())
            for word in sens_spec
        ))

        globals()['top_words'] = top_words
        self.play(
            TransformFromCopy(lower_words, top_words[0]),
            RemovePiCreatureBubble(
                self.teacher, target_mode="raise_right_hand",
                look_at=top_words,
            ),
            *(ApplyMethod(pi.look_at, top_words) for pi in self.students)
        )
        self.play(
            LaggedStartMap(ShowCreation, lines),
            LaggedStart(*(
                FadeIn(word, shift=word.get_center() - top_words.get_center())
                for word in sens_spec
            )),
            run_time=1,
        )
        self.wait(4)
