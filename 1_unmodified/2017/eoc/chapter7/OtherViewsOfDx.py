# ==============================================================================
# Scene:      OtherViewsOfDx
# Source:     videos/_2017/eoc/chapter7.py (lines 616-729)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OtherViewsOfDx.py OtherViewsOfDx -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class OtherViewsOfDx(TeacherStudentsScene):
    def construct(self):
        definition = OldTex(
            "{df", "\\over \\,", "dx}", "(", "2", ")", "=",
            "\\lim", "_{h", "\\to", "0}", 
            "{f", "(", "2", "+", "h", ")", "-", "f", "(", "2", ")",
            "\\over \\,", "h}"
        )
        tex_to_color = {
            "df" : YELLOW,
            "f" : YELLOW,
            "dx" : GREEN,
            "h" : GREEN,
            "2" : RED
        }
        for tex, color in list(tex_to_color.items()):
            definition.set_color_by_tex(tex, color)
        definition.scale(0.8)
        definition.to_corner(UP+LEFT)
        dx_group = VGroup(*definition.get_parts_by_tex("dx"))
        h_group = VGroup(*definition.get_parts_by_tex("h"))
        self.add(definition)

        statements = [
            OldTexText(*args)
            for args in [
                ("Why the new \\\\ variable", "$h$", "?"),
                ("$dx$", "is more $\\dots$ contentious."),
                ("$dx$", "is infinitely small"),
                ("$dx$", "is nothing more \\\\ than a symbol"),
            ]
        ]
        for statement in statements:
            statement.h, statement.dx = [
                VGroup(*statement.get_parts_by_tex(
                    tex, substring = False
                )).set_color(GREEN)
                for tex in ("$h$", "$dx$")
            ]

        #Question
        self.student_says(
            statements[0],
            index = 1,
            target_mode = "confused"
        )
        self.play(ReplacementTransform(
            statements[0].h.copy(), h_group,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.wait()

        #Teacher answer
        self.teacher_says(
            statements[1],
            target_mode = "hesitant",
            bubble_creation_class = FadeIn,
        )
        self.play(ReplacementTransform(
            statements[1].dx.copy(), dx_group, 
            run_time = 2,
        ))
        self.wait()

        #First alternate view
        moving_dx = dx_group.copy()
        bubble_intro = PiCreatureBubbleIntroduction(
            self.get_students()[2],
            statements[2],
            target_mode = "hooray",
            bubble_creation_class = FadeIn,
        )
        bubble_intro.update(1)
        dx_movement = Transform(
            moving_dx, statements[2].dx,
            run_time = 2
        )
        bubble_intro.update(0)
        self.play(
            bubble_intro, dx_movement,
            RemovePiCreatureBubble(self.get_teacher()),
        )   
        self.play(self.get_teacher().change_mode, "erm")
        self.wait()

        #Next alternate view
        bubble_intro = PiCreatureBubbleIntroduction(
            self.get_students()[0],
            statements[3],
            target_mode = "maybe",
            look_at = 3*UP,
            bubble_creation_class = FadeIn,
        )
        bubble_intro.update(1)
        dx_movement = Transform(
            moving_dx, statements[3].dx,
            run_time = 2
        )
        bubble_intro.update(0)
        last_bubble = self.get_students()[2].bubble
        self.play(
            bubble_intro, dx_movement,
            FadeOut(last_bubble),
            FadeOut(last_bubble.content),
            *it.chain(*[
                [
                    pi.change_mode, "pondering", 
                    pi.look_at, bubble_intro.mobject
                ]
                for pi in self.get_students()[1:]
            ])
        )
        self.wait(3)
