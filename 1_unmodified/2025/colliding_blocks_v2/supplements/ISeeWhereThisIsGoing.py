# ==============================================================================
# Scene:      ISeeWhereThisIsGoing
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 646-712)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ISeeWhereThisIsGoing.py ISeeWhereThisIsGoing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ISeeWhereThisIsGoing(TeacherStudentsScene):
    def construct(self):
        # Setup
        morty = self.teacher
        stds = self.students
        std = stds[1]
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen)
        )
        self.wait()
        self.play(std.says("I see!", mode="hooray"))
        self.play(morty.change("hesitant"))

        # Show the progression
        mass_terms = VGroup(
            Tex(R"m_1 = 100^n", t2c={"m_1": BLUE}),
            Tex(R"m_2 = 1", t2c={"m_2": BLUE}),
        )
        mass_terms.arrange(DOWN, aligned_edge=LEFT)
        mass_terms.next_to(std.get_corner(UL), UP, buff=0.5)

        implies = Tex(R"\Longrightarrow", font_size=72)
        implies.next_to(mass_terms, RIGHT)
        q_mark = Tex(R"?").next_to(implies, UP, SMALL_BUFF)
        theta_eq = Tex(R"\theta=(0.1)^n")
        theta_eq.next_to(implies, RIGHT)

        group = VGroup(mass_terms, implies, q_mark, theta_eq)

        self.play(
            std.debubble(mode="raise_left_hand", look_at=mass_terms),
            FadeIn(mass_terms, UL, scale=2),
            stds[0].change("hesitant", mass_terms),
            stds[2].change("erm", mass_terms),
        )
        self.wait()
        self.play(
            std.change("raise_right_hand", look_at=theta_eq),
            Write(implies),
            Write(q_mark),
            FadeTransform(mass_terms[0].copy(), theta_eq),
            stds[0].animate.look_at(theta_eq),
            stds[2].animate.look_at(theta_eq),
        )
        self.wait()
        self.play(
            std.change("hooray", group),
            group.animate.set_height(0.75).to_edge(UP),
        )
        self.wait(3)
        self.play(
            morty.says("Almost", mode="well"),
            self.change_students("pondering", "angry", "confused", look_at=morty.eyes)
        )
        self.wait(3)

        # Final statement
        self.play(
            FadeOut(morty.bubble),
            morty.says("One final bit\nof reasoning", mode="speaking"),
            self.change_students("thinking", "hesitant", "happy"),
        )
        self.wait(3)
