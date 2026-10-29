# ==============================================================================
# Scene:      BuildUpFromStart
# Source:     videos/_2018/eop/combinations.py (lines 1617-1744)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BuildUpFromStart.py BuildUpFromStart -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - stacks.deepcopy() -> stacks.copy() (GL deepcopy recurses infinitely on circular references)
#   - top_stacks.numbers = stacks.numbers.copy() (copy() does not duplicate the numbers attribute that deepcopy duplicated)
# ==============================================================================

from manim_imports_ext import *

class Male(Tex):
    CONFIG = {
        "height" : 0.4,
        "tex" : "\\male",
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Tex.__init__(self, self.tex, **kwargs)
        self.set_height(self.height)
        self.set_color(self.color)


class Female(Male):
    CONFIG = {
        "tex" : "\\female",
        "color" : MAROON_B,
    }


class BuildUpFromStart(Scene):
    CONFIG = {
        "n_iterations" : 7,
    }
    def construct(self):
        stacks = VGroup(VGroup(Male()), VGroup(Female()))
        stacks.arrange(RIGHT, buff = LARGE_BUFF)
        stacks.numbers = self.get_numbers(stacks)

        max_width = FRAME_WIDTH - 3
        max_height = FRAME_Y_RADIUS - 1

        self.add(stacks, stacks.numbers)
        for x in range(self.n_iterations):
            if x < 2:
                wait_time = 1
            else:
                wait_time = 0.2
            #Divide
            low_stacks = stacks
            low_group = VGroup(low_stacks, low_stacks.numbers)
            # CHANGE: GL deepcopy() recurses forever on these coin stacks (circular references); copy() is enough here
            top_stacks = stacks.copy()
            # CHANGE: copy() does not duplicate the .numbers VGroup attribute (deepcopy did); copy it too so top and low rows have their own numbers
            top_stacks.numbers = stacks.numbers.copy()
            top_group = VGroup(top_stacks, top_stacks.numbers)
            for group, vect in (top_group, UP), (low_group, DOWN):
                group.generate_target()
                if group[0].get_height() > max_height:
                    group.target[0].stretch_to_fit_height(max_height)
                    for stack, num in zip(*group.target):
                        num.next_to(stack, UP)
                group.target.next_to(ORIGIN, vect)
            self.play(*list(map(MoveToTarget, [top_group, low_group])))
            self.wait(wait_time)

            #Expand
            for stacks, i in (low_stacks, 0), (top_stacks, -1):
                sym = stacks[i][i][i]
                new_stacks = VGroup()
                for stack in stacks:
                    new_stack = VGroup()
                    for line in stack:
                        new_line = line.copy()
                        new_sym = sym.copy()
                        buff = 0.3*line.get_height()
                        new_sym.next_to(line, RIGHT, buff = buff)
                        new_line.add(new_sym)
                        line.add(VectorizedPoint(line[-1].get_center()))
                        new_stack.add(new_line)
                    new_stacks.add(new_stack)
                new_stacks.arrange(
                    RIGHT, buff = LARGE_BUFF, aligned_edge = DOWN
                )
                if new_stacks.get_width() > max_width:
                    new_stacks.stretch_to_fit_width(max_width)
                if new_stacks.get_height() > max_height:
                    new_stacks.stretch_to_fit_height(max_height)
                new_stacks.move_to(stacks, DOWN)
                stacks.target = new_stacks
                stacks.numbers.generate_target()

                for num, stack in zip(stacks.numbers.target, new_stacks):
                    num.next_to(stack, UP)
            self.play(*list(map(MoveToTarget, [
                top_stacks, low_stacks,
                top_stacks.numbers, low_stacks.numbers,
            ])))
            self.wait(wait_time)

            #Shift
            dist = top_stacks[1].get_center()[0] - top_stacks[0].get_center()[0]
            self.play(
                top_group.shift, dist*RIGHT/2,
                low_group.shift, dist*LEFT/2,
            )
            self.wait(wait_time)

            #Stack
            all_movers = VGroup()
            plusses = VGroup()
            expressions = VGroup(low_stacks.numbers[0])
            stacks = VGroup(low_stacks[0])
            v_buff = 0.25*stacks[0][0].get_height()

            for i, top_stack in enumerate(top_stacks[:-1]):
                low_stack = low_stacks[i+1]
                top_num = top_stacks.numbers[i]
                low_num = low_stacks.numbers[i+1]
                movers = [top_stack, top_num, low_num]
                for mover in movers:
                    mover.generate_target()
                plus = OldTex("+")
                expr = VGroup(top_num.target, plus, low_num.target)
                expr.arrange(RIGHT, buff = SMALL_BUFF)
                top_stack.target.next_to(low_stack, UP, buff = v_buff)
                expr.next_to(top_stack.target, UP)

                all_movers.add(*movers)
                plusses.add(plus)
                expressions.add(VGroup(top_num, plus, low_num))
                stacks.add(VGroup(*it.chain(low_stack, top_stack)))

            last_group = VGroup(top_stacks[-1], top_stacks.numbers[-1])
            last_group.generate_target()
            last_group.target.align_to(low_stacks, DOWN)
            all_movers.add(last_group)
            stacks.add(top_stacks[-1])
            expressions.add(top_stacks.numbers[-1])

            self.play(*it.chain(
                list(map(MoveToTarget, all_movers)),
                list(map(Write, plusses)),
            ))

            #Add
            new_numbers = self.get_numbers(stacks)
            self.play(ReplacementTransform(
                expressions, VGroup(*list(map(VGroup, new_numbers)))
            ))
            self.wait(wait_time)
            stacks.numbers = new_numbers


    ####

    def get_numbers(self, stacks):
        return VGroup(*[
            OldTex(str(len(stack))).next_to(stack, UP)
            for stack in stacks
        ])
