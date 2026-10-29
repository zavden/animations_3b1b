# ==============================================================================
# Scene:      NeedleInAHaystackProblem
# Source:     videos/_2025/grover/runtime.py (lines 217-408)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl NeedleInAHaystackProblem.py NeedleInAHaystackProblem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


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


class Superposition(Group):
    def __init__(
        self,
        pieces,
        offset_multiple=0.2,
        max_rot_vel=3,
        glow_color=TEAL,
        glow_stroke_range=(1, 22, 4),
        glow_stroke_opacity=0.05
    ):
        self.pieces = pieces
        self.center_points = Group(
            Point(piece.get_center())
            for piece in pieces
        )
        self.offset_multipler = ValueTracker(offset_multiple)

        for piece, point_mob in zip(pieces, self.center_points):
            piece.center_point = point_mob

            piece.offset_vect = rotate_vector(RIGHT, np.random.uniform(0, TAU))
            piece.offset_vect_rot_vel = np.random.uniform(-max_rot_vel, max_rot_vel)

        glow_strokes = np.arange(*glow_stroke_range)
        glows = pieces.replicate(len(glow_strokes))
        glows.set_fill(opacity=0)
        for glow, sw in zip(glows, glow_strokes):
            glow.set_stroke(glow_color, width=float(sw), opacity=glow_stroke_opacity)

        self.glows = glows

        super().__init__(glows, pieces, self.center_points, self.offset_multipler)
        self.add_updater(lambda m, dt: m.update_piece_positions(dt))

    def update_piece_positions(self, dt):
        offset_multiple = self.offset_multipler.get_value()

        for piece in self.pieces:
            piece.offset_vect = rotate_vector(piece.offset_vect, dt * piece.offset_vect_rot_vel)
            piece.offset_radius = offset_multiple
            piece.move_to(piece.center_point.get_center() + piece.offset_radius * piece.offset_vect)

        for glow in self.glows:
            for sm1, sm2 in zip(glow.family_members_with_points(), self.pieces.family_members_with_points()):
                sm1.match_points(sm2)

    def set_offset_multiple(self, value):
        self.offset_multipler.set_value(value)

    def set_glow_opacity(self, opacity=0.1):
        self.glows.set_stroke(opacity=opacity)



# ----- From _2025/grover/runtime.py -----

