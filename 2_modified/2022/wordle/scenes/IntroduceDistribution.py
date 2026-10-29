# ==============================================================================
# Scene:      IntroduceDistribution
# Source:     videos/_2022/wordle/scenes.py (lines 1437-1764)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl IntroduceDistribution.py IntroduceDistribution -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - PATTERN_MATRIX_FILE points to _lib/data/wordle/pattern_matrix.npy (matrix precomputed in blocks; computing it inside the scene needs more than 5 GB)
#   - get_dynamic_bar_label: VGroup(*Tex(*tex)) -> VGroup(*OldTex(*tex)) (one part per string, as in 2022)
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


def safe_log2(x):
    return math.log2(x) if x > 0 else 0


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


def pattern_from_string(pattern_string):
    return sum((3**i) * int(c) for i, c in enumerate(pattern_string))


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


def get_word_buckets(guess, possible_words):
    buckets = [[] for x in range(3**5)]
    hashes = get_pattern_matrix([guess], possible_words).flatten()
    for index, word in zip(hashes, possible_words):
        buckets[index].append(word)
    return buckets


def get_weights(words, priors):
    frequencies = np.array([priors[word] for word in words])
    total = frequencies.sum()
    if total == 0:
        return np.zeros(frequencies.shape)
    return frequencies / total


def get_pattern_distributions(allowed_words, possible_words, weights):
    """
    For each possible guess in allowed_words, this finds the probability
    distribution across all of the 3^5 wordle patterns you could see, assuming
    the possible answers are in possible_words with associated probabilities
    in weights.

    It considers the pattern hash grid between the two lists of words, and uses
    that to bucket together words from possible_words which would produce
    the same pattern, adding together their corresponding probabilities.
    """
    pattern_matrix = get_pattern_matrix(allowed_words, possible_words)

    n = len(allowed_words)
    distributions = np.zeros((n, 3**5))
    n_range = np.arange(n)
    for j, prob in enumerate(weights):
        distributions[n_range, pattern_matrix[:, j]] += prob
    return distributions


def entropy_of_distributions(distributions, atol=1e-12):
    axis = len(distributions.shape) - 1
    return entropy(distributions, base=2, axis=axis)


def get_entropies(allowed_words, possible_words, weights):
    if weights.sum() == 0:
        return np.zeros(len(allowed_words))
    distributions = get_pattern_distributions(allowed_words, possible_words, weights)
    return entropy_of_distributions(distributions)



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


