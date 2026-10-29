# ==============================================================================
# Scene:      DotProductWithGenderDirection
# Source:     videos/_2024/transformers/embedding.py (lines 2067-2078)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl DotProductWithGenderDirection.py DotProductWithGenderDirection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
# ==============================================================================

from __future__ import annotations
import gensim
from pathlib import Path
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")



# ----- From _2024/transformers/embedding.py -----

def get_word_to_vec_model(model_name="glove-wiki-gigaword-50"):
    filename = str(Path(DATA_DIR, model_name))
    if os.path.exists(filename):
        return gensim.models.keyedvectors.KeyedVectors.load(filename)
    model = gensim.downloader.load(model_name)
    model.save(filename)
    return model


class DotProductWithPluralDirection(InteractiveScene):
    vec_tex = R"\vec{\text{plur}}"
    ref_words = ["cat", "cats"]
    word_groups = [
        ["puppy", "puppies"],
        ["octopus", "octopi", "octopuses", "octopodes"],
        ["student", "students"],
        ["one", "two", "three", "four"],
    ]
    x_range = (-4, 4 + 1e-4, 0.25)
    colors = [BLUE, RED]
    threshold = -1.0

    def construct(self):
        # Initialize equation
        self.model = get_word_to_vec_model()
        word_groups = self.word_groups
        words = list(it.chain(*word_groups))

        # Write plurality equation
        gen_lhs = self.get_equation_lhs(words[0])[0].copy()
        equals = Tex(":=")
        rf1, rf2 = self.ref_words
        rhs = Tex(
            Rf"E(\text{{{rf2}}}) - E(\text{{{rf1}}})",
            tex_to_color_map={
                Rf"\text{{{ref_word}}}": color
                for ref_word, color in zip(self.ref_words, self.colors)
            }
        )
        top_eq = VGroup(gen_lhs, equals, rhs)
        top_eq.arrange(RIGHT)
        gen_lhs.align_to(rhs, DOWN)
        top_eq.center().to_edge(UP, buff=0.5)

        self.play(FadeIn(rhs, UP))
        self.play(LaggedStart(
            FadeIn(equals, 0.5 * LEFT),
            FadeIn(gen_lhs, 1.0 * LEFT),
        ))
        self.wait()

        # Show on number line
        x_range = self.x_range
        number_line = NumberLine(
            x_range,
            big_tick_numbers=list(np.arange(*x_range[:2])),
            tick_size=0.05,
            longer_tick_multiple=3.0,
            width=12
        )
        number_line.rotate(PI / 2)
        number_line.add_numbers(
            np.arange(*x_range[:2]),
            num_decimal_places=1,
            font_size=40,
            direction=LEFT,
        )
        number_line.numbers.shift(SMALL_BUFF * LEFT)
        number_line.set_max_height(FRAME_HEIGHT - 1)
        number_line.to_edge(LEFT, buff=1.0)

        eq_lhs = self.get_equation_lhs(words[0])
        eq_rhs = self.get_equation_rhs(eq_lhs, words[0])
        equation = VGroup(eq_lhs, eq_rhs)
        brace = Brace(eq_lhs[2], LEFT, buff=0.1)
        brace.next_to(equation, LEFT, SMALL_BUFF, DOWN)
        equation_group = VGroup(brace, equation)
        dp = eq_rhs.get_value()

        word = eq_lhs[2][2:-1]
        lil_word = word.copy().scale(0.25)
        dot = GlowDot(color=word[0].get_color())
        dot.move_to(number_line.n2p(dp))

        lil_word.next_to(dot, RIGHT, buff=0)
        equation_group.next_to(dot, RIGHT, buff=0, submobject_to_align=brace)

        self.play(
            top_eq.animate.scale(0.75).to_corner(UR),
            TransformFromCopy(gen_lhs, eq_lhs[0]),
            FadeIn(eq_lhs[1:], shift=DOWN),
            FadeIn(brace, shift=DOWN),
            UpdateFromAlphaFunc(
                eq_rhs,
                lambda m, a: m.set_value(a * dp).next_to(eq_lhs[-1], RIGHT),
                run_time=1,
            ),
            Write(number_line, run_time=1)
        )
        self.add_dot(word, dot)
        self.wait()

        # Show some alternate
        new_rhs = eq_rhs.copy()
        eq_rhs.set_opacity(0)
        new_rhs.f_always.set_value(lambda: number_line.p2n(brace.get_center()))
        new_rhs.always.next_to(eq_lhs[-1], RIGHT)
        self.add(new_rhs)

        to_fade = Group(dot)
        for word_group in self.word_groups:
            for new_word in word_group:
                new_dp = self.get_dot_with_key_word(new_word)
                nl_point = number_line.n2p(new_dp)
                color = self.colors[int(new_dp > self.threshold)]
                new_dot = GlowDot(number_line.n2p(new_dp), color=color)
                new_lhs = self.get_equation_lhs(new_word)
                new_rhs = self.get_equation_rhs(new_lhs, new_word)
                new_rhs.set_opacity(0)
                new_equation = VGroup(new_lhs, new_rhs)
                new_equation.move_to(equation, LEFT)
                new_brace = brace.copy()
                new_equation_group = VGroup(new_brace, new_equation)
                y_shift = new_dot.get_y() - brace.get_y()
                new_equation_group.shift(y_shift * UP)

                if new_word == word_group[0]:
                    added_anim = FadeOut(to_fade)
                    to_fade = Group()
                else:
                    ghost = equation_group.copy()
                    ghost.target = ghost.generate_target()
                    ghost.target.set_fill(opacity=0.75)
                    ghost.target.scale(0.5, about_point=ghost[0].get_left())
                    added_anim = MoveToTarget(ghost)
                    to_fade.add(ghost)
                self.play(
                    Transform(equation_group, new_equation_group),
                    added_anim,
                )
                self.add_dot(new_lhs[2][2:-1], new_dot)
                to_fade.add(new_dot)

    def add_dot(self, word, dot):
        self.play(
            FadeInFromPoint(dot, word.get_center()),
            LaggedStart(
                (FadeTransform(char.copy(), dot.copy().set_opacity(0))
                for char in word),
                lag_ratio=2e-2,
                group_type=Group
            ),
            run_time=1
        )

    def get_equation_lhs(self, word):
        tex_pieces = [
            self.vec_tex, R"\cdot", Rf"E(\text{{{word}}})", "="
        ]
        expression = Tex(
            " ".join(tex_pieces),
            tex_to_color_map={self.vec_tex: YELLOW}
        )
        parts = [
            expression[tex_piece][0]
            for tex_piece in tex_pieces
        ]
        gen_part = parts[0]
        gen_part[0].set_width(0.75 * gen_part.get_width(), about_edge=DOWN)
        gen_part[0].shift(SMALL_BUFF * DOWN)
        value = self.get_dot_with_key_word(word)
        parts[2][2:-1].set_color(self.colors[int(value > self.threshold)])
        return VGroup(*parts)

    def get_equation_rhs(self, equation_lhs, word):
        rhs = DecimalNumber(self.get_dot_with_key_word(word))
        rhs.next_to(equation_lhs[-1], RIGHT)
        return rhs

    def get_dot_with_key_word(self, word):
        if word == "octopodes":
            return 2.3  # Hack
        elif word == "four":
            return 1.80  # To make the spacing nicer
        rf1, rf2 = self.ref_words
        return np.dot(
            (self.model[rf2] - self.model[rf1]).flatten(),
            self.model[word].flatten(),
        )


class DotProductWithGenderDirection(DotProductWithPluralDirection):
    vec_tex = R"\vec{\text{gen}}"
    ref_words = ["man", "woman"]
    words = [
        "mother", "father",
        "aunt", "uncle",
        "sister", "brother",
        "mama", "papa",
    ]
    x_range = (-5, 7 + 1e-4, 0.25)
    colors = [BLUE, RED]
    threshold = 1.0
