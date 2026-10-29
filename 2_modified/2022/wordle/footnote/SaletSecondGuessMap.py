# ==============================================================================
# Scene:      SaletSecondGuessMap
# Source:     videos/_2022/wordle/footnote.py (lines 588-651)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/scenes.py, _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl SaletSecondGuessMap.py SaletSecondGuessMap -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - PATTERN_MATRIX_FILE points to _lib/data/wordle/pattern_matrix.npy (matrix precomputed in blocks; computing it inside the scene needs more than 5 GB)
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/wordle/pattern_matrix.npy (precomputed pattern matrix; generator 2022/wordle/make_wordle_data.py)
#   - _lib/assets/generated/2022/wordle/data/{possible_words.txt,allowed_words.txt,freq_map.json} (free lists: ENABLE + SCOWL and wordfreq frequencies, instead of Wordle/NYT's; generator 2022/wordle/make_wordle_wordlists.py)
# ==============================================================================

from manim_imports_ext import *
from tqdm import tqdm as ProgressDisplay
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


def get_bucket_sizes(allowed_words, possible_words):
    """
    Returns a (len(allowed_words), 243) shape array reprenting the size of
    word buckets associated with each guess in allowed_words
    """
    weights = np.ones(len(possible_words))
    return get_pattern_distributions(allowed_words, possible_words, weights)


def get_bucket_counts(allowed_words, possible_words):
    """
    Returns the number of separate buckets that each guess in allowed_words
    would separate possible_words into
    """
    bucket_sizes = get_bucket_sizes(allowed_words, possible_words)
    return (bucket_sizes > 0).sum(1)


def entropy_to_expected_score(ent):
    """
    Based on a regression associating entropies with typical scores
    from that point forward in simulated games, this function returns
    what the expected number of guesses required will be in a game where
    there's a given amount of entropy in the remaining possibilities.
    """
    # Assuming you can definitely get it in the next guess,
    # this is the expected score
    min_score = 2**(-ent) + 2 * (1 - 2**(-ent))

    # To account for the likely uncertainty after the next guess,
    # and knowing that entropy of 11.5 bits seems to have average
    # score of 3.5, we add a line to account
    # we add a line which connects (0, 0) to (3.5, 11.5)
    return min_score + 1.5 * ent / 11.5


def get_expected_scores(allowed_words, possible_words, priors,
                        look_two_ahead=False,
                        n_top_candidates_for_two_step=25,
                        ):
    # Currenty entropy of distribution
    weights = get_weights(possible_words, priors)
    H0 = entropy_of_distributions(weights)
    H1s = get_entropies(allowed_words, possible_words, weights)

    word_to_weight = dict(zip(possible_words, weights))
    probs = np.array([word_to_weight.get(w, 0) for w in allowed_words])
    # If this guess is the true answer, score is 1. Otherwise, it's 1 plus
    # the expected number of guesses it will take after getting the corresponding
    # amount of information.
    expected_scores = probs + (1 - probs) * (1 + entropy_to_expected_score(H0 - H1s))

    if not look_two_ahead:
        return expected_scores

    # For the top candidates, refine the score by looking two steps out
    # This is currently quite slow, and could be optimized to be faster.
    # But why?
    sorted_indices = np.argsort(expected_scores)
    allowed_second_guesses = get_word_list()
    expected_scores += 1  # Push up the rest
    for i in ProgressDisplay(sorted_indices[:n_top_candidates_for_two_step], leave=False):
        guess = allowed_words[i]
        H1 = H1s[i]
        dist = get_pattern_distributions([guess], possible_words, weights)[0]
        buckets = get_word_buckets(guess, possible_words)
        second_guesses = [
            optimal_guess(allowed_second_guesses, bucket, priors, look_two_ahead=False)
            for bucket in buckets
        ]
        H2s = [
            get_entropies([guess2], bucket, get_weights(bucket, priors))[0]
            for guess2, bucket in zip(second_guesses, buckets)
        ]

        prob = word_to_weight.get(guess, 0)
        expected_scores[i] = sum((
            # 1 times Probability guess1 is correct
            1 * prob,
            # 2 times probability guess2 is correct
            2 * (1 - prob) * sum(
                p * word_to_weight.get(g2, 0)
                for p, g2 in zip(dist, second_guesses)
            ),
            # 2 plus expected score two steps from now
            (1 - prob) * (2 + sum(
                p * (1 - word_to_weight.get(g2, 0)) * entropy_to_expected_score(H0 - H1 - H2)
                for p, g2, H2 in zip(dist, second_guesses, H2s)
            ))
        ))
    return expected_scores


