# ==============================================================================
# Scene:      ChoosingBasedOnLetterFrequencies
# Source:     videos/_2022/wordle/scenes.py (lines 1306-1379)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl ChoosingBasedOnLetterFrequencies.py ChoosingBasedOnLetterFrequencies -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - PATTERN_MATRIX_FILE points to _lib/data/wordle/pattern_matrix.npy (matrix precomputed in blocks; computing it inside the scene needs more than 5 GB)
#   - animate_color_change: minimum height 1e-6 -> 1e-2 (the points are float32: with 1e-6 the letters of the row were deformed when restored)
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/wordle/pattern_matrix.npy (precomputed pattern matrix; generator 2022/wordle/make_wordle_data.py)
#   - _lib/assets/generated/2022/wordle/data/{possible_words.txt,allowed_words.txt,freq_map.json} (free lists: ENABLE + SCOWL and wordfreq frequencies, instead of Wordle/NYT's; generator 2022/wordle/make_wordle_wordlists.py)
# ==============================================================================

from manim_imports_ext import *
from scipy.stats import entropy


# ----- From _2022/wordle/simulations.py -----

MISPLACED = np.uint8(1)


EXACT = np.uint8(2)


DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)


SHORT_WORD_LIST_FILE = os.path.join(DATA_DIR, "possible_words.txt")


LONG_WORD_LIST_FILE = os.path.join(DATA_DIR, "allowed_words.txt")


WORD_FREQ_FILE = os.path.join(DATA_DIR, "wordle_words_freqs_full.txt")


WORD_FREQ_MAP_FILE = os.path.join(DATA_DIR, "freq_map.json")


# CHANGE: the pattern matrix (168 MB) lives in _lib/data/wordle (make_wordle_data.py generates it);
# CHANGE: in the original it is computed on first use, with more than 5 GB of memory
PATTERN_MATRIX_FILE = os.path.join(get_directories()["data"], "wordle", "pattern_matrix.npy")


# To store the large grid of patterns at run time
PATTERN_GRID_DATA = dict()


CHUNK_LENGTH = 13000


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_word_list(short=False):
    result = []
    file = SHORT_WORD_LIST_FILE if short else LONG_WORD_LIST_FILE
    with open(file) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result


def get_word_frequencies(regenerate=False):
    if os.path.exists(WORD_FREQ_MAP_FILE) or regenerate:
        with open(WORD_FREQ_MAP_FILE) as fp:
            result = json.load(fp)
        return result
    # Otherwise, regenerate
    freq_map = dict()
    with open(WORD_FREQ_FILE) as fp:
        for line in fp.readlines():
            pieces = line.split(' ')
            word = pieces[0]
            freqs = [
                float(piece.strip())
                for piece in pieces[1:]
            ]
            freq_map[word] = np.mean(freqs[-5:])
    with open(WORD_FREQ_MAP_FILE, 'w') as fp:
        json.dump(freq_map, fp)
    return freq_map


def get_frequency_based_priors(n_common=3000, width_under_sigmoid=10):
    """
    We know that that list of wordle answers was curated by some human
    based on whether they're sufficiently common. This function aims
    to associate each word with the likelihood that it would actually
    be selected for the final answer.

    Sort the words by frequency, then apply a sigmoid along it.
    """
    freq_map = get_word_frequencies()
    words = np.array(list(freq_map.keys()))
    freqs = np.array([freq_map[w] for w in words])
    arg_sort = freqs.argsort()
    sorted_words = words[arg_sort]

    # We want to imagine taking this sorted list, and putting it on a number
    # line so that it's length is 10, situating it so that the n_common most common
    # words are positive, then applying a sigmoid
    x_width = width_under_sigmoid
    c = x_width * (-0.5 + n_common / len(words))
    xs = np.linspace(c - x_width / 2, c + x_width / 2, len(words))
    priors = dict()
    for word, x in zip(sorted_words, xs):
        priors[word] = sigmoid(x)
    return priors


