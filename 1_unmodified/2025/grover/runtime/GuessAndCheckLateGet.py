# ==============================================================================
# Scene:      GuessAndCheckLateGet
# Source:     videos/_2025/grover/runtime.py (lines 458-459)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl GuessAndCheckLateGet.py GuessAndCheckLateGet -w -m --fps 15
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



# ----- From _2025/grover/runtime.py -----

class LargeGuessAndCheck(InteractiveScene):
    key_value = 42
    wait_time_per_mob = 0.1
    row_size = 10

    def construct(self):
        # Create grid of values and machine
        N = self.row_size
        grid = VGroup(Integer(n) for n in range(int(self.row_size**2)))
        grid.arrange_in_grid(buff=0.75, fill_rows_first=False)
        grid.set_height(FRAME_HEIGHT - 1)

        output = Text("False").set_color(RED)
        output.match_height(grid[0])

        machine = get_blackbox_machine(height=1.5 * grid[0].get_height())
        machine.next_to(output, LEFT, SMALL_BUFF)
        machine_group = VGroup(machine, output)
        extra_width = machine_group.get_width()
        grid.shift(0.5 * extra_width * RIGHT)

        self.add(grid)

        # Sweep through
        self.add(machine_group)
        for n, mob in enumerate(grid):
            if n % self.row_size == 0:
                grid[n:n + self.row_size].shift(extra_width * LEFT)
            machine_group.next_to(mob, RIGHT, buff=0.5 * mob.get_width())
            if n != self.key_value:
                self.play(grid[n].animate.set_opacity(0.5), run_time=self.wait_time_per_mob)
                continue

            new_output = Text("True").set_color(GREEN)
            new_output.replace(machine_group[1])
            machine_group.replace_submobject(1, new_output)
            break

        rect = SurroundingRectangle(grid[n])
        self.play(ShowCreation(rect), grid[n].animate.set_color(YELLOW))
        self.wait()


class GuessAndCheckLateGet(LargeGuessAndCheck):
    key_value = 92