def get_score_lower_bounds(allowed_words, possible_words):
    """
    Assuming a uniform distribution on how likely each element
    of possible_words is, this gives the a lower boudn on the
    possible score for each word in allowed_words
    """
    bucket_counts = get_bucket_counts(allowed_words, possible_words)
    N = len(possible_words)
    # Probabilities of getting it in 1
    p1s = np.array([w in possible_words for w in allowed_words]) / N
    # Probabilities of getting it in 2
    p2s = bucket_counts / N - p1s
    # Otherwise, assume it's gotten in 3 (which is optimistics)
    p3s = 1 - bucket_counts / N
    return p1s + 2 * p2s + 3 * p3s


def optimal_guess(allowed_words, possible_words, priors,
                  look_two_ahead=False,
                  optimize_for_uniform_distribution=False,
                  purely_maximize_information=False,
                  ):
    if purely_maximize_information:
        if len(possible_words) == 1:
            return possible_words[0]
        weights = get_weights(possible_words, priors)
        ents = get_entropies(allowed_words, possible_words, weights)
        return allowed_words[np.argmax(ents)]

    # Just experimenting here...
    if optimize_for_uniform_distribution:
        expected_scores = get_score_lower_bounds(
            allowed_words, possible_words
        )
    else:
        expected_scores = get_expected_scores(
            allowed_words, possible_words, priors,
            look_two_ahead=look_two_ahead
        )
    return allowed_words[np.argmin(expected_scores)]



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
            mob.set_height(
                mob.initial_height * max(abs(interpolate(1, -1, alpha)), 1e-6),
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


class HowLookTwoAheadWorks(Scene):
    prob_color = BLUE_D
    entropy_color = TEAL
    first_guess = "tares"
    n_shown_trials = 240
    transition_time = 1

    def get_priors(self):
        return get_frequency_based_priors()

    def construct(self):
        # Setup
        all_words = get_word_list()
        possibilities = get_word_list()
        priors = self.get_priors()

        # Show first guess
        guess1 = self.get_word_mob(self.first_guess)
        guess1.to_edge(LEFT)
        pattern_array1 = self.get_pattern_array(guess1, possibilities, priors)
        prob_bars1 = self.get_prob_bars(pattern_array1.pattern_mobs)

        self.add(guess1)
        self.play(
            ShowCreation(
                pattern_array1.connecting_lines,
                lag_ratio=0.1
            ),
            LaggedStartMap(
                FadeIn, pattern_array1.pattern_mobs,
                shift=0.2 * RIGHT,
                lag_ratio=0.1,
            ),
            run_time=2,
        )
        self.play(Write(pattern_array1.dot_parts))
        self.wait()
        for bar in prob_bars1:
            bar.save_state()
            bar.stretch(0, 0, about_edge=LEFT)
            bar.set_opacity(0)
        self.play(LaggedStartMap(Restore, prob_bars1))
        self.wait()

        # Reminder on entropy
        H_eq = OldTex(
            "E[I] = \\sum_{x} p(x) \\cdot \\log_2\\big((1 / p(x)\\big)",
            font_size=36
        )
        H_eq.next_to(prob_bars1, RIGHT)

        info_labels = VGroup(*(
            self.get_info_label(bar)
            for bar in prob_bars1
        ))

        self.play(Write(H_eq))
        self.wait()
        self.play(FadeIn(info_labels[0], lag_ratio=0.1))
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, info_labels[1:], lag_ratio=0.5),
            H_eq.animate.scale(0.7).to_edge(DOWN),
            run_time=2,
        )
        self.wait()

        H_label = self.get_entropy_label(guess1, pattern_array1.distribution)
        self.play(FadeTransform(H_eq, H_label))
        self.wait()
        self.play(LaggedStartMap(FadeOut, info_labels), run_time=1)

        # Show example second guess
        word_buckets = get_word_buckets(guess1.text, possibilities)

        arrows = VGroup()
        second_guesses = VGroup()
        second_ents = VGroup()
        for i, bar in enumerate(prob_bars1):
            pattern = pattern_array1.pattern_mobs[i].pattern
            bucket = word_buckets[pattern]
            optimal_word = optimal_guess(all_words, bucket, priors)
            shown_words = random.sample(all_words, self.n_shown_trials)
            shown_words.append(optimal_word)
            for j, shown_word in enumerate(shown_words):
                guess2 = self.get_word_mob(shown_word)
                guess2.set_width(0.7)
                guess2.match_y(bar)
                guess2.set_x(0, LEFT)
                arrow = Arrow(bar.label, guess2, stroke_width=3, buff=SMALL_BUFF)
                pattern_array2 = self.get_pattern_array(guess2, bucket, priors, n_shown=25)
                prob_bars2 = self.get_prob_bars(pattern_array2.pattern_mobs, width_scalar=5)
                h2_label = self.get_entropy_label(guess2, pattern_array2.distribution)

                group = VGroup(
                    arrow, guess2, h2_label, pattern_array2, prob_bars2,
                )
                self.add(group, second_ents)
                self.wait(1 / self.camera.frame_rate, ignore_presenter_mode=True)
                if i in (0, 1) and j == 0:
                    self.wait(self.transition_time)
                self.remove(group)
            self.add(*group, second_ents)
            self.wait()

            # Consolidate
            arrow, guess2, h2_label, pattern_array2, prob_bars2 = group
            for line in pattern_array2.connecting_lines:
                line.reverse_points()
            h2_label.generate_target()
            h2_label.target.scale(0.8)
            h2_label.target.next_to(guess2, RIGHT)
            guess2.set_color(YELLOW)
            self.add(pattern_array2.connecting_lines, second_ents)
            self.play(
                MoveToTarget(h2_label),
                Uncreate(pattern_array2.connecting_lines, lag_ratio=0.01),
                LaggedStartMap(FadeOut, pattern_array2.pattern_mobs),
                LaggedStartMap(FadeOut, pattern_array2.dot_parts),
                LaggedStartMap(FadeOut, prob_bars2, scale=0.25),
                run_time=self.transition_time
            )
            arrows.add(arrow)
            second_guesses.add(guess2)
            second_ents.add(h2_label)

        # Show weighted sum
        brace = Brace(VGroup(second_ents, pattern_array1), RIGHT)
        label = brace.get_text("Compute a\nweighted average", buff=MED_SMALL_BUFF)

        sum_parts = VGroup()
        for bar, h_label in zip(prob_bars1, second_ents):
            d0 = DecimalNumber(bar.prob, num_decimal_places=3)
            d1 = h_label[1].copy()
            d0.match_height(d1)
            group = VGroup(d0, OldTex("\\cdot", font_size=24), d1)
            group.generate_target()
            group.target.arrange(RIGHT, buff=SMALL_BUFF)
            group.target.next_to(brace, RIGHT)
            group.target.match_y(bar)
            sum_parts.add(group)
            for part in group[:2]:
                part.move_to(bar.label)
                part.set_opacity(0)

        self.play(
            GrowFromCenter(brace),
            Write(label)
        )
        self.wait()
        self.play(
            LaggedStartMap(MoveToTarget, sum_parts, run_time=2),
            label.animate.scale(0.7).to_edge(DOWN),
        )
        self.wait()

    def get_word_mob(self, word):
        return Text(word, font="Consolas", font_size=36)

    def get_pattern_array(self, word, possibilities, priors, n_shown=15):
        weights = get_weights(possibilities, priors)
        dist = get_pattern_distributions([word.text], possibilities, weights)[0]
        indices = np.argsort(dist)[::-1]
        patterns = np.arange(3**5)[indices]
        patterns = patterns[:n_shown]  # Only show non-zero possibilities

        top_parts = VGroup(*(self.get_pattern_mob(p) for p in patterns[:n_shown]))
        dot_parts = OldTex("\\vdots\\\\", "\\le 3^5 \\text{ patterns}\\\\", "\\vdots")

        for prob, row in zip(dist[indices][:n_shown], top_parts):
            row.prob = prob

        stack = VGroup(*top_parts, *dot_parts)
        dot_parts.match_width(stack[0])
        stack.arrange(DOWN, buff=SMALL_BUFF)
        stack.set_max_height(FRAME_HEIGHT - 1)
        stack.next_to(word, RIGHT, buff=1.5)
        # stack.set_y(0)
        stack.shift_onto_screen(buff=MED_LARGE_BUFF)

        pattern_mobs = top_parts
        connecting_lines = VGroup(*(
            self.get_connecting_line(word, row)
            for row in pattern_mobs
        ))

        result = VGroup(pattern_mobs, dot_parts, connecting_lines)
        result.pattern_mobs = pattern_mobs
        result.dot_parts = dot_parts
        result.connecting_lines = connecting_lines
        result.distribution = dist

        return result

    def get_pattern_mob(self, pattern, width=1.5):
        result = Square().replicate(5)
        result.arrange(RIGHT, buff=SMALL_BUFF)
        result.set_stroke(WHITE, width=0.5)
        for square, n in zip(result, pattern_to_int_list(pattern)):
            square.set_fill(WordleScene.color_map[n], 1)
        result.set_width(width)
        result.pattern = pattern
        return result

    def get_connecting_line(self, mob1, mob2):
        diff = mob2.get_left()[0] - mob1.get_right()[0]
        return CubicBezier(
            mob1.get_right() + SMALL_BUFF * RIGHT,
            mob1.get_right() + RIGHT * diff / 2,
            mob2.get_left() + LEFT * diff / 2,
            mob2.get_left() + SMALL_BUFF * LEFT,
            stroke_color=WHITE,
            stroke_width=1,
        )

    def get_prob_bars(self, pattern_mobs, width_scalar=10):
        result = VGroup()
        for pattern_mob in pattern_mobs:
            bar = Rectangle(
                width=width_scalar * pattern_mob.prob,
                height=pattern_mob.get_height(),
                fill_color=self.prob_color,
                fill_opacity=1,
                stroke_width=0.5,
                stroke_color=WHITE,
            )
            bar.next_to(pattern_mob, RIGHT, buff=SMALL_BUFF)
            label = DecimalNumber(100 * pattern_mob.prob, num_decimal_places=1, unit="\\%")
            # label = DecimalNumber(pattern_mob.prob, num_decimal_places=3)
            label.set_height(bar.get_height() * 0.6)
            label.next_to(bar, RIGHT, SMALL_BUFF)
            bar.label = label
            bar.add(label)
            bar.prob = pattern_mob.prob
            result.add(bar)
        return result

    def get_entropy_label(self, word_mob, distribution):
        ent2 = entropy_of_distributions(distribution)
        kw = dict(font_size=24)
        h_label = VGroup(OldTex(f"E[I] = ", **kw), DecimalNumber(ent2, **kw))
        h_label.set_color(self.entropy_color)
        h_label.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=UP)
        h_label.move_to(word_mob)
        h_label.shift(0.5 * DOWN)
        h_label.set_backstroke(width=8)
        return h_label

    def get_info_label(self, bar):
        result = VGroup(
            # DecimalNumber(bar.prob, num_decimal_places=3),
            OldTex("\\log_2\\big( 1 / "),
            DecimalNumber(bar.prob, num_decimal_places=3),
            OldTex("\\big) = "),
            # DecimalNumber(-bar.prob * math.log2(bar.prob), num_decimal_places=3)
            DecimalNumber(-math.log2(bar.prob), num_decimal_places=3)
        )
        result.arrange(RIGHT, buff=SMALL_BUFF)
        result.set_height(bar.get_height())
        result.match_y(bar)
        result.set_x(0, LEFT)
        arrow = Arrow(bar.label.get_right(), result, stroke_width=2, buff=SMALL_BUFF)
        result.add_to_back(arrow)
        return result



