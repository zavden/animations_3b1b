# ==============================================================================
# Scene:      AltOpeningQuote
# Source:     videos/_2018/cramer.py (lines 77-111)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltOpeningQuote.py AltOpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AltOpeningQuote(OpeningQuote):
    def construct(self):
        kw = {
            "tex_to_color_map": {
                "Jerry": YELLOW,
                "Kramer": BLUE,
            },
            "arg_separator": "",
            "alignment": "",
        }
        parts = VGroup(
            OldTexText("Jerry: Ah, you're crazy!", **kw),
            OldTexText(
                "Kramer:",
                "{} Am I? Or am I so sane that\\\\",
                "you just blew your mind?",
                **kw
            ),
            OldTexText("Jerry: It's impossible!", **kw),
            OldTexText(
                "Kramer:", "{} Is it?! Or is it so possible\\\\",
                "your head is spinning like a top?",
                **kw
            )
        )
        for part in parts[1::2]:
            part[-1].align_to(part[-2], LEFT)

        parts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        self.add(parts[0])
        self.play(FadeIn(parts[1], lag_ratio=0.1, run_time=2))
        self.play(FadeIn(parts[2], lag_ratio=0))
        self.play(FadeIn(parts[3], lag_ratio=0.1, run_time=2))
        self.wait()
