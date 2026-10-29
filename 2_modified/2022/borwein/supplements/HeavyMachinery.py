# ==============================================================================
# Scene:      HeavyMachinery
# Source:     videos/_2022/borwein/supplements.py (lines 264-325)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HeavyMachinery.py HeavyMachinery -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
# ==============================================================================

from manim_imports_ext import *

class HeavyMachinery(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(
            stds[2].says("Why on earth are\nthose two related?", bubble_direction=LEFT, look_at=self.screen),
            morty.change("tease"),
            stds[0].change("pleading", self.screen),
            stds[1].change("confused", self.screen),
        )
        self.wait(2)
        self.play(self.change_students("maybe", "confused", "hesitant"))
        self.wait(2)

        # Heavy machinery
        kw = dict(font_size=60)
        ft = Text("Fourier Transforms", **kw)
        conv = OldTexText("Convolution", "s", **kw)
        conv_thm = OldTexText("The ", "Convolution", R"\\Theorem", **kw)
        for text in ft, conv, conv_thm:
            text.move_to(self.hold_up_spot, DOWN)

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(ft, UP),
            stds[2].debubble(mode="guilty", look_at=ft),
            stds[0].change("erm", look_at=ft),
            stds[1].change("sad", look_at=ft),
        )
        self.wait()
        self.play(
            FadeIn(conv, UP),
            ft.animate.next_to(conv, UP, MED_LARGE_BUFF)
        )
        self.wait(2)
        self.play(morty.change("tease"))
        self.wait()

        # Don't want to assume
        ft.save_state()
        conv.save_state()
        self.play(
            morty.says("First, a high\nlevel overview", bubble_direction=RIGHT),
            self.change_students("skeptical", "erm", "pondering"),
            VGroup(ft, conv).animate.scale(0.55).to_corner(UR),
        )
        self.wait(3)

        self.play(
            morty.debubble(mode="raise_right_hand"),
            conv.animate.restore(),
            self.change_students("pondering", "thinking", "thinking", look_at=self.screen),
        )
        self.wait(4)

        # Mention theorem
        self.play(
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            TransformMatchingShapes(conv, conv_thm),
            morty.change("hooray", conv_thm),
        )
        self.play(self.change_students("thinking", "hesitant", "pondering", look_at=conv_thm))
        self.wait(3)