def get_true_wordle_prior():
    words = get_word_list()
    short_words = get_word_list(short=True)
    return dict(
        (w, int(w in short_words))
        for w in words
    )


def words_to_int_arrays(words):
    return np.array([[ord(c)for c in w] for w in words], dtype=np.uint8)


def generate_pattern_matrix(words1, words2):
    """
    A pattern for two words represents the wordle-similarity
    pattern (grey -> 0, yellow -> 1, green -> 2) but as an integer
    between 0 and 3^5. Reading this integer in ternary gives the
    associated pattern.

    This function computes the pairwise patterns between two lists
    of words, returning the result as a grid of hash values. Since
    this can be time-consuming, many operations that can be are vectorized
    (perhaps at the expense of easier readibility), and the the result
    is saved to file so that this only needs to be evaluated once, and
    all remaining pattern matching is a lookup.
    """

    # Number of letters/words
    nl = len(words1[0])
    nw1 = len(words1)  # Number of words
    nw2 = len(words2)  # Number of words

    # Convert word lists to integer arrays
    word_arr1, word_arr2 = map(words_to_int_arrays, (words1, words2))

    # equality_grid keeps track of all equalities between all pairs
    # of letters in words. Specifically, equality_grid[a, b, i, j]
    # is true when words[i][a] == words[b][j]
    equality_grid = np.zeros((nw1, nw2, nl, nl), dtype=bool)
    for i, j in it.product(range(nl), range(nl)):
        equality_grid[:, :, i, j] = np.equal.outer(word_arr1[:, i], word_arr2[:, j])

    # full_pattern_matrix[a, b] should represent the 5-color pattern
    # for guess a and answer b, with 0 -> grey, 1 -> yellow, 2 -> green
    full_pattern_matrix = np.zeros((nw1, nw2, nl), dtype=np.uint8)

    # Green pass
    for i in range(nl):
        matches = equality_grid[:, :, i, i].flatten()  # matches[a, b] is true when words[a][i] = words[b][i]
        full_pattern_matrix[:, :, i].flat[matches] = EXACT

        for k in range(nl):
            # If it's a match, mark all elements associated with
            # that letter, both from the guess and answer, as covered.
            # That way, it won't trigger the yellow pass.
            equality_grid[:, :, k, i].flat[matches] = False
            equality_grid[:, :, i, k].flat[matches] = False

    # Yellow pass
    for i, j in it.product(range(nl), range(nl)):
        matches = equality_grid[:, :, i, j].flatten()
        full_pattern_matrix[:, :, i].flat[matches] = MISPLACED
        for k in range(nl):
            # Similar to above, we want to mark this letter
            # as taken care of, both for answer and guess
            equality_grid[:, :, k, j].flat[matches] = False
            equality_grid[:, :, i, k].flat[matches] = False

    # Rather than representing a color pattern as a lists of integers,
    # store it as a single integer, whose ternary representations corresponds
    # to that list of integers.
    pattern_matrix = np.dot(
        full_pattern_matrix,
        (3**np.arange(nl)).astype(np.uint8)
    )

    return pattern_matrix


def generate_pattern_matrix_in_blocks(many_words1, many_words2, block_length=CHUNK_LENGTH):
    block_matrix = None
    for words1 in chunks(many_words1, block_length):
        row = None

        for words2 in chunks(many_words2, block_length):
            block = generate_pattern_matrix(words1, words2)

            if row is None:
                row = block
            else:
                row = np.hstack((row, block))

        if block_matrix is None:
            block_matrix = row
        else:
            block_matrix = np.vstack((block_matrix, row))

    return block_matrix


def generate_full_pattern_matrix():
    words = get_word_list()
    pattern_matrix = generate_pattern_matrix_in_blocks(words, words)
    # Save to file
    np.save(PATTERN_MATRIX_FILE, pattern_matrix)
    return pattern_matrix


