# ==============================================================================
# Scene:      IntroduceSHA256
# Source:     videos/_2017/crypto.py (lines 2461-2659)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceSHA256.py IntroduceSHA256 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
#   - memory: 32 Transforms between 256-glyph digests exceed the 5 GB cap (SIGKILL at animation 81); show 12 guesses instead of 32
# ==============================================================================

from manim_imports_ext import *
from hashlib import sha256

def sha256_bit_string(message):
    hexdigest = sha256(message.encode('utf-8')).hexdigest()
    return bin(int(hexdigest, 16))[2:]


def bit_string_to_mobject(bit_string):
    line = OldTex("0"*32)
    pre_result = VGroup(*[
        line.copy() for row in range(8)
    ])
    pre_result.arrange(DOWN, buff = SMALL_BUFF)
    result = VGroup(*it.chain(*pre_result))
    result.scale(0.7)
    bit_string = (256 - len(bit_string))*"0" + bit_string

    # CHANGE: assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
    parts = list(result)
    for i, (bit, part) in enumerate(zip(bit_string, parts)):
        if bit == "1":
            one = OldTex("1")[0]
            one.replace(part, dim_to_match = 1)
            parts[i] = one
    result.set_submobjects(parts)

    return result


def sha256_tex_mob(message, n_forced_start_zeros = 0):
    true_bit_string = sha256_bit_string(message)
    n = n_forced_start_zeros
    bit_string = "0"*n + true_bit_string[n:]
    return bit_string_to_mobject(bit_string)


