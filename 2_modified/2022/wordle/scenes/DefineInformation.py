# ==============================================================================
# Scene:      DefineInformation
# Source:     videos/_2022/wordle/scenes.py (lines 1868-2129)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl DefineInformation.py DefineInformation -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
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


PATTERN_MATRIX_FILE = os.path.join(DATA_DIR, "pattern_matrix.npy")


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


class DefineInformation(Scene):
    def construct(self):
        # Spaces
        pre_space = Square(side_length=3)
        pre_space.set_stroke(WHITE, 2)
        pre_space.set_fill(BLUE, 0.7)

        post_space = self.get_post_space(pre_space, 1)
        arrow = Vector(2 * RIGHT)
        group = VGroup(pre_space, arrow, post_space)
        group.arrange(RIGHT)

        # Labels
        kw = dict(font_size=36)
        pre_label = Text("Space of possibilities", **kw)
        pre_label.next_to(pre_space, UP, SMALL_BUFF)
        obs_label = Text("Observation", **kw)
        obs_label.next_to(arrow, UP)
        post_labels = self.get_post_space_labels(post_space, **kw)

        # 1 bit (has an s)
        self.add(pre_space)
        self.add(pre_label)
        self.wait()
        self.wait()
        self.play(
            ShowCreation(arrow),
            FadeIn(obs_label, lag_ratio=0.1),
            FadeTransform(pre_space.copy().set_fill(opacity=0), post_space),
            FadeIn(post_labels[1], 3 * RIGHT),
        )
        self.wait()
        self.play(Write(post_labels[0], run_time=1))
        self.wait()

        # Show all words
        n_rows = 25
        n_cols = 8
        all_words = get_word_list()
        words_sample = random.sample(all_words, n_rows * n_cols)
        word_grid = WordleScene.get_grid_of_words(words_sample, n_rows, n_cols)
        word_grid.replace(pre_space, dim_to_match=1)
        word_grid.scale(0.95)
        word_grid.shuffle()
        for word in word_grid:
            word.save_state()
        word_grid.scale(2)
        word_grid.set_opacity(0)

        self.play(LaggedStartMap(Restore, word_grid, lag_ratio=0.02, run_time=2))
        self.wait()

        word_grid.save_state()
        word_grid.generate_target()
        for word in word_grid.target:
            if 's' not in word.text:
                word.set_opacity(0.1)

        has_s = OldTexText("Has an `s'", font_size=24)
        has_s.next_to(arrow, DOWN)
        self.play(
            MoveToTarget(word_grid),
            FadeIn(has_s, 0.5 * DOWN),
        )
        self.wait()

        # 2 bits (has a t)
        frame = self.camera.frame
        mini_group1 = self.get_mini_group(pre_space, arrow, post_space, post_labels)
        mini_group1.target.to_edge(UP, buff=0.25)
        post_space2 = self.get_post_space(pre_space, 2).move_to(post_space)
        post_labels2 = self.get_post_space_labels(post_space2, **kw)
        has_t = OldTexText("Has a `t'", font_size=24)
        has_t.next_to(arrow, DOWN, SMALL_BUFF)

        self.play(
            MoveToTarget(mini_group1),
            FadeOut(has_s),
            Restore(word_grid),
            FadeOut(post_space),
            FadeOut(post_labels),
            frame.animate.move_to(2 * RIGHT)
        )
        self.play(
            FadeTransform(pre_space.copy(), post_space2),
            FadeIn(post_labels2, shift=3 * RIGHT)
        )
        self.wait()
        word_grid.generate_target()
        for word in word_grid.target:
            if 't' not in word.text:
                word.set_opacity(0.1)
        self.play(
            FadeIn(has_t, 0.5 * DOWN),
            MoveToTarget(word_grid),
        )
        self.wait()
        self.remove(has_t)
        word_grid.restore()

        # 3 through 5 bits
        last_posts = VGroup(post_space2, post_labels2)
        mini_groups = VGroup(mini_group1)
        for n in range(3, 7):
            new_mini = self.get_mini_group(pre_space, arrow, *last_posts)
            new_mini.target.next_to(mini_groups, DOWN, buff=0.5)
            new_post_space = self.get_post_space(pre_space, n)
            new_post_space.move_to(post_space)
            new_post_labels = self.get_post_space_labels(new_post_space, **kw)

            self.play(LaggedStart(
                MoveToTarget(new_mini),
                AnimationGroup(
                    FadeOut(last_posts),
                    FadeIn(new_post_space),
                    FadeIn(new_post_labels),
                ),
                lag_ratio=0.5
            ))
            self.wait()

            mini_groups.add(new_mini)
            last_posts = VGroup(new_post_space, new_post_labels)

        # Show formula
        group = VGroup(pre_space, pre_label, word_grid, arrow, obs_label, *last_posts)

        kw = dict(tex_to_color_map={"I": YELLOW})
        formulas = VGroup(
            OldTex("\\left( \\frac{1}{2} \\right)^I = p", **kw),
            OldTex("2^I = \\frac{1}{p}", **kw),
            OldTex("I = \\log_2\\left(\\frac{1}{p}\\right)", **kw),
            OldTex("I = -\\log_2(p)", **kw)
        )
        formulas[:3].arrange(RIGHT, buff=LARGE_BUFF)
        formulas[:3].to_edge(UP)
        formulas[1:3].match_y(formulas[0][-1][0])
        formulas[3].next_to(formulas[2], DOWN, aligned_edge=LEFT)

        formulas[0].save_state()
        formulas[0].move_to(formulas[1])
        self.play(
            FadeIn(formulas[0]),
            group.animate.to_edge(DOWN, buff=MED_SMALL_BUFF)
        )
        self.wait()
        self.play(Restore(formulas[0]))
        for i in (0, 1, 2):
            self.play(TransformMatchingShapes(formulas[i].copy(), formulas[i + 1]))
            self.wait()

        rhs_rect = SurroundingRectangle(formulas[3])
        rhs_rect.set_stroke(YELLOW, 2)
        self.play(ShowCreation(rhs_rect))
        self.wait()

        # Ask why?
        randy = Randolph("confused", height=1.5)
        randy.next_to(formulas[2], DL, MED_LARGE_BUFF)
        randy.look_at(rhs_rect)
        randy.save_state()
        randy.change("plain")
        randy.set_opacity(0)

        self.play(Restore(randy))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("maybe"))
        self.play(Blink(randy))
        self.wait()

        # Readibility
        expr = OldTex(
            "20 \\text{ bits} \\Leftrightarrow p \\approx 0.00000095",
            tex_to_color_map={"\\text{bits}": YELLOW}
        )
        expr.next_to(group, UP, buff=0.75)

        self.play(
            FadeOut(randy),
            FadeOut(formulas[3]),
            FadeOut(rhs_rect),
            Write(expr),
        )
        self.wait()

        # Additive
        group = group[:-2]
        self.play(
            FadeOut(expr),
            FadeOut(last_posts),
            group.animate.scale(0.7, about_edge=DL),
            FadeOut(mini_groups, RIGHT),
            frame.animate.move_to(RIGHT),
        )

        ps1 = self.get_post_space(pre_space, 2)
        ps2 = self.get_post_space(pre_space, 5)
        ps2.set_stroke(width=1)
        ps2.add(ps1.copy().fade(0.5))
        arrow2 = arrow.copy()
        ps1.next_to(arrow, RIGHT)
        arrow2.next_to(ps1, RIGHT)
        ps2.next_to(arrow2, RIGHT)

        ps1.label = self.get_post_space_labels(ps1, font_size=24)
        ps2.label = self.get_post_space_labels(
            self.get_post_space(pre_space, 3).replace(ps2),
            font_size=24
        )

        self.play(
            FadeTransform(pre_space.copy().set_opacity(0), ps1),
            FadeIn(ps1.label, 2 * RIGHT),
        )
        self.wait()
        self.play(
            FadeTransform(ps1.copy().set_opacity(0), ps2),
            FadeIn(ps2.label, 2 * RIGHT),
            ShowCreation(arrow2),
        )
        self.wait()

        brace = Brace(VGroup(ps1.label, ps2.label), UP)
        b_label = brace.get_text("5 bits").set_color(YELLOW)

        self.play(
            GrowFromCenter(brace),
            FadeIn(b_label, 0.2 * UP),
        )
        self.wait()

    def get_post_space(self, pre_space, n_bits):
        n_rows = 2**((n_bits // 2))
        n_cols = 2**((n_bits // 2) + n_bits % 2)
        result = pre_space.get_grid(n_rows, n_cols, buff=0)
        result.replace(pre_space, stretch=True)
        result[:-1].set_fill(opacity=0)
        return result

    def get_post_space_labels(self, post_space, **kw):
        n_bits = int(math.log2(len(post_space)))
        top_label = OldTexText("Information = ", f"${n_bits}$ bits", **kw)
        if n_bits == 1:
            top_label[-1][-1].set_opacity(0)
        top_label.next_to(post_space, UP, buff=0.15)
        top_label.set_color(YELLOW)
        bottom_label = OldTexText(f"$p = {{1 \\over {2**n_bits}}}$", **kw)
        bottom_label.next_to(post_space, DOWN, SMALL_BUFF)
        return VGroup(top_label, bottom_label)

    def get_mini_group(self, pre_space, arrow, post_space, post_labels):
        mini_group = VGroup(pre_space, arrow, post_space, post_labels[0]).copy()
        mini_group.generate_target()
        mini_group.target.scale(0.25)
        mini_group.target[-1][0].set_opacity(0)
        mini_group.target[-1][1].scale(3, about_edge=DOWN)
        mini_group.target[-1][1].match_x(mini_group.target[2])
        mini_group.target.next_to(post_space, RIGHT, buff=2.0)
        mini_group[::2].set_fill(opacity=0)
        mini_group.target[::2].set_stroke(width=1)
        return mini_group