class NeedleInAHaystackProblem(InteractiveScene):
    def construct(self):
        # Set up terms
        shown_numbers = list(range(20))
        number_strs = list(map(str, shown_numbers))
        number_set = Tex("".join([
            R"\{",
            *[str(n) + "," for n in shown_numbers],
            R"\dots N - 1"
            R"\}",
        ]), isolate=number_strs)
        number_mobs = VGroup(number_set[n_str][0] for n_str in number_strs)
        number_set.set_width(FRAME_WIDTH - 1)
        number_set.to_edge(UP)

        machine = get_blackbox_machine()
        machine.set_z_index(2)

        self.play(FadeIn(number_set, lag_ratio=0.01))
        self.wait()

        # Show mystery machine
        q_marks = Tex(R"???", font_size=90)
        q_marks.space_out_submobjects(1.2)
        q_marks.next_to(machine, UP)

        self.play(
            FadeIn(machine, scale=2),
            Write(q_marks)
        )
        self.play(LaggedStartMap(FadeOut, q_marks, shift=0.25 * DOWN, lag_ratio=0.1))
        self.wait()

        # Plug in key value
        key_number = 12
        key_input = number_mobs[key_number]
        key_icon = SVGMobject("key").rotate(135 * DEG)
        key_icon.set_fill(YELLOW)
        key_icon.match_width(key_input)
        key_icon.next_to(key_input, DOWN, SMALL_BUFF)

        self.play(
            FlashAround(key_input),
            key_input.animate.set_color(YELLOW),
            FadeIn(key_icon, 0.25 * DOWN)
        )
        self.wait()

        in_mob = key_input.copy().set_color(YELLOW)
        self.play(in_mob.animate.scale(1.5).next_to(machine, LEFT, MED_LARGE_BUFF))
        self.play(self.evaluation_animation(in_mob, machine, True))
        self.wait()

        # Plug in other values
        other_inputs = number_mobs.copy()
        other_inputs.remove(other_inputs[key_number])
        other_inputs.add(number_set["N - 1"][0].copy())
        other_inputs.generate_target()
        other_inputs.target.arrange_in_grid(n_cols=3, buff=MED_SMALL_BUFF)
        other_inputs.target.next_to(machine, LEFT, LARGE_BUFF)

        self.play(
            FadeOut(in_mob, DOWN),
            FadeOut(machine.output_group, DOWN),
            MoveToTarget(other_inputs, lag_ratio=0.01),
        )
        machine.output_group.clear()
        self.play(LaggedStart(
            (self.evaluation_animation(mob, machine)
            for mob in other_inputs),
            lag_ratio=0.2,
        ))
        self.wait()
        self.play(
            FadeOut(other_inputs, shift=0.25 * DOWN, lag_ratio=0.01),
            FadeOut(machine.output_group, 0.25 * DOWN),
        )
        machine.output_group.clear()
        self.wait()

        # Show innards
        innards = Code("""
            def f(n):
                return (n == 12)
        """, font_size=16)
        innards[8:].shift(0.5 * RIGHT)
        innards.move_to(machine).shift(0.25 * LEFT)

        self.play(
            machine.animate.set_fill(opacity=0),
            FadeIn(innards)
        )
        self.wait()
        self.play(
            FadeOut(innards),
            machine.animate.set_fill(opacity=1),
            FadeIn(q_marks, shift=0.25 * UP, lag_ratio=0.25)
        )
        self.play(FadeOut(q_marks))
        self.wait()

        # Guess and check
        last_group = VGroup()
        for n, in_mob in enumerate(number_mobs[:key_number + 1].copy()):
            self.play(
                FadeOut(last_group),
                in_mob.animate.scale(1.5).next_to(machine, LEFT, MED_LARGE_BUFF)
            )
            output = (n == key_number)
            self.play(self.evaluation_animation(in_mob, machine, output))
            last_group = VGroup(in_mob, machine.output_group[0])
            machine.output_group.clear()

        self.wait()
        self.play(FadeOut(last_group))

        # Put into a superposition
        pile = number_mobs.copy()
        for mob in pile:
            mob.scale(0.5)
        superposition = Superposition(pile)
        superposition.set_offset_multiple(0)
        superposition.set_glow_opacity(0)
        superposition.update()

        superposition.generate_target()
        for piece in superposition.pieces:
            piece.scale(2)

        for point in superposition.target[2]:
            point.next_to(machine, LEFT, buff=2.0)
            point.scale(0.5)
            point.shift(np.random.normal(0, 0.5, 3))

        superposition.target[2].arrange(DOWN, buff=0.25).next_to(machine, LEFT, buff=1.5)

        superposition.target.set_offset_multiple(0.1)
        superposition.target.set_glow_opacity(0.1)

        self.play(
            MoveToTarget(superposition, run_time=2),
        )

        # Pass superposition through the function
        answers = VGroup(
            Text("True").set_color(GREEN) if n == key_number else Text("False").set_color(RED)
            for n, piece in enumerate(superposition.pieces)
        )
        answers.match_height(superposition.pieces[0])
        answers.arrange_to_fit_height(superposition.get_height())
        answers.next_to(machine, RIGHT, buff=1.5)
        answers.shuffle()
        answer_superposition = Superposition(answers, glow_color=RED)
        answer_superposition.set_offset_multiple(0)
        answer_superposition.set_glow_opacity(0)
        answer_superposition.update()

        superposition.set_z_index(2)
        self.play(LaggedStart(
            LaggedStart(
                (FadeOutToPoint(glow.copy(), machine.get_left() + 0.5 * RIGHT)
                for glow in superposition.glows),
                lag_ratio=0.1,
            ),
            LaggedStart(
                (FadeInFromPoint(answer, machine.get_right() + 0.5 * LEFT)
                for answer in answer_superposition.pieces),
                lag_ratio=0.05,
            ),
            lag_ratio=0.5
        ))
        self.play(answer_superposition.animate.set_offset_multiple(0.025).set_glow_opacity(1e-2))
        self.wait(10)

    def evaluation_animation(self, input_mob, machine, output=False, run_time=1.0):
        if output:
            out_mob = Text("True").set_color(GREEN)
        else:
            out_mob = Text("False").set_color(RED)
        out_mob.scale(1.25)
        out_mob.next_to(machine, RIGHT, MED_LARGE_BUFF)

        moving_input = input_mob.copy()
        input_mob.set_opacity(0.25)

        machine.output_group.add(out_mob)
        in_point = interpolate(machine.get_left(), machine.get_center(), 0.5)

        return AnimationGroup(
            FadeOutToPoint(moving_input, in_point, time_span=(0, 0.75 * run_time)),
            FadeInFromPoint(out_mob, machine.get_left(), time_span=(0.25 * run_time, run_time)),
        )
