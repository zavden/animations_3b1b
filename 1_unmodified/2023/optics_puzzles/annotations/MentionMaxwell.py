# ==============================================================================
# Scene:      MentionMaxwell
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 429-537)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionMaxwell.py MentionMaxwell -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MentionMaxwell(TeacherStudentsScene):
    def construct(self):
        # Introduce
        stds = self.students
        morty = self.teacher
        kw = dict(
            tex_to_color_map={
                R"\mathbf{E}": BLUE,
                R"\mathbf{B}": YELLOW,
            },
            font_size=30,
        )
        maxwells_equations = VGroup(
            Tex(R"\nabla \cdot \mathbf{E}=\frac{\rho}{\varepsilon_0}", **kw),
            Tex(R"\nabla \cdot \mathbf{B}=0", **kw),
            Tex(R"\nabla \times \mathbf{E}=-\frac{\partial \mathbf{B}}{\partial t}", **kw),
            Tex(R"\nabla \times \mathbf{B}=\mu_0\left(\mathbf{J}+\varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}\right)", **kw),
        )
        maxwells_equations.arrange(DOWN, aligned_edge=LEFT)
        equations_rect = SurroundingRectangle(maxwells_equations, buff=0.25)
        equations_rect.set_stroke(WHITE, 1)
        equations_rect.set_fill(BLACK, 1)
        maxwells_equations.add_to_back(equations_rect)

        maxwells_equations.next_to(stds[2].get_corner(UR), UP)
        maxwells_equations.shift(MED_SMALL_BUFF * UP)
        equations_title = Text("Maxwell's Equations")
        equations_title.next_to(maxwells_equations, UP, buff=0.25)

        self.play(
            stds[2].says(TexText(R"What about \\ Maxwell's equations?")),
            morty.change("tease"),
            self.change_students("confused", "pondering")
        )
        self.play(
            stds[2].change("raise_right_hand"),
            FadeIn(maxwells_equations, UP),
        )
        self.play(
            FadeTransform(stds[2].bubble.content["Maxwell's equations"].copy(), equations_title),
            stds[2].debubble(),
            *(pi.animate.look_at(equations_title) for pi in [morty, *stds[:2]]),
        )
        self.wait()
        self.play(self.change_students("maybe", "erm", look_at=maxwells_equations))
        self.wait(4)

        maxwells_equations.add(equations_title)

        # Lorentz law
        maxwells_equations.generate_target()
        maxwells_equations.target.scale(0.7).to_edge(LEFT)

        equation = Tex(R"""
            \vec{E}_{\text{rad}}(\vec{r}, t) = 
            {-q \over 4\pi \epsilon_0 c^2}
            {1 \over ||\vec{r}||}
            \vec{a}_\perp(t - ||\vec{r}|| / c)
        """, font_size=42)
        lhs = equation[R"\vec{E}_{\text{rad}}(\vec{r}, t)"]
        lhs.set_color(BLUE)
        equation[R"\vec{a}_\perp("].set_color(PINK)
        equation[R")"][1].set_color(PINK)

        equation.next_to(morty.get_corner(UL), UP)
        equation.shift_onto_screen()
        equation.match_y(maxwells_equations)
        eq_rect = SurroundingRectangle(equation)
        eq_rect.set_stroke(BLUE, 2)
        eq_rect.set_fill(BLUE, 0.1)

        implies_arrow = Arrow(eq_rect, maxwells_equations.target)
        implies_word = Text("Derived from these", font_size=30)
        implies_word.next_to(implies_arrow, UP)

        question = Text("How far will this take us?")
        question.next_to(equation, UP, buff=2.0)
        question.shift_onto_screen()
        arrow = Arrow(equation, question)

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(equation, 0.5 * UP),
            MoveToTarget(maxwells_equations),
            GrowArrow(implies_arrow),
            FadeIn(implies_word, lag_ratio=0.1),
            self.change_students("well", "happy")
        )
        self.wait()
        self.add(eq_rect, equation)
        self.play(
            FadeIn(eq_rect),
            ShowCreation(arrow),
            FadeIn(question, lag_ratio=0.1),
            morty.change("tease", look_at=question),
            self.change_students("tease", "well", "happy", look_at=equation)
        )
        self.wait(4)

        # Remove
        self.remove(equation)
        everything = Group(*self.mobjects)

        self.play(
            LaggedStartMap(FadeOut, everything),
            equation.copy().animate.scale(36.0 / 42).to_corner(UR),
            run_time=1,
        )
        self.wait()