def get_pattern_matrix(words1, words2):
    if not PATTERN_GRID_DATA:
        if not os.path.exists(PATTERN_MATRIX_FILE):
            log.info("\n".join([
                "Generating pattern matrix. This takes a minute, but",
                "the result will be saved to file so that it only",
                "needs to be computed once.",
            ]))
            generate_full_pattern_matrix()
        PATTERN_GRID_DATA['grid'] = np.load(PATTERN_MATRIX_FILE)
        PATTERN_GRID_DATA['words_to_index'] = dict(zip(
            get_word_list(), it.count()
        ))

    full_grid = PATTERN_GRID_DATA['grid']
    words_to_index = PATTERN_GRID_DATA['words_to_index']

    indices1 = [words_to_index[w] for w in words1]
    indices2 = [words_to_index[w] for w in words2]
    return full_grid[np.ix_(indices1, indices2)]


def get_pattern(guess, answer):
    if PATTERN_GRID_DATA:
        saved_words = PATTERN_GRID_DATA['words_to_index']
        if guess in saved_words and answer in saved_words:
            return get_pattern_matrix([guess], [answer])[0, 0]
    return generate_pattern_matrix([guess], [answer])[0, 0]


def pattern_to_int_list(pattern):
    result = []
    curr = pattern
    for x in range(5):
        result.append(curr % 3)
        curr = curr // 3
    return result


def get_possible_words(guess, pattern, word_list):
    all_patterns = get_pattern_matrix([guess], word_list).flatten()
    return list(np.array(word_list)[all_patterns == pattern])


def get_weights(words, priors):
    frequencies = np.array([priors[word] for word in words])
    total = frequencies.sum()
    if total == 0:
        return np.zeros(frequencies.shape)
    return frequencies / total


def entropy_of_distributions(distributions, atol=1e-12):
    axis = len(distributions.shape) - 1
    return entropy(distributions, base=2, axis=axis)



# ----- From _2022/wordle/scenes.py -----

