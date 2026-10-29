# ==============================================================================
# Scene:      AmbientPermutations
# Source:     videos/_2022/galois/art_supplements.py (lines 4-32)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AmbientPermutations.py AmbientPermutations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AmbientPermutations(Scene):
    def construct(self):
        # Test
        text = Text("abcde", font_size=72)
        text.arrange_to_fit_width(4.5)
        self.add(text)

        # Animate swaps
        n_swaps = 10
        perms = list(it.permutations(range(len(text))))

        for x in range(n_swaps):
            perm = random.choice(perms)
            letter_anims = []
            arrow_anims = []
            for i, letter in enumerate(text):
                target = text[perm[i]]
                letter_anims.append(letter.animate.move_to(target, DOWN).set_anim_args(path_arc=90 * DEGREES))
                if i < perm[i]:
                    arrow = Arrow(letter.get_bottom(), target.get_bottom(), path_arc=90 * DEGREES)
                elif i > perm[i]:
                    arrow = Arrow(letter.get_top(), target.get_top(), path_arc=90 * DEGREES)
                else:
                    arrow = VMobject()
                arrow.set_stroke(BLUE)
                arrow_anims.append(ShowCreationThenFadeOut(arrow, run_time=2))

            self.play(LaggedStart(*arrow_anims, *letter_anims, lag_ratio=0.05))
            text.sort()
