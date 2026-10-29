# ==============================================================================
# Scene:      WhyWeNeedProofs
# Source:     videos/_2022/visual_proofs/lies.py (lines 1657-1705)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyWeNeedProofs.py WhyWeNeedProofs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyWeNeedProofs(TeacherStudentsScene):
    def construct(self):
        phrases = VGroup(
            Text("Looks can be deceiving"),
            Text("We need rigor!"),
            Text("We need proofs!"),
        )
        phrases.move_to(self.hold_up_spot, DOWN)
        for phrase in phrases:
            phrase.shift_onto_screen()
            phrase.align_to(phrases[0], LEFT)

        image = ImageMobject("Euclid").set_height(3)
        rect = SurroundingRectangle(image, buff=0)
        rect.set_stroke(WHITE, 2)
        name = Text("Euclid")
        name.next_to(image, DOWN, )
        euclid = Group(image, rect, name)
        euclid.to_corner(UL)

        morty = self.teacher
        ss = self.students

        # Show phrases
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(phrases[0], UP),
            ss[0].change("happy"),
            ss[1].change("tease"),
            ss[2].change("happy"),
        )
        self.wait()
        self.play(
            morty.change("hooray"),
            phrases[0].animate.shift(UP),
            FadeIn(phrases[1], UP),
        )
        self.play(
            phrases[0].animate.shift(UP),
            phrases[1].animate.shift(UP),
            FadeIn(phrases[2], UP),
        )
        self.wait()
        self.play(
            morty.change("tease"),
            FadeIn(euclid, lag_ratio=0.3),
            self.change_students("pondering", "pondering", "thinking", look_at=euclid)
        )
        self.wait(4)
