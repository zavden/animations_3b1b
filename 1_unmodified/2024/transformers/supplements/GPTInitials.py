# ==============================================================================
# Scene:      GPTInitials
# Source:     videos/_2024/transformers/supplements.py (lines 9-123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GPTInitials.py GPTInitials -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GPTInitials(InteractiveScene):
    def construct(self):
        # Write name
        frame = self.frame
        name_str = "Generative Pre-trained Transformer"
        name = Text(name_str, font_size=72)
        name.to_edge(UP)
        name.save_state()
        frame.move_to(name).shift(DOWN)
        words = VGroup(name[word][0] for word in name_str.split(" "))
        initials = Text("GPT")
        initials.replace(name, dim_to_match=1)
        t_target = initials["T"][0].generate_target()
        t_target.shift(3 * RIGHT)

        words[0].next_to(initials["P"], LEFT, aligned_edge=DOWN)
        words[1].next_to(t_target, LEFT, aligned_edge=DOWN)

        morty = Mortimer(mode='plain').flip()
        morty.next_to(initials, DL).shift(0.5 * DOWN)
        morty.body.insert_n_curves(100)
        self.add(morty)

        def letter_anim(letters, point):
            for letter in letters:
                letter.save_state()
                letter.set_opacity(0)
                letter.move_to(point)
            return LaggedStart(
                (Restore(letter) for letter in letters),
                lag_ratio=0.05,
                time_span=(0.25, 0.75)
            )

        self.play(
            LaggedStartMap(FadeIn, initials, scale=2, lag_ratio=0.25, run_time=1),
            morty.change("raise_right_hand", initials),
        )
        self.play(Blink(morty))
        self.play(
            ReplacementTransform(initials[0], words[0][0]),
            letter_anim(words[0][1:], initials[0].get_center()),
            morty.animate.look_at(words[0]),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            words[0].animate.next_to(words[1], LEFT, aligned_edge=DOWN),
            Transform(initials[2], t_target),
            ReplacementTransform(initials[1], words[1][0]),
            letter_anim(words[1][1:], initials[1].get_center()),
            morty.change("well", words[1]),
            run_time=1
        )
        self.remove(initials)
        self.wait(0.5)
        self.play(
            Transform(name[:-len(words[2])], name.saved_state[:-len(words[2])]),
            ReplacementTransform(initials[2], words[2][0]),
            letter_anim(words[2][1:], initials[2].get_center()),
            morty.animate.look_at(words[2])
        )
        self.add(name)
        self.play(Blink(morty))
        self.wait()

        # Set up T structure
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(words, DOWN).set_x(0)
        v_lines = Line(UP, DOWN).set_height(FRAME_HEIGHT).replicate(2)
        v_lines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        v_lines.next_to(h_line, DOWN, buff=0)
        t_lines = VGroup(h_line, *v_lines)
        t_lines.set_stroke(GREY_B, 1)

        # Go through each word
        words.target = words.generate_target()
        words.target[0].set_fill(YELLOW)
        words.target[1:].set_fill(WHITE, 0.5, border_width=0)
        offset = FRAME_WIDTH / 3
        words.target[0].set_x(-offset)
        words.target[1].set_x(0)
        words.target[2].set_x(offset)
        line = Underline(words.target[0])
        line.set_stroke(YELLOW)
        self.play(LaggedStart(
            MoveToTarget(words),
            ShowCreation(line),
            frame.animate.center(),
            morty.change("thinking", words.target[0]).set_opacity(0),
            Write(t_lines, stroke_width=2),
            FlashAround(words.target[0].copy())
        ))
        self.remove(morty)
        self.wait()
        for i in [1, 2]:
            words.target = words.generate_target()
            words.target.set_fill(WHITE, 0.5, border_width=0)
            words.target[i].set_fill(YELLOW, 1, border_width=0.5)
            self.play(
                line.animate.become(Underline(words[i])).set_stroke(YELLOW).set_anim_args(run_time=0.75),
                FlashAround(words[i]),
                MoveToTarget(words),
            )
            self.wait()

        # Isolate just Transformer
        self.play(
            words[2].animate.set_x(0).set_color(WHITE).shift(0.25 * UP),
            line.animate.set_x(0).set_color(WHITE).set_width(6).shift(0.25 * UP),
            FadeOut(words[0], LEFT),
            FadeOut(words[1], 3 * LEFT),
            Uncreate(t_lines, lag_ratio=0),
        )
        self.wait()