# ----- From _2022/wordle/footnote.py -----

class SaletSecondGuessMap(HowLookTwoAheadWorks):
    first_guess = "salet"

    def construct(self):
        path = os.path.join(get_directories()['data'], 'wordle', 'salet_with_brute_force_guess_map.json')
        with open(path) as fp:
            self.guess_map = json.load(fp)

        self.all_words = get_word_list()
        possibilities = get_word_list(short=True)
        priors = self.priors = self.get_priors()

        guess1 = self.get_word_mob(self.first_guess)
        guess1.to_edge(LEFT)
        pattern_array1 = self.get_pattern_array(guess1, possibilities, priors)

        arrows, guess2s = self.get_next_guess_group(guess1.text, pattern_array1, possibilities)

        self.add(guess1)
        self.add(pattern_array1)
        self.play(
            LaggedStartMap(ShowCreation, arrows, lag_ratio=0.5),
            LaggedStartMap(FadeIn, guess2s, lambda m: (m, RIGHT), lag_ratio=0.5),
            run_time=2,
        )
        self.wait()

        for pm, guess2 in zip(pattern_array1.pattern_mobs, guess2s):
            bucket = get_possible_words(guess1.text, pm.pattern, possibilities)
            pattern_array2 = self.get_pattern_array(guess2, bucket, priors)
            ng_group = self.get_next_guess_group(
                guess2.text, pattern_array2, bucket,
                prefix=guess1.text + "".join(map(str, pattern_to_int_list(pm.pattern))),
            )

            self.add(pattern_array2, ng_group)
            self.wait(0.5)
            self.remove(pattern_array2, ng_group)

    def get_next_guess_group(self, guess, pattern_array, possibilities, prefix=""):
        arrows = VGroup()
        guesses = VGroup()
        for pm in pattern_array.pattern_mobs:
            ps = "".join(map(str, pattern_to_int_list(pm.pattern)))
            key = prefix + guess + ps
            if key in self.guess_map:
                next_guess = self.guess_map[key]
            else:
                next_guess = optimal_guess(
                    self.all_words,
                    get_possible_words(guess, pm.pattern, possibilities),
                    self.priors,
                    optimize_for_uniform_distribution=True
                )
            next_guess_mob = self.get_word_mob(next_guess)
            next_guess_mob.scale(0.8)
            arrow = Vector(0.5 * RIGHT, stroke_width=3)
            arrow.next_to(pm, RIGHT, buff=SMALL_BUFF)
            next_guess_mob.next_to(arrow, RIGHT, buff=SMALL_BUFF)

            arrows.add(arrow)
            guesses.add(next_guess_mob)

        return VGroup(arrows, guesses)
