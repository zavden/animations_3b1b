# ==============================================================================
# Scene:      TransitionFromLastVideo
# Source:     videos/_2017/eoc/chapter4.py (lines 18-203)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TransitionFromLastVideo.py TransitionFromLastVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class TransitionFromLastVideo(TeacherStudentsScene):
    def construct(self):
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        simple_rules = VGroup(*list(map(OldTex, [
            "\\frac{d(x^3)}{dx} = 3x^2",
            "\\frac{d(\\sin(x))}{dx} = \\cos(x)",
            "\\frac{d(1/x)}{dx} = -\\frac{1}{x^2}",
        ])))

        combination_rules = VGroup(*[
            OldTex("\\frac{d}{dx}\\left(%s\\right)"%tex)
            for tex in [
                "\\sin(x) + x^2",
                "\\sin(x)(x^2)",
                "\\sin(x^2)",
            ]
        ])
        for rules in simple_rules, combination_rules:
            rules.arrange(buff = LARGE_BUFF)
            rules.next_to(self.get_teacher(), UP, buff = MED_LARGE_BUFF)
            rules.to_edge(LEFT)

        series = VideoSeries()
        series.to_edge(UP)
        last_video = series[2]
        last_video.save_state()
        this_video = series[3]
        brace = Brace(last_video)

        #Simple rules
        self.add(series)
        self.play(
            FadeIn(brace),
            last_video.set_color, YELLOW
        )
        for rule in simple_rules:
            self.play(
                Write(rule, run_time = 2),
                self.get_teacher().change_mode, "raise_right_hand",
                *[
                    ApplyMethod(pi.change_mode, "pondering")
                    for pi in self.get_students()
                ]
            )
            self.wait()
        self.wait(2)
        self.play(simple_rules.replace, last_video)
        self.play(
            last_video.restore,            
            Animation(simple_rules),
            brace.next_to, this_video, DOWN,
            this_video.set_color, YELLOW
        )

        #Combination rules
        self.play(
            Write(combination_rules),
            *[
                ApplyMethod(pi.change_mode, "confused")
                for pi in self.get_students()
            ]
        )
        self.wait(2)
        for rule in combination_rules:
            interior = VGroup(*rule[5:-1])
            added_anims = []
            if rule is combination_rules[-1]:
                inner_func = VGroup(*rule[-4:-2])
                self.play(inner_func.shift, 0.5*UP)
                added_anims = [
                    inner_func.shift, 0.5*DOWN,
                    inner_func.set_color, YELLOW
                ]
            self.play(
                interior.set_color, YELLOW,
                *added_anims,
                lag_ratio = 0.5
            )
            self.wait()
        self.wait()

        #Address subtraction and division
        subtraction = OldTex("\\sin(x)", "-", "x^2")
        decomposed_subtraction = OldTex("\\sin(x)", "+(-1)\\cdot", "x^2")
        pre_division = OldTex("\\frac{\\sin(x)}{x^2}")
        division = VGroup(
            VGroup(*pre_division[:6]),
            VGroup(*pre_division[6:7]),
            VGroup(*pre_division[7:]),
        )
        pre_decomposed_division = OldTex("\\sin(x)\\cdot\\frac{1}{x^2}")
        decomposed_division = VGroup(
            VGroup(*pre_decomposed_division[:6]),
            VGroup(*pre_decomposed_division[6:9]),
            VGroup(*pre_decomposed_division[9:]),
        )
        for mob in subtraction, decomposed_subtraction, division, decomposed_division:
            mob.next_to(
                VGroup(self.get_teacher(), self.get_students()[-1]),
                UP, buff = MED_LARGE_BUFF
            )

        top_group = VGroup(series, simple_rules, brace)
        combination_rules.save_state()
        self.play(
            top_group.next_to, FRAME_Y_RADIUS*UP, UP,
            combination_rules.to_edge, UP,
        )
        pairs = [
            (subtraction, decomposed_subtraction), 
            (division, decomposed_division)
        ]
        for question, answer in pairs:
            self.play(
                Write(question),
                combination_rules.fade, 0.2,
                self.get_students()[2].change_mode, "raise_right_hand",
                self.get_teacher().change_mode, "plain",
            )
            self.wait()
            answer[1].set_color(GREEN)
            self.play(
                Transform(question, answer),
                self.get_teacher().change_mode, "hooray",
                self.get_students()[2].change_mode, "plain",
            )
            self.wait()
            self.play(FadeOut(question))

        #Monstrous expression
        monster = OldTex(
            "\\Big(",
            "e^{\\sin(x)} \\cdot",
            "\\cos\\Big(",
            "\\frac{1}{x^3}",
            " + x^3",
            "\\Big)",
            "\\Big)^4"
        )
        monster.next_to(self.get_pi_creatures(), UP)
        parts = [
            VGroup(*monster[3][2:]),
            VGroup(*monster[3][:2]),
            monster[4],
            VGroup(monster[2], monster[5]),
            monster[1],
            VGroup(monster[0], monster[6])
        ]
        modes = 3*["erm"] + 3*["pleading"]
        for part, mode in zip(parts, modes):
            self.play(
                FadeIn(part, lag_ratio = 0.5),
                self.get_teacher().change_mode, "raise_right_hand",
                *[
                    ApplyMethod(pi.change_mode, mode)
                    for pi in self.get_students()
                ]
            )
        self.wait()
        self.play_student_changes(*["happy"]*3)
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
        words = list(map(OldTexText, [
            "composition", "product", 
            "composition", "sum",
            "composition"
        ]))

        for word, part in zip(words, reversed(parts)):
            word.set_color(YELLOW)
            word.next_to(monster, UP)
            self.play(
                FadeIn(word),
                part.scale, 1.2,
                part.set_color, YELLOW
            )
            self.wait()
            self.play(*list(map(FadeOut, [word, part])))
        self.play(FadeOut(parts[0]))

        #Bring back combinations
        self.play(
            combination_rules.restore,
            *[
                ApplyMethod(pi_creature.change_mode, "pondering")
                for pi_creature in self.get_pi_creatures()
            ]
        )
        self.wait(2)