class WordleScene(Scene):
    n_letters = 5
    grid_height = 6
    font_to_square_height = 65
    grid_center = ORIGIN
    secret_word = None
    color_map = {
        0: "#797C7E",  # GREY
        1: "#C6B566",  # YELLOW
        2: GREEN_D,  # GREEN
    }
    uniform_prior = False
    wordle_based_prior = False
    freq_prior = True
    reveal_run_time = 2
    reveal_lag_ratio = 0.5

    CONFIG = {"random_seed": None}

    def setup(self):
        self.all_words = self.get_word_list()
        self.priors = self.get_priors()
        if self.secret_word is None:
            s_words = get_word_list(short=True)
            self.secret_word = random.choice(s_words)
        self.guesses = []
        self.patterns = []
        self.possibilities = self.get_initial_possibilities()

        self.add_grid()

    def get_word_list(self):
        return get_word_list()

    def get_initial_possibilities(self):
        return get_word_list()

    def get_priors(self):
        words = self.all_words
        if self.uniform_prior:
            return dict((w, 1) for w in words)
        elif self.wordle_based_prior:
            return get_true_wordle_prior()
        else:
            return get_frequency_based_priors()

    def get_pattern(self, guess):
        return get_pattern(guess, self.secret_word)

    def get_current_entropy(self):
        weights = get_weights(self.possibilities, self.priors)
        return entropy_of_distributions(weights)

    ##

    def add_grid(self):
        buff = 0.1
        row = Square(side_length=1).get_grid(1, self.n_letters, buff=buff)
        grid = row.get_grid(6, 1, buff=buff)
        grid.set_height(self.grid_height)
        grid.move_to(self.grid_center)
        grid.set_stroke(WHITE, 2)
        grid.words = VGroup()
        grid.pending_word = VGroup()
        grid.add(grid.words, grid.pending_word)
        grid.pending_pattern = None
        grid.add_updater(lambda m: m)
        self.grid = grid
        self.add(grid)

    def get_curr_row(self):
        return self.grid[len(self.grid.words)]

    def get_curr_square(self):
        row = self.get_curr_row()
        return row[len(self.grid.pending_word)]

    def add_letter(self, letter):
        grid = self.grid
        if len(grid.pending_word) == len(grid[0]):
            return

        letter_mob = self.get_letter_in_square(letter, self.get_curr_square())
        grid.pending_word.add(letter_mob)

    def get_letter_in_square(self, letter, square):
        font_size = self.font_to_square_height * square.get_height()
        letter_mob = Text(letter.upper(), font="Consolas", font_size=font_size)
        letter_mob.move_to(square)
        return letter_mob

    def delete_letter(self):
        if len(self.grid.pending_word) == 0:
            return
        letter_mob = self.grid.pending_word[-1]
        self.grid.pending_word.remove(letter_mob)

    def add_word(self, word, wait_time_per_letter=0.1):
        for letter in word:
            self.add_letter(letter)
            self.wait(
                wait_time_per_letter,
                ignore_presenter_mode=True
            )

    def pending_word_as_string(self):
        return "".join(
            t.text.lower()
            for t in self.grid.pending_word
        )

    def is_valid_guess(self):
        guess = self.pending_word_as_string()
        return guess in self.all_words

    def reveal_pattern(self, pattern=None, animate=True):
        grid = self.grid
        guess = self.pending_word_as_string()

        if not self.is_valid_guess():
            self.shake_word_out()
            return False

        if pattern is None:
            pattern = self.get_pattern(guess)
            if pattern is None:
                return False

        self.show_pattern(pattern, animate=animate)

        self.guesses.append(guess)
        self.patterns.append(pattern)
        grid.words.add(grid.pending_word.copy())
        grid.pending_word.set_submobjects([])
        grid.pending_pattern = None
        self.refresh_possibilities(guess, pattern)

        # Win condition
        if self.has_won():
            self.win_animation()

        return True

    def refresh_possibilities(self, guess, pattern):
        self.possibilities = get_possible_words(
            guess, pattern, self.possibilities
        )

    def shake_word_out(self):
        row = self.get_curr_row()
        c = row.get_center().copy()
        func = bezier([0, 0, 1, 1, -1, -1, 0, 0])
        self.play(UpdateFromAlphaFunc(
            VGroup(row, self.grid.pending_word),
            lambda m, a: m.move_to(c + func(a) * RIGHT),
            run_time=0.5,
        ))
        self.grid.pending_word.set_submobjects([])

    def show_pattern(self, pattern, animate=False, added_anims=[]):
        row = self.get_curr_row()
        colors = self.get_colors(pattern)
        if animate:
            self.animate_color_change(row, self.grid.pending_word, colors, added_anims)
        else:
            self.set_row_colors(row, colors)

        self.grid.pending_pattern = pattern

    def set_row_colors(self, row, colors):
        for square, color in zip(row, colors):
            square.set_fill(color, 1)

    def animate_color_change(self, row, word, colors, added_anims=[]):
        colors.extend((len(row) - len(colors)) * [self.color_map[0]])
        for square, color in zip(row, colors):
            square.future_color = color

        def alpha_func(mob, alpha):
            if not hasattr(mob, 'initial_height'):
                mob.initial_height = mob.get_height()
            # CHANGE: with 1e-6 the points (float32) collapse and the letters come out deformed when they return to their height; 1e-2 is used
            mob.set_height(
                mob.initial_height * max(abs(interpolate(1, -1, alpha)), 1e-2),
                stretch=True
            )
            if isinstance(mob, Square) and alpha > 0.5:
                mob.set_fill(mob.future_color, 1)

        mobjects = self.mobjects
        self.play(
            *(
                LaggedStart(
                    *(
                        UpdateFromAlphaFunc(sm, alpha_func)
                        for sm in mob
                    ),
                    lag_ratio=self.reveal_lag_ratio,
                    run_time=self.reveal_run_time,
                )
                for mob in (row, word)
            ),
            *added_anims
        )
        self.clear()
        self.add(*mobjects)

    def get_colors(self, pattern):
        return [self.color_map[key] for key in pattern_to_int_list(pattern)]

    def win_animation(self):
        grid = self.grid
        row = grid[len(grid.words) - 1]
        letters = grid.words[-1]
        mover = VGroup(*(
            VGroup(square, letter)
            for square, letter in zip(row, letters)
        ))
        y = row.get_y()
        bf = bezier([0, 0, 1, 1, -1, -1, 0, 0])

        self.play(
            LaggedStart(*(
                UpdateFromAlphaFunc(sm, lambda m, a: m.set_y(y + 0.2 * bf(a)))
                for sm in mover
            ), lag_ratio=0.1, run_time=1.5),
            LaggedStart(*(
                Flash(letter, line_length=0.1, flash_radius=0.4)
                for letter in letters
            ), lag_ratio=0.3, run_time=1.5),
        )

    def has_won(self):
        return len(self.patterns) > 0 and self.patterns[-1] == 3**5 - 1

    @staticmethod
    def get_grid_of_words(all_words, n_rows, n_cols, dots_index=-5, sort_key=None, font_size=24):
        if sort_key:
            all_words = list(sorted(all_words, key=sort_key))
        subset = all_words[:n_rows * n_cols]
        show_ellipsis = len(subset) < len(all_words)

        if show_ellipsis:
            subset[dots_index] = "..." if n_cols == 1 else "....."
            subset[dots_index + 1:] = all_words[dots_index + 1:]

        full_string = ""
        for i, word in zip(it.count(1), subset):
            full_string += str(word)
            if i % n_cols == 0:
                full_string += " \n"
            else:
                full_string += "  "

        full_text_mob = Text(full_string, font="Consolas", font_size=font_size)

        result = VGroup()
        for word in subset:
            part = full_text_mob.get_part_by_text(word)
            part.text = word
            result.add(part)

        if show_ellipsis and n_cols == 1:
            result[dots_index].rotate(PI / 2)
            result[dots_index].next_to(result[dots_index - 1], DOWN, SMALL_BUFF)
            result[dots_index + 1:].next_to(result[dots_index], DOWN, SMALL_BUFF)
        result.set_color(GREY_A)
        result.words = subset

        return result

    @staticmethod
    def patterns_to_squares(patterns, color_map=None):
        if color_map is None:
            color_map = WordleScene.color_map
        row = Square().get_grid(1, 5, buff=SMALL_BUFF)
        rows = row.get_grid(len(patterns), 1, buff=SMALL_BUFF)
        rows.set_stroke(WHITE, 1)
        for pattern, row in zip(patterns, rows):
            for square, key in zip(row, pattern_to_int_list(pattern)):
                square.set_fill(color_map[key], 1)
        return rows

    # Interactive parts
    def on_key_press(self, symbol, modifiers):
        try:
            char = chr(symbol)
        except OverflowError:
            log.warning("The value of the pressed key is too large.")
            return

        is_letter = (ord('a') <= ord(char) <= ord('z'))

        if is_letter:
            self.add_letter(char)
        elif symbol == 65288:  # Delete
            self.delete_letter()
        elif symbol == 65293:  # Enter
            self.reveal_pattern()

        if char == 'q' and modifiers == 1:
            self.delete_letter()
            self.quit_interaction = True

        if not is_letter:
            super().on_key_press(symbol, modifiers)