class WordleDistributions(WordleScene):
    grid_center = [-4.5, -0.5, 0]
    grid_height = 5
    bar_style = dict(
        fill_color=TEAL_D,
        fill_opacity=0.8,
        stroke_color=WHITE,
        stroke_width=0.1,
    )
    show_fraction_in_p_label = True

    def get_axes(self,
                 x_max=3**5 / 2, y_max=0.1,
                 width=7.5,
                 height=6):
        axes = Axes(
            (0, x_max),
            (0, y_max, y_max / 5),
            height=height,
            width=width,
            x_axis_config={
                "tick_size": 0,
            }
        )
        axes.next_to(self.grid, RIGHT, LARGE_BUFF, aligned_edge=DOWN)
        # y_label = OldTex("p(\\text{Pattern})", font_size=24)
        # y_label.next_to(axes.y_axis.get_top(), UR, buff=SMALL_BUFF)
        # axes.y_axis.add(y_label)
        axes.y_axis.add_numbers(num_decimal_places=2)

        x_label = Text("Pattern", font_size=24)
        x_label.next_to(axes.x_axis.get_right(), DR, MED_SMALL_BUFF)
        x_label.shift_onto_screen()
        axes.x_axis.add(x_label)

        self.axes = axes
        return axes

    def get_total_words_label(self, font_size=36):
        label = VGroup(
            Integer(len(self.all_words), font_size=font_size, edge_to_fix=UR),
            Text("Total words", font_size=font_size)
        )
        label.arrange(RIGHT, aligned_edge=UP)
        label.match_x(self.grid)
        label.to_edge(UP, buff=MED_SMALL_BUFF)
        return label

    def get_dynamic_match_label(self, font_size=36):
        label = VGroup(
            Integer(len(self.possibilities), font_size=font_size, edge_to_fix=UR),
            Text("Possible matches", font_size=font_size)
        )
        label.arrange(RIGHT, aligned_edge=DOWN)
        label.set_max_width(self.grid.get_width())
        label.next_to(self.grid, UP)

        def update_label(label):
            word = self.pending_word_as_string()
            if self.grid.pending_pattern is None or not self.is_valid_guess():
                label.set_opacity(0)
            else:
                buckets = get_word_buckets(word, self.possibilities)
                bucket_size = len(buckets[self.grid.pending_pattern])
                label[0].set_value(bucket_size)
                label[0].next_to(label[1], LEFT, submobject_to_align=label[0][-1])
                label.set_opacity(1)

        label.add_updater(update_label)

        return label

    def get_bars(self, axes, values):
        x_unit = axes.x_axis.unit_size
        y_unit = axes.y_axis.unit_size
        bars = Rectangle(width=x_unit, **self.bar_style).replicate(3**5)

        for x, bar, value in zip(it.count(), bars, values):
            bar.set_height(value * y_unit, stretch=True)
            bar.move_to(axes.c2p(x, 0), DL)
        return bars

    def get_distribution_bars(self, axes, guess):
        distribution = get_pattern_distributions(
            [guess], self.possibilities,
            get_weights(self.possibilities, self.priors)
        )[0]
        buckets = get_word_buckets(guess, self.possibilities)
        pattern_indices = np.argsort(distribution)[::-1]

        bars = self.get_bars(axes, distribution[pattern_indices])
        bars.patterns = pattern_indices

        for i, bar in enumerate(bars):
            bar.prob = distribution[pattern_indices[i]]
            bar.count = len(buckets[pattern_indices[i]])
        return bars

    def get_bar_indicator(self, bars, pattern_index):
        pattern_index_tracker = ValueTracker(pattern_index)

        def get_pattern_index():
            return int(pattern_index_tracker.get_value())

        def get_pattern():
            return bars.patterns[get_pattern_index()]

        tri = ArrowTip(angle=PI / 2)
        tri.set_height(0.1)
        tri.add_updater(lambda m: m.next_to(bars[get_pattern_index()], DOWN, buff=0))

        row = self.get_curr_row()
        row_copy = row.copy()
        row_copy.scale(0.25)
        row_copy.add_updater(lambda m: m.next_to(tri, DOWN, SMALL_BUFF))

        bars.add_updater(lambda m: m.set_opacity(0.35))
        bars.add_updater(lambda m: m[get_pattern_index()].set_opacity(1))
        self.grid.add_updater(lambda m: self.show_pattern(get_pattern()))
        self.add(self.grid)
        row_copy.add_updater(lambda m: m.match_style(row).set_stroke(width=0.1))

        self.mouse_drag_point.move_to(tri)
        pattern_index_tracker.add_updater(lambda m: m.set_value(
            clip(self.axes.x_axis.p2n(self.mouse_drag_point.get_center()), 0, 3**5)
        ))

        indicator = Group(tri, row_copy)

        def get_bar():
            value = pattern_index_tracker.get_value()
            index = int(clip(value, 0, 3**5 - 1))
            return bars[index]

        return indicator, pattern_index_tracker, get_bar

    def get_dynamic_bar_label(self, tex, font_size=36):
        row_copy = self.get_curr_row().copy()
        row_copy.scale(0.25)
        ndp = len(tex[-1].split(".")[1])
        dec = DecimalNumber(0, num_decimal_places=ndp, font_size=font_size)
        # CHANGE: Tex(*strs) no longer gives one part per string (it gives glyphs); OldTex does, and the code indexes by string
        result = VGroup(*OldTex(*tex, font_size=font_size))
        row_copy.replace(result[1], dim_to_match=0)
        dec.replace(result[-1])
        result.replace_submobject(1, row_copy)

        result.remove(result[-1])
        result.add(dec)

        result.add_updater(lambda m: m[1].match_style(self.get_curr_row()).set_stroke(WHITE, 0.1))
        return result

    def get_p_label(self, get_bar, max_y=1):
        poss_string = "{:,}".format(len(self.possibilities)).replace(",", "{,}")
        strs = ["p\\left(", "00000", "\\right)", "="]
        if self.show_fraction_in_p_label:
            strs.extend(["{" + poss_string, "\\over ", poss_string + "}", "=", ])
        strs.append("0.0000")
        p_label = self.get_dynamic_bar_label(strs)

        if self.show_fraction_in_p_label:
            num = Integer(edge_to_fix=DOWN, font_size=36)
            num.move_to(p_label[4], DOWN)
            p_label.replace_submobject(4, num)

        def update_label(label):
            label[4].set_value(int(get_bar().count))
            label[-1].set_value(get_bar().prob)
            label.next_to(get_bar(), UR, SMALL_BUFF)
            label.set_y(min(max_y, label.get_y()))
            label.shift_onto_screen(buff=1.0)

        p_label.add_updater(update_label)
        return p_label

    def get_information_label(self, p_label, get_bar):
        info_label = self.get_dynamic_bar_label(
            (
                "I\\left(", "00000", "\\right)", "=",
                "\\log_2\\left(1 / p)", "=",
                "0.00"
            ),
        )
        info_label.add_updater(lambda m: m[-1].set_value(-safe_log2(get_bar().prob)))
        info_label.add_updater(lambda m: m.next_to(p_label, UP, aligned_edge=LEFT))
        info_label.add_updater(lambda m: m.shift_onto_screen())
        return info_label

    def get_entropy_label(self, font_size=36):
        guess = self.pending_word_as_string()
        if self.is_valid_guess():
            entropy = get_entropies(
                [guess],
                self.possibilities,
                get_weights(self.possibilities, self.priors)
            )[0]
        else:
            entropy = 0

        lhs = OldTex(
            "E[I] = \\sum_x ",
            "p(x) \\cdot \\log_2(1 / p(x))", "=",
            tex_to_color_map={"I": BLUE},
            font_size=font_size,
        )
        value = DecimalNumber(entropy, font_size=font_size)
        value.next_to(lhs[-1], RIGHT)
        result = VGroup(lhs, value)
        result.move_to(self.axes, UR)
        result.to_edge(UP)

        return result

    def get_grid_of_matches(self, n_rows=20, n_cols=9):
        if self.grid.pending_pattern is not None:
            buckets = get_word_buckets(
                self.pending_word_as_string(),
                self.possibilities
            )
            words = buckets[self.grid.pending_pattern]
        else:
            words = self.possibilities
        word_mobs = self.get_grid_of_words(words, n_rows, n_cols)
        word_mobs.move_to(midpoint(self.grid.get_right(), RIGHT_SIDE))
        return word_mobs

    # Animations

    def add_distribution(self, axes):
        pass


