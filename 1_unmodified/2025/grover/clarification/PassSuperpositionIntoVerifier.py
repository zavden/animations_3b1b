# ==============================================================================
# Scene:      PassSuperpositionIntoVerifier
# Source:     videos/_2025/grover/clarification.py (lines 1118-1291)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl PassSuperpositionIntoVerifier.py PassSuperpositionIntoVerifier -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)



# ----- From _2025/grover/qc_supplements.py -----

def get_blackbox_machine(height=2, color=GREY_D, label_tex="f(n)", label_height_ratio=0.25):
    square = Square(height)
    in_tri = ArrowTip().set_height(0.5 * height)
    out_tri = in_tri.copy().rotate(PI)
    in_tri.move_to(square.get_left())
    out_tri.move_to(square.get_right())
    machine = Union(square, in_tri, out_tri)
    machine.set_fill(color, 1)
    machine.set_stroke(WHITE, 2)

    label = Tex(label_tex)
    label.set_height(label_height_ratio * height)
    label.move_to(machine)
    machine.add(label)

    machine.output_group = VGroup()

    return machine



# ----- From _2025/grover/clarification.py -----

class PassSuperpositionIntoVerifier(InteractiveScene):
    def construct(self):
        # Set up machine
        frame = self.frame
        frame.shift(1.5 * LEFT)
        machine = get_blackbox_machine(label_tex="V")
        machine[-1].set_color(TEAL)
        self.add(machine)

        # Bit string to general input
        bit_ket = KetGroup(Tex("0111...0011"))
        bit_ket.next_to(machine, LEFT, MED_LARGE_BUFF)

        basis_kets = VGroup(
            KetGroup(Tex(R"b_0")),
            KetGroup(Tex(R"b_1")),
            Tex(R"\vdots"),
            KetGroup(Tex(R"b_k")),
            Tex(R"\vdots"),
            KetGroup(Tex(R"b_{n-2}")),
            KetGroup(Tex(R"b_{n-1}")),
        )
        basis_kets.set_submobject_colors_by_gradient(BLUE, BLUE_E)
        basis_kets.arrange(DOWN)
        basis_kets.next_to(machine, LEFT, MED_LARGE_BUFF)
        components = VGroup(
            Tex(R"x_0"), Tex(R"+x_1"), VectorizedPoint(), Tex("+x_k"), VectorizedPoint(), Tex("+x_{n-2}"), Tex(R"+x_{n-1}")
        )
        for comp, ket in zip(components, basis_kets):
            comp.next_to(ket, LEFT, SMALL_BUFF)

        basis_label = Text("Basis")
        basis_label.next_to(bit_ket, LEFT)
        brace = Brace(components, LEFT)
        superposition_word = brace.get_text("Superposition")

        self.add(bit_ket)
        self.play(FadeIn(basis_label))
        self.wait()
        self.play(
            Transform(bit_ket, basis_kets[3]),
            basis_label.animate.next_to(basis_kets[3], LEFT),
        )
        self.wait()
        self.play(
            FadeTransform(basis_label, superposition_word),
            GrowFromCenter(brace),
            FadeIn(basis_kets, lag_ratio=0.1, run_time=2),
            FadeIn(components, lag_ratio=0.1, run_time=2),
        )
        self.remove(bit_ket)
        self.wait()

        # Show the output
        out_kets = basis_kets.copy()
        out_Vs = VGroup(
            Tex(R"V").set_color(TEAL).next_to(ket, LEFT, SMALL_BUFF)
            for ket in out_kets
        )
        VGroup(out_Vs[2], out_Vs[4]).set_opacity(0)
        out_comps = components.copy()
        out_comps.shift(out_Vs[0].get_width() * LEFT)
        out_group = VGroup(out_comps, out_Vs, out_kets)
        out_group.next_to(machine, RIGHT)

        in_group = VGroup(components, basis_kets)

        self.play(
            LaggedStart(
                FadeOutToPoint(in_group.copy(), machine.get_left() + RIGHT, lag_ratio=0.01),
                FadeInFromPoint(out_group, machine.get_right() + LEFT, lag_ratio=0.01),
                lag_ratio=0.5,
                run_time=2
            ),
            frame.animate.center(),
            FadeOut(brace),
            FadeOut(superposition_word),
        )
        self.wait()

        # Show unchanged parts
        last_annotation = VGroup()
        for n in [0, 1, -2, -1]:
            comp = out_comps[n]
            V = out_Vs[n]
            ket = out_kets[n]

            rect = SurroundingRectangle(VGroup(comp, V, ket))
            rect.set_stroke(YELLOW)
            label = Text("Unchanged", font_size=36)
            label.set_color(YELLOW)
            label.next_to(rect, RIGHT)
            annotation = VGroup(rect, label)
            self.play(LaggedStart(
                FadeOut(last_annotation),
                FadeIn(annotation),
                FadeOut(V),
                comp.animate.shift(V.get_width() * RIGHT),
            ))
            last_annotation = annotation
        self.play(FadeOut(annotation))

        # Show key solution
        sol_index = 3
        solution_label = Text("Sudoku\nSolution")
        solution_label.next_to(components[sol_index], LEFT, LARGE_BUFF)
        solution_arrow = Arrow(solution_label, components[sol_index])

        out_rect = SurroundingRectangle(
            VGroup(out_comps[sol_index], out_Vs[sol_index], out_kets[sol_index])
        )
        out_rect.set_stroke(YELLOW)
        flip_word = Text("Flip!")
        flip_word.set_color(YELLOW)
        flip_word.next_to(out_rect, RIGHT)
        new_out_comp = Tex(R"-x_k")
        new_out_comp.next_to(out_kets[sol_index], LEFT, SMALL_BUFF)

        self.play(
            FadeIn(out_rect),
            FadeIn(flip_word),
            Transform(out_comps[sol_index], new_out_comp),
            FadeOut(out_Vs[sol_index], scale=0.25),
        )
        self.play(
            Write(solution_label),
            GrowArrow(solution_arrow)
        )
        self.wait()

        # Parallelization
        lines = VGroup(
            Line(basis_kets[n].get_right(), out_comps[n].get_left(), buff=SMALL_BUFF)
            for n in range(7)
        )

        new_machines = VGroup(machine.copy().scale(0.25).move_to(line) for line in lines)

        pre_machine = VGroup(machine.copy())
        self.remove(machine)
        self.add(lines, Point(), pre_machine)
        self.play(
            Transform(pre_machine, new_machines),
            LaggedStartMap(ShowCreation, lines)
        )
        self.wait()
        self.play(
            FadeOut(lines),
            FadeOut(pre_machine),
            FadeIn(machine),
        )
        self.wait()

        # Column vector
        in_col = TexMatrix(np.array(["x_0", "x_1", R"\vdots", "x_k", R"\vdots", R"x_{n-2}", R"x_{n-1}"]).reshape(-1, 1))
        out_col = TexMatrix(np.array(["x_0", "x_1", R"\vdots", "-x_k", R"\vdots", R"x_{n-2}", R"x_{n-1}"]).reshape(-1, 1))

        for col, vect in zip([in_col, out_col], [LEFT, RIGHT]):
            col.match_height(basis_kets)
            col.next_to(machine, vect)

        self.play(
            FadeOut(solution_label),
            FadeOut(solution_arrow),
            FadeOut(basis_kets),
            FadeOut(out_kets),
            out_rect.animate.surround(out_col.get_entries()[3]).set_stroke(width=1),
            FadeOut(flip_word),
            ReplacementTransform(components, in_col.get_entries()),
            ReplacementTransform(out_comps, out_col.get_entries()),
            Write(in_col.get_brackets()),
            Write(out_col.get_brackets()),
        )
        self.wait()
