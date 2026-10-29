# ==============================================================================
# Scene:      DesiredMachine
# Source:     videos/_2025/laplace/main_equations.py (lines 488-629)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DesiredMachine.py DesiredMachine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - show_ode is read as self.show_ode (it was a NameError)
# ==============================================================================

from manim_imports_ext import *

class DesiredMachine(InteractiveScene):
    show_ode = True

    def construct(self):
        # Add machine
        machine = self.get_machine()
        machine.rotate(90 * DEG)
        machine.center()
        fancy_L = Tex(R"\mathcal{L}", font_size=120)
        fancy_L.move_to(machine)
        machine.set_z_index(1)
        fancy_L.set_z_index(1)

        self.add(machine, fancy_L)

        # Pump in a function
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        in_func = Tex(R"x({t})", t2c=t2c, font_size=90)
        in_func[re.compile("s_.")].set_color(YELLOW)
        in_func.next_to(machine, UP, MED_LARGE_BUFF)
        in_func_ghost = in_func.copy().set_fill(opacity=0.5)

        self.play(Write(in_func))
        self.wait()
        self.add(in_func_ghost)
        self.play(
            FadeOutToPoint(in_func, machine.get_bottom(), lag_ratio=0.025)
        )
        self.wait()

        # Pump in a differential equation
        # CHANGE: show_ode is a class attribute; in the original it was used as a global variable (NameError).
        if self.show_ode:
            ode = Tex(R"m x''({t}) + \mu x'({t}) + k x(t) = F_0 \cos(\omega{t})", t2c=t2c, font_size=60)
            ode.next_to(machine, UP, MED_LARGE_BUFF)
            ode_ghost = ode.copy().set_fill(opacity=0.5)

            self.play(
                in_func_ghost.animate.to_edge(UP, buff=MED_SMALL_BUFF),
                FadeIn(ode, lag_ratio=0.1),
            )
            self.wait()
            self.add(ode_ghost)
            self.play(LaggedStart(
                (FadeOutToPoint(piece, machine.get_top() + 0.5 * DOWN, path_arc=arc)
                for piece, arc in zip(ode, np.linspace(-70 * DEG, 70 * DEG, len(ode)))),
                lag_ratio=0.05,
                run_time=2
            ))
            self.wait()

        # Result
        out_func = Tex(R"x({t}) = c_1 e^{s_1 {t}} + c_2 e^{s_2 {t}} + c_3 e^{s_3 {t}} + c_4 e^{s_4 {t}}", t2c=t2c, font_size=72)
        # out_func = Tex(R"x({t}) = \sum_{n=1}^N c_n e^{s_n {t}}", t2c=t2c, font_size=72)
        s_parts = out_func[re.compile("s_.")]
        c_parts = out_func[re.compile("c_.")]
        s_parts.set_color(YELLOW)
        c_parts.set_color(GREY_A)
        out_func.next_to(machine, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStart(
            (FadeInFromPoint(piece, machine.get_bottom() + 0.5 * UP, path_arc=arc)
            for piece, arc in zip(out_func, np.linspace(-70 * DEG, 70 * DEG, len(out_func)))),
            lag_ratio=0.05,
            run_time=2
        ))

        # Make way for Laplace Transform words
        if False:
            # For an insert
            text = Text("Laplace Transform", font_size=72)
            machine.set_z_index(0)
            self.play(
                LaggedStart(
                    FadeOut(in_func_ghost, UP),
                    FadeOut(ode_ghost, 2 * UP),
                    FadeOut(out_func, DOWN),
                    FadeTransform(fancy_L[0], text[0]),
                    FadeIn(text[1:], lag_ratio=0.1),
                    run_time=2,
                    lag_ratio=0.2
                ),
                FadeOut(machine, scale=3, run_time=2)
            )
            self.wait()

        # Highlight s and c
        s_rects = VGroup(SurroundingRectangle(part, buff=0.05) for part in s_parts)
        c_rects = VGroup(SurroundingRectangle(part, buff=0.05) for part in c_parts)
        s_rects.set_stroke(YELLOW, 2)
        c_rects.set_stroke(WHITE, 2)

        s_part_copies = s_parts.copy()
        c_part_copies = c_parts.copy()

        self.add(s_part_copies)
        self.play(
            Write(s_rects),
            out_func.animate.set_opacity(0.75),
        )
        self.wait()
        self.play(
            ReplacementTransform(s_rects, c_rects, lag_ratio=0.1),
            FadeOut(s_part_copies),
            FadeIn(c_part_copies),
        )
        self.wait()
        self.play(FadeOut(c_rects), out_func.animate.set_fill(opacity=1))
        self.remove(c_part_copies)

        # Ask about exponential pieces
        mobs = Group(*self.mobjects)
        randy = Randolph()
        randy.move_to(5 * LEFT + 3 * DOWN, DL)
        randy.look_at(out_func),
        exp_piece = Tex(R"e^{{s}{t}}", t2c=t2c, font_size=90)
        exp_piece.next_to(randy, UR, LARGE_BUFF).shift(0.5 * DOWN)
        exp_piece.insert_submobject(2, VectorizedPoint(exp_piece[2].get_right()))

        self.play(
            LaggedStartMap(FadeOut, mobs, run_time=2),
            TransformFromCopy(out_func["e^{s_1 {t}}"][0], exp_piece, run_time=2),
            VFadeIn(randy, time_span=(0.5, 2.0)),
            randy.change("confused", exp_piece).set_anim_args(run_time=2),
        )
        self.play(Blink(randy))
        self.wait()
        for mode in ["pondering", "thinking", "tease"]:
            self.play(randy.change(mode, exp_piece))
            self.play(Blink(randy))
            self.wait(2)

    def get_machine(self, width=1.5, height=2, color=GREY_D):
        square = Rectangle(width, height)
        in_tri = ArrowTip().set_height(0.5 * height)
        in_tri.stretch(2, 1)
        out_tri = in_tri.copy().rotate(PI)
        in_tri.move_to(square.get_left())
        out_tri.move_to(square.get_right())
        machine = Union(square, in_tri, out_tri)
        machine.set_fill(color, 1)
        machine.set_stroke(WHITE, 2)
        return machine
