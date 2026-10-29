# ==============================================================================
# Scene:      ErdosKac
# Source:     videos/_2023/clt/wordy_scenes.py (lines 69-183)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl ErdosKac.py ErdosKac -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy


# ----- From _2023/clt/main.py -----

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)



# ----- From _2023/clt/wordy_scenes.py -----

class ErdosKac(InteractiveScene):
    def construct(self):
        # Title
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        VGroup(h_line, v_line).set_stroke(GREY_A, 1)
        h_line.to_edge(UP, buff=1.0)
        titles = VGroup(
            Tex("N"),
            TexText(R"\# of distinct prime factors of $N$"),
        )
        titles.next_to(h_line, UP)
        titles[0].set_x(-FRAME_WIDTH * 0.25)
        titles[1].set_width(6)
        titles[1].to_edge(RIGHT)
        v_line.set_x(titles[1].get_x(LEFT) - 0.25)

        self.add(titles)
        self.add(h_line)

        # Number line
        number_line = NumberLine((0, 10), width=10)
        number_line.add_numbers(excluding=[0])
        number_line.numbers.shift(number_line.get_unit_size() * LEFT / 2)
        number_line.to_edge(DOWN, buff=LARGE_BUFF)
        self.add(number_line)

        stacks = VGroup(*(
            VGroup(VectorizedPoint(number_line.n2p(x - 0.5)))
            for x in range(1, 20)    
        ))
        self.add(stacks)

        rect_template = Rectangle(width=number_line.get_unit_size(), height=0.1)
        rect_template.set_stroke(BLUE_E, 0.5)
        rect_template.set_fill(TEAL_E, 0.5)

        # Add normal curve
        mean = math.log(math.log(1e18))
        sd = math.sqrt(mean)
        curve = FunctionGraph(lambda x: 10 * gauss_func(x, mean, sd), x_range=(0, 10, 0.25))
        curve.set_stroke(RED, 2)
        curve.match_width(number_line)
        curve.move_to(number_line.n2p(0), DL)
        self.add(curve)

        # Show many numbers
        num = int(1e18)
        group = VGroup()

        for x in range(0, 100):
            rect = rect_template.copy()
            nf = len(sympy.factorint(num + x))
            stack = stacks[nf - 1]
            rect.next_to(stack, UP, buff=0)
            rect.set_fill(YELLOW)

            self.remove(group)
            group = self.get_factor_group(num + x, h_line)
            self.add(group, rect)
            if x < 20:
                self.wait(0.5)
            else:
                self.wait(0.1)

            rect.set_fill(TEAL_E)
            stack.add(rect)
            self.add(stacks)

    def get_factor_group(self, num, h_line, font_size=36):
        # Test
        num_mob = Integer(num, font_size=font_size)
        num_mob.next_to(h_line, DOWN, MED_LARGE_BUFF).to_edge(LEFT, buff=0.25)
        rhs = self.get_rhs(num_mob)

        omega_n = len(sympy.factorint(num))
        omega_n_mob = Integer(omega_n, color=YELLOW)
        omega_n_mob.match_y(num_mob)
        omega_n_mob.to_edge(RIGHT, buff=1)

        arrow = Arrow(rhs, omega_n_mob, buff=0.5)
        group = VGroup(num_mob, rhs, arrow, omega_n_mob)

        return group

    def get_rhs(self, num_mob):
        if not isinstance(num_mob, Integer):
            return VGroup()

        kw = dict(font_size=num_mob.get_font_size())
        parts = [Tex("=", **kw)]
        for factor, exp in sympy.factorint(num_mob.get_value()).items():
            base = Integer(factor, **kw)
            underline = Underline(base, stretch_factor=1)
            underline.set_stroke(YELLOW, 2)
            underline.set_y(base[0].get_y(DOWN) - 0.05)
            base.add(underline)
            if exp == 1:
                parts.append(base)
            else:
                exp_mob = Integer(exp, **kw)
                exp_mob.scale(0.75)
                exp_mob.next_to(base.get_corner(UR), RIGHT, buff=0.05)
                parts.append(VGroup(*base, *exp_mob))
            parts.append(Tex(R"\times", **kw))
        result = VGroup(*parts[:-1])
        result.arrange(RIGHT, buff=SMALL_BUFF)
        result.next_to(num_mob, buff=SMALL_BUFF)
        target_y = num_mob[0].get_y()
        for part in result:
            part.shift((target_y - part[0].get_y()) * UP)

        self.add(result)

        return result
