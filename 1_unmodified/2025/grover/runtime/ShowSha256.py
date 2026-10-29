# ==============================================================================
# Scene:      ShowSha256
# Source:     videos/_2025/grover/runtime.py (lines 1018-1050)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSha256.py ShowSha256 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSha256(InteractiveScene):
    def construct(self):
        # Test
        import hashlib

        input_int = Integer(0, min_total_width=8, group_with_commas=False)
        output_text = Text("")
        lhs = VGroup(Text(R"SHA256("), input_int, Text(")"))
        lhs.arrange(RIGHT, buff=SMALL_BUFF),
        equation = VGroup(lhs, Tex("=").rotate(90 * DEG), output_text)
        equation.arrange(DOWN, buff=MED_SMALL_BUFF)

        def update_hash(text_mob):
            input_bytes = str(input_int.get_value()).encode()
            sha256_hash = hashlib.new('sha256')
            sha256_hash.update(input_bytes)
            hash_hex = sha256_hash.hexdigest()

            new_text = "\n".join(
                "".join(row)
                for row in np.array(list(hash_hex)).reshape((4, 16))
            )

            new_text = Text(new_text, font="Consolas")
            new_text.move_to(text_mob, UP)
            text_mob.set_submobjects(new_text.submobjects)

        output_text.add_updater(update_hash)

        self.add(equation)
        self.play(
            ChangeDecimalToValue(input_int, 2400, rate_func=linear, run_time=24)
        )