class IntroduceDistribution(WordleDistributions):
    secret_word = "brown"
    uniform_prior = True
    n_word_rows = 20
    n_bars_to_analyze = 3

    def construct(self):
        # Total labels
        total_label = self.get_total_words_label()
        self.add(total_label)

        # Show an example guess
        guess = "weary"
        match_label = self.get_dynamic_match_label()
        word_grid = self.get_grid_of_matches(n_rows=self.n_word_rows)

        self.wait()
        self.wait()
        self.play(ShowIncreasingSubsets(word_grid, run_time=3))
        self.wait(note=f"Write {guess}, (but don't submit)")
        if not self.presenter_mode or self.skip_animations:
            self.add_word(guess)

        # Show several possible patterns, with corresponding matches
        pattern_strs = ["20100", "01000"]
        prob_label = VGroup()
        for i, pattern_str in enumerate(pattern_strs):
            pattern = pattern_from_string(pattern_str)
            self.remove(match_label)
            self.show_pattern(pattern, animate=True)
            self.play(FadeOut(word_grid), FadeOut(prob_label))
            word_grid = self.get_grid_of_matches(n_rows=self.n_word_rows)
            self.add(match_label)
            match_label.update()
            self.play(
                CountInFrom(match_label[0], 0),
                ShowIncreasingSubsets(word_grid, run_time=2)
            )
            self.wait(note=f"Pattern {i} / {len(pattern_strs)}")

            num = match_label[0].get_value()
            denom = total_label[0].get_value()
            prob_label = self.get_dynamic_bar_label((
                "p\\left(", "0000", "\\right)", "=",
                "{" + "{:,}".format(num).replace(",", "{,}"), "\\over ",
                "{:,}".format(denom).replace(",", "{,}") + "}", "=",
                "0.0000",
            ))
            prob_label[-1].set_value(num / denom)
            prob_label.next_to(word_grid, UP)
            prob_label.clear_updaters()
            self.play(
                LaggedStart(
                    FadeTransform(match_label[0].copy().clear_updaters(), prob_label[4], remover=True),
                    FadeTransform(total_label[0].copy().clear_updaters(), prob_label[6], remover=True),
                    lag_ratio=0.5,
                ),
                FadeIn(VGroup(*prob_label[:4], prob_label[5], prob_label[7:])),
            )
            self.add(prob_label)
            self.wait()

        # Show distribution
        axes = self.get_axes(y_max=0.15)
        bars = self.get_distribution_bars(axes, guess)

        self.play(
            FadeOut(word_grid),
            FadeOut(prob_label),
        )
        self.play(LaggedStart(
            Write(axes),
            ShowIncreasingSubsets(bars),
            lag_ratio=0.5
        ))
        self.add(bars)
        self.wait()

        index = 20
        bar_indicator, x_tracker, get_bar = self.get_bar_indicator(bars, index)
        p_label = self.get_p_label(get_bar)

        self.add(bar_indicator, x_tracker)
        self.add(p_label)
        self.add(match_label)
        for x in range(self.n_bars_to_analyze):
            self.wait(note=f"Play around with probability {x} / {self.n_bars_to_analyze}")
            word_grid = self.get_grid_of_matches(n_rows=12, n_cols=5)
            word_grid.next_to(p_label, UP, LARGE_BUFF)
            self.play(ShowIncreasingSubsets(word_grid))
            self.wait()
            self.remove(word_grid)

        # Describe aim for expected information
        want = Text("What we want:")
        standin = OldTex(
            "E[\\text{Information}] = \\sum_{x} p(x) \\cdot (\\text{Something})",
            tex_to_color_map={
                "\\text{Something}": GREY_B,
                "\\text{Information}": BLUE,
            },
            font_size=36,
        )
        group = VGroup(want, standin)
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        group.to_corner(UR)

        self.play(FadeIn(want))
        self.play(Write(standin))
        self.wait(note="Discuss adding up over all patterns")

        # Define information
        info_label = self.get_information_label(p_label, get_bar)
        il_copy = info_label.copy().clear_updaters()
        self.play(FadeIn(il_copy, UP, remover=True))
        self.add(info_label)
        self.wait(note="Give intuitions on values of I")

        # Define entropy
        entropy_definition = self.get_entropy_label()
        brace = Brace(entropy_definition, DOWN, buff=SMALL_BUFF)
        ent_label = OldTexText("Entropy, $H$")
        ent_label.set_color(BLUE)
        ent_label.next_to(brace, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(entropy_definition, UP),
            FadeOut(standin, UP),
            FadeOut(want, UP),
        )
        self.wait(note="Drag tracker through full distributinon")
        self.wait()
        self.play(x_tracker.animate.set_value(10), run_time=3)
        self.play(
            GrowFromCenter(brace),
            Write(ent_label)
        )
        self.wait()

        # Show an alternate word
        self.remove(bar_indicator, x_tracker, p_label, info_label, bars, match_label)
        entropy_definition[-1].set_opacity(0)
        self.grid.clear_updaters()
        self.grid.add_updater(lambda m: m)
        self.get_curr_row().set_fill(BLACK, 0)
        self.grid.pending_pattern = None
        self.wait(note="Delete word, write \"saner\", but don't enter!")

        if not self.presenter_mode or self.skip_animations:
            for x in range(5):
                self.delete_letter()
            self.add_word('saner')

        guess = self.pending_word_as_string()
        bars = self.get_distribution_bars(axes, guess)

        self.play(ShowIncreasingSubsets(bars, run_time=3))
        self.wait()

        trackers = self.add_trackers(bars, index=20)
        self.wait(note="Play around more with distribiution")

        self.recalculate_entropy(entropy_definition, guess, trackers[0])
        self.wait()

        # Examples of good entropy
        self.remove(*trackers)
        bars.set_opacity(0.7)
        self.grid.clear_updaters()
        self.grid.add_updater(lambda m: m)
        self.grid.pending_word.set_submobjects([])
        self.add_word("?????")
        self.get_curr_row().set_fill(BLACK, 0)

        eqs = VGroup(
            OldTex("E[I] = \\log_2\\left({1 \\over 1 / 3^5}\\right) = \\log_2(3^5) \\approx 7.92"),
            OldTex("E[I] = \\log_2\\left({1 \\over 1 / 16}\\right) = \\log_2(16) = 4.00"),
            OldTex("E[I] = \\log_2\\left({1 \\over 1 / 64}\\right) = \\log_2(64) = 6.00"),
        )
        eqs.scale(0.7)
        for eq in eqs:
            eq.next_to(ent_label, DOWN, LARGE_BUFF)

        prev_values = [bar.prob for bar in bars]

        last_eq = VGroup()
        ent_rhs = entropy_definition[-1]
        for eq, x in zip(eqs, [3**5, 16, 64]):
            values = [1 / x] * x + [0] * (3**5 - x)
            self.set_bars_to_values(bars, values, ent_rhs, added_anims=[FadeOut(last_eq)])
            self.wait()
            self.play(FadeIn(eq, UP))
            last_eq = eq
            self.wait()

        self.grid.pending_word.set_submobjects([])
        self.add_word(guess, wait_time_per_letter=0)
        self.set_bars_to_values(bars, prev_values, ent_rhs, added_anims=[FadeOut(last_eq)])
        self.wait()

        # Show the second guess
        true_pattern = self.get_pattern(guess)
        self.show_pattern(true_pattern, animate=True)
        trackers[0].set_value(list(bars.patterns).index(true_pattern))
        match_label.update()
        self.play(FadeIn(match_label))
        self.wait()

        self.play(
            ApplyMethod(
                match_label[0].copy().move_to,
                total_label[0], UR,
                remover=True,
            ),
            FadeOut(total_label[0], UP)
        )
        total_label[0].set_value(match_label[0].get_value())
        self.add(total_label)
        self.wait()

        faders = [axes, bars, match_label]
        for fader in faders:
            fader.clear_updaters()
        self.play(
            LaggedStart(*map(FadeOut, faders)),
            FadeOut(entropy_definition[-1]),
        )
        self.grid.clear_updaters()
        self.reveal_pattern(animate=False)
        next_guess = "wordy"
        self.wait(note=f"Type in \"{next_guess}\"")
        if not self.presenter_mode or self.skip_animations:
            self.add_word(next_guess)

        # Show new distribution
        guess = self.pending_word_as_string()
        axes = self.get_axes(y_max=1, x_max=50)
        bars = self.get_distribution_bars(axes, guess)
        self.play(
            FadeIn(axes),
            FadeIn(bars, lag_ratio=0.1, run_time=2)
        )
        self.wait()

        self.remove(match_label)
        trackers = self.add_trackers(bars)
        self.wait(note="Play around with distribution")
        trackers[0].clear_updaters()
        self.play(trackers[0].animate.set_value(10), run_time=3)
        self.play(trackers[0].animate.set_value(0), run_time=5)

        self.recalculate_entropy(entropy_definition, guess)

        # Other second guesses
        self.grid.clear_updaters()
        self.get_curr_row().set_fill(BLACK, 0)
        self.pending_pattern = None
        entropy_definition[1].set_opacity(0)
        self.remove(bars, *trackers)
        if not self.presenter_mode or self.skip_animations:
            words = get_word_list()
            for guess in random.sample(words, 15):
                for x in range(5):
                    self.delete_letter()
                self.add_word(guess, wait_time_per_letter=0)
                bars = self.get_distribution_bars(axes, guess)
                self.add(bars)
                self.play(FadeIn(bars, lag_ratio=0.1, run_time=2))
                self.recalculate_entropy(entropy_definition, guess)
                self.wait()
                self.remove(bars)
        else:
            guess = "print"
            self.wait(note=f"Write \"{guess}\"")
            trackers = self.add_trackers(bars)
            self.wait(note="Play around with distribution")

    def set_bars_to_values(self, bars, values, ent_rhs, run_time=3, added_anims=[]):
        y_unit = self.axes.y_axis.unit_size
        bars.generate_target()
        bar_template = bars[0].copy()
        entropy = entropy_of_distributions(np.array(values))
        for bar, value in zip(bars.target, values):
            target = bar_template.copy()
            target.set_height(
                y_unit * value,
                stretch=True,
                about_edge=DOWN
            )
            target.move_to(bar, DOWN)
            bar.become(target)

        self.play(
            MoveToTarget(bars, run_time=run_time),
            ChangeDecimalToValue(ent_rhs, entropy, run_time=run_time),
            *added_anims
        )

    def recalculate_entropy(self, entropy_definition, guess, x_tracker=None):
        dec = entropy_definition[-1]
        dec.set_value(
            get_entropies(
                [guess], self.possibilities,
                get_weights(self.possibilities, self.priors)
            )[0]
        )
        dec.set_opacity(1)
        dec.next_to(entropy_definition[-2][-1])
        anims = [CountInFrom(dec, 0)]
        run_time = 1
        if x_tracker is not None:
            x_tracker.suspend_updating()
            anims.append(UpdateFromAlphaFunc(
                x_tracker, lambda m, a: m.set_value(a * 200),
                run_time=5,
            ))
            run_time = 3
        self.play(*anims, run_time=run_time)
        self.wait()

    def add_trackers(self, bars, index=1):
        bar_indicator, x_tracker, get_bar = self.get_bar_indicator(bars, index)
        p_label = self.get_p_label(get_bar, max_y=1)
        info_label = self.get_information_label(p_label, get_bar)
        match_label = self.get_dynamic_match_label()
        trackers = [x_tracker, bar_indicator, p_label, info_label, match_label]
        self.add(*trackers)
        return trackers