class IntroduceGame(WordleScene):
    secret_word = "brown"
    grid_center = 3.5 * LEFT

    def construct(self):
        # Secret
        grid = self.grid
        row_copy = self.get_curr_row().copy()
        secret = VGroup(
            Text("Secret word"),
            Vector(0.5 * DOWN),
            row_copy,
        )
        secret[2].match_width(secret[0])
        secret.arrange(DOWN, buff=MED_SMALL_BUFF)
        secret.next_to(grid, RIGHT, buff=2.0, aligned_edge=UP)

        word_list = random.sample(get_word_list(short=True), 100)
        word_list.append("?????")
        words = VGroup(*(Text(word, font="Consolas") for word in word_list))
        words.set_height(row_copy.get_height() * 0.7)
        words[-1].set_color(RED)

        for word in words:
            for char, square in zip(word, row_copy):
                char.move_to(square)

        self.wait()
        self.wait()
        self.play(
            Write(secret[0]),
            ShowCreation(secret[1]),
            TransformFromCopy(grid[0], secret[2])
        )
        self.play(
            ShowSubmobjectsOneByOne(words, run_time=10, rate_func=linear),
        )
        self.wait()

        self.row_copy = row_copy
        self.q_marks = words[-1]

        # Guesses
        numbers = VGroup(*(Integer(i) for i in range(1, 7)))
        for number, row in zip(numbers, grid):
            number.next_to(row, LEFT)

        self.play(FadeIn(numbers, lag_ratio=0.1))

        guesses = ["three", "blues", "one", "onnne", "wonky", "brown"]
        if not self.presenter_mode:
            for guess in guesses:
                self.add_word(guess)
                self.reveal_pattern()
        else:
            self.wait(note=f"Type {guesses}")

        # Show word lists
        all_words = get_word_list()
        answers = get_word_list(short=True)

        titles = VGroup(
            VGroup(Text("Allowed guesses"), Integer(len(all_words))),
            VGroup(Text("Possible answers"), Integer(len(answers))),
        )
        for title in titles:
            title.arrange(DOWN)

        titles.scale(0.8)
        titles.arrange(RIGHT, buff=1.5, aligned_edge=UP)
        titles[1][1].match_y(titles[0][1])
        titles.to_corner(UR)
        titles.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        word_columns = VGroup(
            self.get_grid_of_words(all_words, 20, 5),
            self.get_grid_of_words(answers, 20, 1),
        )
        word_columns[1].set_color(GREEN)
        for column, title in zip(word_columns, titles):
            column.next_to(title, DOWN, MED_LARGE_BUFF)

        grid.add(numbers)
        self.play(
            FadeOut(secret),
            FadeOut(self.q_marks),
            grid.animate.scale(0.7, about_edge=LEFT),
            Write(titles[0][0], run_time=1),
        )
        self.play(
            CountInFrom(titles[0][1], 0),
            ShowIncreasingSubsets(word_columns[0]),
        )
        self.wait()
        self.play(
            FadeIn(titles[1][0]),
            CountInFrom(titles[1][1], 0),
            ShowIncreasingSubsets(word_columns[1]),
        )
        self.wait()

        # Try not to use wordle_words
        frame = self.camera.frame
        answer_rect = SurroundingRectangle(VGroup(titles[1], word_columns[1]))
        answer_rect.set_stroke(TEAL, 3)
        avoid = OldTexText("Let's try to avoid\\\\using this")
        avoid.next_to(answer_rect, RIGHT)
        morty = Mortimer(height=2)
        morty.next_to(avoid, DOWN, MED_LARGE_BUFF)
        morty.change("hesitant", answer_rect)
        morty.save_state()
        morty.change("plain").set_opacity(0)

        self.play(
            frame.animate.match_x(word_columns, LEFT).shift(LEFT),
            ShowCreation(answer_rect),
            run_time=2,
        )
        self.play(
            Write(avoid),
            Restore(morty),
        )
        self.wait()

        # Common but not in wordle list
        priors = get_frequency_based_priors()
        not_in_answers = set(all_words).difference(answers)
        sorted_by_freq = list(sorted(not_in_answers, key=lambda w: priors[w]))
        n = 15
        most_common = self.get_grid_of_words(sorted_by_freq[-n:], n, 1)
        most_common.set_color(BLUE)
        most_common.move_to(morty.get_corner(UR), DOWN).shift(MED_SMALL_BUFF * UP)

        non_s_most_common = self.get_grid_of_words(
            list(filter(lambda w: w[-1] != 's', sorted_by_freq))[-n:], n, 1
        )
        non_s_most_common.match_style(most_common)
        non_s_most_common.replace(most_common)

        label = Text("Not in wordle list", font_size=36)
        label.next_to(most_common, UP)

        self.play(
            FadeOut(avoid, DOWN),
            morty.change("raise_LEFT_hand", most_common),
            ShowIncreasingSubsets(most_common),
        )
        self.play(FadeIn(label))
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("pondering", most_common),
            LaggedStartMap(FadeOut, most_common, shift=RIGHT),
            LaggedStartMap(FadeIn, non_s_most_common, shift=RIGHT),
        )
        self.wait()

    def show_pattern(self, *args, **kwargs):
        guess = self.pending_word_as_string()
        letters = self.grid.pending_word.copy()
        for letter, q_mark in zip(letters, self.q_marks):
            letter.replace(q_mark, dim_to_match=1)

        added_anims = []
        if guess == self.secret_word:
            added_anims.append(LaggedStart(
                *(
                    square.animate.set_fill(GREEN, 1)
                    for square in self.row_copy
                ),
                lag_ratio=0.7,
                run_time=2
            ))
            added_anims.append(LaggedStart(
                *(
                    Transform(q_mark, letter)
                    for q_mark, letter in zip(self.q_marks, letters)
                ),
                lag_ratio=0.7,
                run_time=2
            ))
        super().show_pattern(*args, added_anims=added_anims, **kwargs)


