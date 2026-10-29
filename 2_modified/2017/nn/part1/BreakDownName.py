# ==============================================================================
# Scene:      BreakDownName
# Source:     videos/_2017/nn/part1.py (lines 929-1034)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BreakDownName.py BreakDownName -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from manim_imports_ext import *
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class BreakDownName(Scene):
    def construct(self):
        self.ask_questions()
        self.show_neuron()

    def ask_questions(self):
        name = OldTexText("Neural", "network")
        name.to_edge(UP)
        q1 = OldTexText(
            "What are \\\\ the ", "neuron", "s?",
            arg_separator = ""
        )
        q2 = OldTexText("How are \\\\ they connected?")
        q1.next_to(name[0].get_bottom(), DOWN, buff = LARGE_BUFF)
        q2.next_to(name[1].get_bottom(), DOWN+RIGHT, buff = LARGE_BUFF)
        a1 = Arrow(q1.get_top(), name[0].get_bottom())
        a2 = Arrow(q2.get_top(), name.get_corner(DOWN+RIGHT))
        VGroup(q1, a1).set_color(BLUE)
        VGroup(q2, a2).set_color(YELLOW)

        randy = Randolph().to_corner(DOWN+LEFT)
        brain = SVGMobject(file_name = "brain")
        brain.set_fill(GREY_B, opacity = 0)
        brain.replace(randy.eyes, dim_to_match = 1)

        self.add(name)
        self.play(randy.change, "pondering")
        self.play(
            brain.set_height, 2,
            brain.shift, 2*UP,
            brain.set_fill, None, 1,
            randy.look, UP
        )
        brain_outline = brain.copy()
        brain_outline.set_fill(opacity = 0)
        brain_outline.set_stroke(BLUE_B, 3)
        self.play(
            ShowPassingFlash(
                brain_outline, 
                time_width = 0.5,
                run_time = 2
            )
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            Write(q1, run_time = 1),
            ShowCreation(a1),
            name[0].set_color, q1.get_color(),
        )
        self.play(
            Write(q2, run_time = 1),
            ShowCreation(a2),
            name[1].set_color, q2.get_color()
        )
        self.wait(2)

        self.play(*list(map(FadeOut, [
            name, randy, brain, 
            q2, a1, a2,
            q1[0], q1[2]
        ])))

        self.neuron_word = q1[1]

    def show_neuron(self):
        neuron_word = OldTexText("Neuron")
        arrow = OldTex("\\rightarrow")
        arrow.shift(LEFT)
        description = OldTexText("Thing that holds a number")
        neuron_word.set_color(BLUE)
        neuron_word.next_to(arrow, LEFT)
        neuron_word.shift(0.5*SMALL_BUFF*UP)
        description.next_to(arrow, RIGHT)

        neuron = Circle(radius = 0.35, color = BLUE)
        neuron.next_to(neuron_word, UP, MED_LARGE_BUFF)
        num = OldTex("0.2")
        num.set_width(0.7*neuron.get_width())
        num.move_to(neuron)
        num.save_state()
        num.move_to(description.get_right())
        num.set_fill(opacity = 1)

        self.play(
            ReplacementTransform(self.neuron_word, neuron_word),
            ShowCreation(neuron)
        )
        self.play(
            ShowCreation(arrow),
            Write(description, run_time = 1)
        )
        self.wait()
        self.play(
            neuron.set_fill, None, 0.2,
            num.restore
        )
        self.wait()
        for value in 0.8, 0.4, 0.1, 0.5:
            mob = OldTex(str(value))
            mob.replace(num)
            self.play(
                neuron.set_fill, None, value,
                Transform(num, mob)
            )
            self.wait()
