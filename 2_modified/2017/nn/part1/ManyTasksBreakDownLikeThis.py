# ==============================================================================
# Scene:      ManyTasksBreakDownLikeThis
# Source:     videos/_2017/nn/part1.py (lines 2108-2195)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ManyTasksBreakDownLikeThis.py ManyTasksBreakDownLikeThis -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - `shift(MED_SMALL_BUFF, DOWN)` added a scalar to a vector (a typo in the original); the intent is a shift down by MED_SMALL_BUFF.
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


class ManyTasksBreakDownLikeThis(TeacherStudentsScene):
    def construct(self):
        audio = self.get_wave_form()
        audio_label = OldTexText("Raw audio")
        letters = OldTexText(" ".join("recognition"))
        syllables = OldTexText("$\\cdot$".join([
            "re", "cog", "ni", "tion"
        ]))
        word = OldTexText(
            "re", "cognition",
            arg_separator = ""
        )
        word[1].set_color(BLUE)
        arrows = VGroup()
        def get_arrow():
            arrow = Arrow(ORIGIN, RIGHT, color = BLUE)
            arrows.add(arrow)
            return arrow
        sequence = VGroup(
            audio, get_arrow(),
            letters, get_arrow(),
            syllables, get_arrow(),
            word
        )
        sequence.arrange(RIGHT)
        sequence.set_width(FRAME_WIDTH - 1)
        sequence.to_edge(UP)

        audio_label.next_to(audio, DOWN)
        VGroup(audio, audio_label).set_color(YELLOW)
        audio.save_state()

        self.teacher_says(
            "Many", "recognition", "tasks\\\\",
            "break down like this"
        )
        self.play_student_changes(*["pondering"]*3)
        self.wait()
        content = self.teacher.bubble.content
        pre_word = content[1]
        content.remove(pre_word)
        audio.move_to(pre_word)
        self.play(
            self.teacher.bubble.content.fade, 1,
            ShowCreation(audio),
            # CHANGE: `shift(MED_SMALL_BUFF, DOWN)` added a scalar to a vector (a typo in the original); the intent is a shift down by MED_SMALL_BUFF.
            pre_word.shift, MED_SMALL_BUFF*DOWN
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(self.teacher),
            audio.restore,
            FadeIn(audio_label),
            *[
                ReplacementTransform(
                    m1, m2
                )
                for m1, m2 in zip(pre_word, letters)
            ]
        )
        self.play(
            GrowFromPoint(arrows[0], arrows[0].get_start()),
        )
        self.wait()
        self.play(
            GrowFromPoint(arrows[1], arrows[1].get_start()),
            LaggedStartMap(FadeIn, syllables, run_time = 1)
        )
        self.wait()
        self.play(
            GrowFromPoint(arrows[2], arrows[2].get_start()),
            LaggedStartMap(FadeIn, word, run_time = 1)
        )
        self.wait()

    def get_wave_form(self):
        func = lambda x : abs(sum([
            (1./n)*np.sin((n+3)*x)
            for n in range(1, 5)
        ]))
        result = VGroup(*[
            Line(func(x)*DOWN, func(x)*UP)
            for x in np.arange(0, 4, 0.1)
        ])
        result.set_stroke(width = 2)
        result.arrange(RIGHT, buff = MED_SMALL_BUFF)
        result.set_height(1)

        return result