class ChoosingBasedOnLetterFrequencies(IntroduceGame):
    def construct(self):
        # Reconfigure grid to be flat
        grid = self.grid
        grid.set_submobjects([VGroup(*it.chain(*grid))])
        grid.add(grid.pending_word)
        self.add(grid)

        # Data on right
        letters_and_frequencies = [
            ("E", 13),
            ("T", 9.1),
            ("A", 8.2),
            ("O", 7.5),
            ("I", 7),
            ("N", 6.7),
            ("S", 6.3),
            ("H", 6.1),
            ("R", 6),
            ("D", 4.3),
            ("L", 4),
            ("U", 2.8),
            ("C", 2.8),
            ("M", 2.5),
            ("W", 2.4),
            ("F", 2.2),
            ("G", 2.0),
            ("Y", 2.0),
        ]
        freq_data = VGroup(*(
            VGroup(
                Text(letter, font="Consolas"),
                Rectangle(
                    height=0.25, width=0.2 * freq,
                    stroke_width=0,
                    fill_color=(BLUE if letter in "AEIOUY" else GREY_B),
                    fill_opacity=1,
                ),
                DecimalNumber(freq, num_decimal_places=1, font_size=24, unit="\\%")
            ).arrange(RIGHT)
            for letter, freq in letters_and_frequencies
        ))
        freq_data.arrange(DOWN, aligned_edge=LEFT)
        freq_data.set_height(FRAME_HEIGHT - 1)
        freq_data.to_edge(RIGHT, buff=LARGE_BUFF)
        self.freq_data = freq_data
        for row, lf in zip(freq_data, letters_and_frequencies):
            letter = lf[0]
            row.letter = letter
            row.rect = SurroundingRectangle(row, buff=SMALL_BUFF)
            row.rect.set_stroke(YELLOW, 0)
            row.add(row.rect)
        freq_data.add_updater(lambda m: m)
        self.add(freq_data)

    def add_letter(self, letter):
        super().add_letter(letter)
        self.update_freq_data_highlights()

    def delete_letter(self):
        super().delete_letter()
        self.update_freq_data_highlights()

    def update_freq_data_highlights(self):
        word = self.pending_word_as_string()
        for row in self.freq_data:
            if row.letter.lower() in word.lower():
                row.set_opacity(1)
                row.rect.set_fill(opacity=0)
                row.rect.set_stroke(width=2)
            else:
                row.set_opacity(0.5)
                row.rect.set_fill(opacity=0)
                row.rect.set_stroke(width=0)
