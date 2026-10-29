# ==============================================================================
# Scene:      LuongQuote
# Source:     videos/_2026/2025_P6/p6.py (lines 4586-4596)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LuongQuote.py LuongQuote -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


class QuoteScene(InteractiveScene):
    quote_color = YELLOW
    settled_color = WHITE
    bg_color = "#111111"
    lag_ratio = 0.1
    wait_time = 0.15
    run_time_per_word = 0.25
    min_run_time = 1.0
    max_run_time = 3.0

    def get_quote_and_sections(self, raw_text):
        section_texts = raw_text.split("|")
        full_text = "".join(section_texts)

        quote = Text(full_text, alignment="left")
        aspect_ratio = FRAME_WIDTH / FRAME_HEIGHT
        if quote.get_width() / quote.get_height() > aspect_ratio:
            quote.set_width(FRAME_WIDTH * 0.8)
        else:
            quote.set_height(FRAME_HEIGHT * 0.8)
        quote.set_color(self.quote_color)

        sections = [quote[text] for text in section_texts]
        return quote, sections, section_texts

    def get_section_run_time(self, section_text):
        n_words = len(section_text.split())
        run_time = n_words * self.run_time_per_word
        return max(self.min_run_time, min(self.max_run_time, run_time))

    def play_quote(self, raw_text, run_times=None, wait_time=None):
        quote, sections, section_texts = self.get_quote_and_sections(raw_text)

        quote_bg = quote.copy().set_color(self.bg_color).set_opacity(0)
        self.add(quote_bg)

        if run_times is None:
            run_times = [self.get_section_run_time(t) for t in section_texts]
        if wait_time is None:
            wait_time = self.wait_time

        prev_section = None
        for section, run_time in zip(sections, run_times):
            anims = [FadeIn(section, lag_ratio=self.lag_ratio, run_time=run_time)]
            if prev_section is not None:
                anims.append(prev_section.animate.set_color(self.settled_color))
            self.play(*anims)
            self.wait(wait_time)
            prev_section = section

        self.play(prev_section.animate.set_color(self.settled_color))
        return quote


class LuongQuote(QuoteScene):
    def construct(self):
        # Show the quote
        raw_text = """
            ‘‘We didn’t really have a way to teach
            the model to be patient.| It didn’t take
            the time to understand the problem,|
            to get a feel for the problem,|
            to not try to solve the problem.”
            """
        self.play_quote(raw_text)