class IntroduceSHA256(Scene):
    def construct(self):
        self.introduce_evaluation()
        self.inverse_function_question()
        self.issue_challenge()
        self.shift_everything_down()
        self.guess_and_check()

    def introduce_evaluation(self):
        messages = [
            "3Blue1Brown",
            "3Blue1Crown",
            "Mathologer",
            "Infinite Series",
            "Numberphile",
            "Welch Labs",
            "3Blue1Brown",
        ]
        groups = VGroup()
        for message in messages:
            lhs = OldTexText(
                "SHA256", "(``", message, "'') =",
                arg_separator = ""
            )
            lhs.set_color_by_tex(message, BLUE)
            digest = sha256_tex_mob(message)
            digest.next_to(lhs, RIGHT)
            group = VGroup(lhs, digest)
            group.to_corner(UP+RIGHT)
            group.shift(MED_LARGE_BUFF*DOWN)
            groups.add(group)

        group = groups[0]
        lhs, digest = group
        sha, lp, message, lp = lhs
        sha_brace = Brace(sha, UP)
        message_brace = Brace(message, DOWN)
        digest_brace = Brace(digest, DOWN)
        sha_text = sha_brace.get_text("", "Hash function")
        sha_text.set_color(YELLOW)
        message_text = message_brace.get_text("Message/file")
        message_text.set_color(BLUE)
        digest_text = digest_brace.get_text("``Hash'' or ``Digest''")
        brace_text_pairs = [
            (sha_brace, sha_text),
            (message_brace, message_text),
            (digest_brace, digest_text),
        ]

        looks_random = OldTexText("Looks random")
        looks_random.set_color(MAROON_B)
        looks_random.next_to(digest_text, DOWN)

        self.add(group)
        self.remove(digest)
        for brace, text in brace_text_pairs:
            if brace is digest_brace:
                self.play(LaggedStartMap(
                    FadeIn, digest,
                    run_time = 4,
                    lag_ratio = 0.05
                ))
                self.wait()
            self.play(
                GrowFromCenter(brace),
                Write(text, run_time = 2)
            )
            self.wait()
        self.play(Write(looks_random))
        self.wait(2)
        for mob in digest, message:
            self.play(LaggedStartMap(
                ApplyMethod, mob,
                lambda m : (m.set_color, YELLOW),
                rate_func = there_and_back,
                run_time = 1
            ))
        self.wait()
        self.play(FadeOut(looks_random))

        new_lhs, new_digest = groups[1]
        char = new_lhs[2][-5]
        arrow = Arrow(UP, ORIGIN, buff = 0)
        arrow.next_to(char, UP)
        arrow.set_color(RED)
        self.play(ShowCreation(arrow))
        for new_group in groups[1:]:
            new_lhs, new_digest = new_group
            new_message = new_lhs[2]
            self.play(
                Transform(lhs, new_lhs),
                message_brace.stretch_to_fit_width, new_message.get_width(),
                message_brace.next_to, new_message, DOWN,
                MaintainPositionRelativeTo(message_text, message_brace),
                MaintainPositionRelativeTo(sha_brace, lhs[0]),
                MaintainPositionRelativeTo(sha_text, sha_brace)
            )
            self.play(Transform(
                digest, new_digest,
                run_time = 2,
                lag_ratio = 0.5,
                path_arc = np.pi/2
            ))
            if arrow in self.get_mobjects():
                self.wait()
                self.play(FadeOut(arrow))
        self.wait()

        new_sha_text = OldTexText(
            "Cryptographic", "hash function"
        )
        new_sha_text.next_to(sha_brace, UP)
        new_sha_text.shift_onto_screen()
        new_sha_text.set_color(YELLOW)
        new_sha_text[0].set_color(GREEN)
        self.play(Transform(sha_text, new_sha_text))
        self.wait()

        self.lhs = lhs
        self.message = message
        self.digest = digest
        self.digest_text = digest_text
        self.message_text = message_text

    def inverse_function_question(self):
        arrow = Arrow(3*RIGHT, 3*LEFT, buff = 0)
        arrow.set_stroke(width = 8)
        arrow.set_color(RED)
        everything = VGroup(*self.get_mobjects())
        arrow.next_to(everything, DOWN)
        words = OldTexText("Inverse is infeasible")
        words.set_color(RED)
        words.next_to(arrow, DOWN)

        self.play(ShowCreation(arrow))
        self.play(Write(words))
        self.wait()

    def issue_challenge(self):
        desired_output_text = OldTexText("Desired output")
        desired_output_text.move_to(self.digest_text)
        desired_output_text.set_color(YELLOW)
        new_digest = sha256_tex_mob("Challenge")
        new_digest.replace(self.digest)
        q_marks = OldTexText("???")
        q_marks.move_to(self.message_text)
        q_marks.set_color(BLUE)

        self.play(
            Transform(
                self.digest, new_digest,
                run_time = 2,
                lag_ratio = 0.5,
                path_arc = np.pi/2
            ),
            Transform(self.digest_text, desired_output_text)
        )
        self.play(
            FadeOut(self.message),
            Transform(self.message_text, q_marks)
        )
        self.wait()

    def shift_everything_down(self):
        everything = VGroup(*self.get_top_level_mobjects())
        self.play(
            everything.scale, 0.85,
            everything.to_edge, DOWN
        )

    def guess_and_check(self):
        groups = VGroup()
        # CHANGE: memory: 32 Transforms between 256-glyph digests exceed the 5 GB cap (SIGKILL at animation 81); show 12 guesses instead of 32
        for x in range(12):
            message = "Guess \\#%d"%x
            lhs = OldTexText(
                "SHA256(``", message, "'') = ",
                arg_separator = ""
            )
            lhs.set_color_by_tex("Guess", BLUE)
            digest = sha256_tex_mob(message)
            digest.next_to(lhs, RIGHT)
            group = VGroup(lhs, digest)
            group.scale(0.85)
            group.next_to(self.digest, UP, aligned_edge = RIGHT)
            group.to_edge(UP)
            groups.add(group)

        group = groups[0]
        self.play(FadeIn(group))
        for new_group in groups[1:]:
            self.play(Transform(
                group[0], new_group[0],
                run_time = 0.5,
            ))
            self.play(Transform(
                group[1], new_group[1],
                run_time = 1,
                lag_ratio = 0.5
            ))
