# ==============================================================================
# Scene:      RankingUpdates
# Source:     videos/_2022/wordle/footnote.py (lines 654-786)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl RankingUpdates.py RankingUpdates -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/wordle/best_entropies.json (regenerated; generator 2022/wordle/make_wordle_data.py)
#   - _lib/data/wordle/best_double_entropies.json (regenerated; generator 2022/wordle/make_wordle_data.py)
#   - _lib/data/wordle/best_scores_with_entropy_method.json (regenerated; generator 2022/wordle/make_wordle_data.py)
#   - _lib/assets/generated/2022/wordle/data/{possible_words.txt,allowed_words.txt,freq_map.json} (free lists: ENABLE + SCOWL and wordfreq frequencies, instead of Wordle/NYT's; generator 2022/wordle/make_wordle_wordlists.py)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/wordle/simulations.py -----

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)


SHORT_WORD_LIST_FILE = os.path.join(DATA_DIR, "possible_words.txt")


LONG_WORD_LIST_FILE = os.path.join(DATA_DIR, "allowed_words.txt")


def get_word_list(short=False):
    result = []
    file = SHORT_WORD_LIST_FILE if short else LONG_WORD_LIST_FILE
    with open(file) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result



# ----- From _2022/wordle/footnote.py -----

class RankingUpdates(Scene):
    def construct(self):
        # Titles
        kw = dict(tex_to_color_map={"$E[I]$": TEAL}, font_size=30)
        titles = VGroup(
            OldTexText("Highest $E[I]$\\\\(one step)", **kw),
            OldTexText("Highest $E[I]$\\\\(two steps)", **kw),
            OldTexText("Lowest average\\\\scores", **kw),
        )
        for x, title in zip(range(-1, 2), titles):
            title.set_x(x * FRAME_WIDTH / 3)
            title.to_edge(UP, buff=MED_SMALL_BUFF)
        titles.to_edge(UP)

        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY_B, 1)
        h_line.next_to(titles, DOWN)
        h_line.set_x(0)

        v_lines = VGroup(*(
            Line(UP, DOWN).set_height(FRAME_HEIGHT).set_x(x * FRAME_WIDTH / 6)
            for x in (-1, 1)
        ))
        v_lines.match_style(h_line)

        self.add(h_line)
        self.add(v_lines)

        # Lists
        n_shown = 15

        def get_column(rows, title, row_height=0.2, buff=0.2):
            for row in rows:
                row.move_to(ORIGIN, LEFT)
            rows.set_height(row_height)
            for i, row in enumerate(rows):
                row.shift(i * (row_height + buff) * DOWN)
            rows.next_to(h_line, DOWN)

            numbers = VGroup()
            for i, row in zip(it.count(1), rows):
                num = Integer(i, unit=".")
                num.match_height(row)
                num.next_to(row, LEFT)
                numbers.add(num)

            result = VGroup(numbers, rows)
            result.match_x(title)
            result.rows = rows
            result.numbers = numbers
            return result

        # One step
        with open(os.path.join(get_directories()["data"], "wordle", "best_entropies.json")) as fp:
            rows1 = VGroup()
            for word, ent in json.load(fp)[:n_shown]:
                row = VGroup(
                    Text(word, font="Consolas"),
                    OldTex("\\rightarrow"),
                    DecimalNumber(ent, color=TEAL),
                )
                row.arrange(RIGHT)
                rows1.add(row)

        # Two step
        with open(os.path.join(get_directories()["data"], "wordle", "best_double_entropies.json")) as fp:
            rows2 = VGroup()
            for word, ent1, ent2 in json.load(fp)[:n_shown]:
                row = VGroup(
                    Text(word, font="Consolas"),
                    OldTex("\\rightarrow"),
                    DecimalNumber(ent1, color=TEAL),
                    OldTex("+"),
                    DecimalNumber(ent2, color=TEAL),
                    OldTex("="),
                    DecimalNumber(ent1 + ent2, color=TEAL),
                )
                row.arrange(RIGHT)
                rows2.add(row)

        # Score
        answers = get_word_list(short=True)
        with open(os.path.join(get_directories()["data"], "wordle", "best_scores_with_entropy_method.json")) as fp:
            rows3 = VGroup()
            for word, score, dist in json.load(fp)[:n_shown]:
                row = VGroup(
                    Text(word, font="Consolas"),
                    OldTex("\\rightarrow"),
                    DecimalNumber(score / len(answers), num_decimal_places=3, color=BLUE),
                )
                row.arrange(RIGHT)
                rows3.add(row)

        all_rows = [rows1, rows2, rows3]
        col1, col2, col3 = cols = [
            get_column(rows, title)
            for rows, title in zip(all_rows, titles)
        ]
        for row in col2.rows:
            row[-2:].align_to(col2.rows[0][-2:], LEFT)

        # Animations
        self.add(titles[0])
        self.play(FadeIn(col1, lag_ratio=0.1, run_time=2))
        self.wait()

        last_col = col1
        for title, col in zip(titles[1:], cols[1:]):
            pre_words = VGroup(*(r[0] for r in last_col.rows))
            words = VGroup(*(r[0] for r in col.rows))
            mover_anims = []
            fade_anims = []
            for word in words:
                has_pre = False
                for pre_word in pre_words:
                    if word.text == pre_word.text:
                        has_pre = True
                        mover_anims.append(TransformFromCopy(pre_word, word))
                if not has_pre:
                    fade_anims.append(FadeInFromPoint(word, last_col.get_bottom()))

            for row in col.rows:
                fade_anims.append(FadeIn(row[1:]))

            self.play(
                FadeIn(title),
                FadeIn(col.numbers, lag_ratio=0.1),
                LaggedStart(*mover_anims, run_time=2, lag_ratio=0.2),
            )
            self.play(LaggedStart(*fade_anims))
            self.add(col)
            self.wait()
            last_col = col
