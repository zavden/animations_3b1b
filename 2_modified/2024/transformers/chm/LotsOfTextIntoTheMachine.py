# ==============================================================================
# Scene:      LotsOfTextIntoTheMachine
# Source:     videos/_2024/transformers/chm.py (lines 185-229)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/generation.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl LotsOfTextIntoTheMachine.py LotsOfTextIntoTheMachine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR points to _lib/data (in the original, to Grant's output folder)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import warnings
from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel
import torch
import openai
from pathlib import Path


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")


def get_paragraph(words, line_len=40, font_size=48):
    """
    Handle word wrapping
    """
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, alignment="LEFT", font_size=font_size)


def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))
    
    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class Dial(VGroup):
    def __init__(
        self,
        radius=0.5,
        relative_tick_size=0.2,
        value_range=(0, 1, 0.1),
        initial_value=0,
        arc_angle=270 * DEGREES,
        stroke_width=2,
        stroke_color=WHITE,
        needle_color=BLUE,
        needle_stroke_width=5.0,
        value_to_color_config=dict(),
        set_anim_streak_color=TEAL,
        set_anim_streak_width=4,
        set_value_anim_streak_density=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())



# ----- From _2024/transformers/generation.py -----

@lru_cache(maxsize=1)
def get_gpt2_tokenizer(model_name='gpt2'):
    return GPT2Tokenizer.from_pretrained(model_name)


@lru_cache(maxsize=1)
def get_gpt2_model(model_name='gpt2'):
    return GPT2LMHeadModel.from_pretrained(model_name)


def gpt2_predict_next_token(text, n_shown=7):
    tokenizer = get_gpt2_tokenizer()
    model = get_gpt2_model()
    # Encode the input text
    indexed_tokens = tokenizer.encode(
        text, add_special_tokens=False, return_tensors='pt'
    )

    # Predict all tokens
    with torch.no_grad():
        outputs = model(indexed_tokens)
        # Pull out the first batch, and the last token prediction
        predictions = outputs[0][0, -1, :]

    # Get the predicted next token
    indices = torch.argsort(predictions)
    top_indices = reversed(indices[-n_shown:])
    tokens = list(map(tokenizer.decode, top_indices))
    probs = softmax(predictions)[top_indices]

    return tokens, probs


def gpt3_predict_next_token(text, n_shown=10, random_seed=0):
    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.Completion.create(
        # Or another model version, adjust as necessary
        engine="gpt-3.5-turbo-instruct",
        prompt=text,
        max_tokens=1,
        n=1,
        temperature=1.0,
        user=str(random_seed),
        logprobs=50  # I think this is actually set to a max of 20?
    )
    top_logprob_dict = response.choices[0]["logprobs"]["top_logprobs"][0]
    tokens, logprobs = zip(*top_logprob_dict.items())
    probs = np.exp(logprobs)
    indices = np.argsort(-probs)
    shown_tokens = [tokens[i] for i in indices[:n_shown]]
    return shown_tokens, probs[indices[:n_shown]]


class SimpleAutogregression(InteractiveScene):
    text_corner = 3.5 * UP + 0.75 * RIGHT
    line_len = 31
    font_size = 35
    n_shown_predictions = 12
    seed_text = "Behold, a wild pi creature, foraging in its native"
    seed_text_color = BLUE_B
    machine_name = "Transformer"
    machine_phi = 10 * DEGREES
    machine_theta = 12 * DEGREES
    n_predictions = 120
    skip_through = False
    random_seed = 0
    model = "gpt2"

    def construct(self):
        # Repeatedly generate
        text_mob, next_word_line, machine = self.init_text_and_machine()
        for n in range(self.n_predictions):
            text_mob = self.new_selection_cycle(
                text_mob, next_word_line, machine,
                quick=(n > 10),
                skip_anims=self.skip_through,
            )

    def init_text_and_machine(self):
        # Set up active text
        self.cur_str = self.seed_text
        text_mob = self.string_to_mob(self.cur_str)
        text_mob.set_color(self.seed_text_color)
        next_word_line = self.get_next_word_line(text_mob)

        # Set up Transformer as some sort of machine
        machine = self.get_transformer_drawing()
        machine.set_y(0).to_edge(LEFT, buff=-0.6)

        self.add(text_mob)
        self.add(next_word_line)
        self.add(machine)

        return text_mob, next_word_line, machine

    def string_to_mob(self, text):
        text += " l"  # Dumb hack for alignment
        result = get_paragraph(
            text.replace("\n", " ").split(" "),
            self.line_len,
            self.font_size
        )
        result.move_to(self.text_corner, UL)
        result[-1].set_fill(BLACK, 0)  # Continue dumb hack
        result[-1].stretch(0, 0, about_edge=LEFT)
        return result

    def get_next_word_line(self, text_mob, char_len=7):
        next_word_line = Underline(text_mob[:char_len])
        next_word_line.set_stroke(TEAL, 2)
        next_word_line.next_to(text_mob[-1], RIGHT, SMALL_BUFF, aligned_edge=DOWN)
        if self.skip_through:
            next_word_line.set_opacity(0)
        return next_word_line

    def get_transformer_drawing(self):
        self.camera.light_source.move_to([-5, 5, 10])
        self.frame.set_field_of_view(20 * DEGREES)
        blocks = VGroup(
            VPrism(3, 2, 0.2)
            for n in range(10)
        )
        blocks.set_fill(GREY_D, 1)
        blocks.set_stroke(width=0)
        blocks.set_shading(0.25, 0.5, 0.2)
        blocks.arrange(OUT)
        blocks.move_to(ORIGIN, OUT)
        blocks.rotate(self.machine_phi, RIGHT, about_edge=OUT)
        blocks.rotate(self.machine_theta, UP, about_edge=OUT)

        blocks.deactivate_depth_test()
        for block in blocks:
            block.sort(lambda p: p[2])

        word = Text(self.machine_name, alignment="LEFT")
        word.next_to(blocks[-1], UP)
        word.shift(0.1 * UP + 0.4 * LEFT)
        word.move_to(blocks[-1])
        word.set_backstroke(BLACK, 5)
        out_arrow = Vector(
            0.5 * RIGHT, stroke_width=10,
            max_tip_length_to_length_ratio=0.5,
            max_width_to_length_ratio=12
        )
        out_arrow.next_to(blocks[-1], RIGHT, buff=SMALL_BUFF)
        out_arrow.set_opacity(0)

        result = VGroup(blocks, word, out_arrow)
        return result

    def get_distribution(
        self, words, probs, machine,
        font_size=24,
        width_100p=1.8,
        bar_height=0.25,
        show_ellipses=True
    ):
        labels = VGroup(Text(word, font_size=font_size) for word in words)
        bars = VGroup(
            Rectangle(prob * width_100p, bar_height)
            for prob, label in zip(probs, labels)
        )
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.5 * bar_height)
        bars.set_fill(opacity=1)
        bars.set_submobject_colors_by_gradient(TEAL, YELLOW)
        bars.set_stroke(WHITE, 1)

        bar_groups = VGroup()
        for label, bar, prob in zip(labels, bars, probs):
            prob_label = Integer(int(100 * prob), unit="%", font_size=0.75 * font_size)
            prob_label.next_to(bar, RIGHT, buff=SMALL_BUFF)
            label.next_to(bar, LEFT)
            bar_groups.add(VGroup(label, bar, prob_label))

        if show_ellipses:
            ellipses = Tex(R"\vdots", font_size=font_size)
            ellipses.next_to(bar_groups[-1][0], DOWN)
            bar_groups.add(ellipses)

        arrow_point = machine[-1].get_right()
        bar_groups.shift(arrow_point - bars.get_left() + 1.5 * RIGHT)
        bar_groups.align_to(machine, UP)

        return bar_groups

    def animate_text_input(self, text_mob, machine, position_text_over_machine=True, added_anims=[], lag_ratio=0.02):
        blocks = machine[0]
        text_copy = text_mob.copy()
        if position_text_over_machine:
            text_copy.target = text_copy.generate_target()
            text_copy.target.set_max_width(4)
            text_copy.target.next_to(blocks[0], UP)
            text_copy.target.shift_onto_screen()
            self.play(MoveToTarget(text_copy, path_arc=-45 * DEGREES))
        self.play(LaggedStart(
            *added_anims,
            Transform(
                text_copy,
                VGroup(VectorizedPoint(machine.get_top())),
                lag_ratio=lag_ratio,
                run_time=1,
                path_arc=-45 * DEGREES,
                remover=True,
            ),
            LaggedStart(
                (
                    block.animate.set_color(
                        block.get_color() if block is blocks[-1] else TEAL
                    ).set_anim_args(rate_func=there_and_back)
                    for block in blocks
                ),
                lag_ratio=0.1,
                run_time=1
            ),
            Animation(machine[1:]),
            lag_ratio=0.5
        ))

    def animate_prediction_ouptut(self, machine, cur_str):
        words, probs = self.predict_next_token(cur_str)
        bar_groups = self.get_distribution(words, probs, machine)
        self.play(
            LaggedStart(
                (FadeInFromPoint(bar_group, machine[0][-1].get_right())
                for bar_group in bar_groups),
                lag_ratio=0.025,
                group=bar_groups,
                run_time=1
            )
        )
        return bar_groups

    def animate_random_sample(self, bar_groups):
        widths = np.array([group[1].get_width() for group in bar_groups[:-1]])
        dist = widths / widths.sum()
        seed = random.randint(0, 1000)
        buff = 0.025
        highlight_rect = SurroundingRectangle(bar_groups[0], buff=buff)
        highlight_rect.set_stroke(YELLOW, 2)
        highlight_rect.set_fill(YELLOW, 0.25)

        def highlight_randomly(rect, dist, alpha):
            np.random.seed(seed + int(10 * alpha))
            index = np.random.choice(np.arange(len(dist)), p=dist)
            rect.surround(bar_groups[index], buff=buff)
            rect.stretch(1.1, 0)

        self.play(
            UpdateFromAlphaFunc(highlight_rect, lambda rect, a: highlight_randomly(rect, dist, a)),
            Animation(bar_groups)
        )

        bar_groups.add_to_back(highlight_rect)

    def animate_word_addition(self, bar_groups, text_mob, next_word_line, force_unskip=False):
        # Choose the highlighted_group
        bar_group = None
        if isinstance(bar_groups[0], Rectangle):
            # Use the highlight rect to find the group element
            bars = bar_groups[1:-1]
            diffs = [abs(bg.get_y() - bar_groups[0].get_y()) for bg in bars]
            bar_group = bar_groups[1:][np.argmin(diffs)]
        if bar_group is None:
            bar_group = bar_groups[0]

        # Animate selection
        word = bar_group[0].get_text()
        new_str = self.cur_str + word
        new_text_mob = self.string_to_mob(new_str)
        new_text_mob[:len(self.seed_text.replace(" ", ""))].set_color(self.seed_text_color)

        word_targets = new_text_mob[word.strip()]
        if len(word_targets) > 0:
            target = word_targets[-1]
        else:
            target = new_text_mob[-len(word) - 1:-1]

        # target = new_text_mob[-len(word):]

        self.add(bar_groups)
        self.play(
            FadeTransform(bar_group[0].copy(), target),
            Transform(
                next_word_line,
                self.get_next_word_line(new_text_mob),
            ),
        )
        if force_unskip:
            self.skip_animations = False
            target.save_state()
            target.set_fill(YELLOW)
            self.wait(0.5)
            target.restore()
            self.skip_animations = True
        self.play(
            FadeOut(bar_groups),
        )

        self.remove(text_mob)
        self.add(new_text_mob)

        self.cur_str = new_str

        return new_text_mob

    def new_selection_cycle(self, text_mob, next_word_line, machine, quick=False, skip_anims=False):
        if skip_anims:
            self.skip_animations = True

        if quick:
            words, probs = self.predict_next_token(self.cur_str)
            bar_groups = self.get_distribution(words, probs, machine)
            self.add(bar_groups)
        else:
            self.animate_text_input(text_mob, machine)
            bar_groups = self.animate_prediction_ouptut(machine, self.cur_str)
        self.animate_random_sample(bar_groups)
        new_text_mob = self.animate_word_addition(
            bar_groups, text_mob, next_word_line,
            force_unskip=skip_anims
        )
        return new_text_mob

    #

    def predict_next_token(self, text):
        result = None
        n_shown = self.n_shown_predictions
        if self.model == "gpt3":
            try:
                result = gpt3_predict_next_token(
                    text, n_shown, random_seed=self.random_seed
                )
            except Exception as e:
                pass
        if result is None:
            result = gpt2_predict_next_token(text, n_shown)
        return result



# ----- From _2024/transformers/chm.py -----

class PredictTheNextWord(SimpleAutogregression):
    text_corner = 3.5 * UP + 6.5 * LEFT
    machine_name = "Large\nLanguage\nModel"
    seed_text = "Paris is a city in"
    model = "gpt3"
    n_shown_predictions = 12
    random_seed = 2

    def construct(self):
        # Setup machine
        text_mob, next_word_line, machine = self.init_text_and_machine()
        machine.move_to(ORIGIN)
        machine[1].set_backstroke(BLACK, 3)

        text_group = VGroup(text_mob, next_word_line)
        text_group.save_state()
        text_group.scale(1.5)
        text_group.match_x(machine[0]).to_edge(UP)

        # Introduce the machine
        in_arrow = Arrow(text_group, machine[0].get_top(), thickness=5)
        frame = self.frame
        self.set_floor_plane("xz")
        blocks = machine[0]
        llm_text = machine[1]
        block_outlines = blocks.copy()
        block_outlines.set_fill(opacity=0)
        block_outlines.set_stroke(GREY_B, 2)
        block_outlines.insert_n_curves(20)

        flat_dials, last_dials = self.get_machine_dials(blocks)

        self.clear()
        frame.reorient(-31, -4, -5, (-0.24, -0.26, -0.06), 3)
        self.play(
            FadeIn(blocks, shift=0.0, lag_ratio=0.01),
            LaggedStartMap(VShowPassingFlash, block_outlines.family_members_with_points(), time_width=2.0, lag_ratio=0.01, remover=True),
            LaggedStartMap(VFadeInThenOut, flat_dials, lag_ratio=0.001, remover=True),
            Write(llm_text, time_span=(2, 4), stroke_color=WHITE),
            FadeIn(last_dials, time_span=(4, 5)),
            frame.animate.reorient(0, 0, 0, (-0.17, -0.12, 0.0), 4.50),
            run_time=6,
        )
        blocks[-1].add(last_dials)
        self.play(
            frame.animate.to_default_state(),
            FadeIn(text_group, UP),
            GrowFromCenter(in_arrow),
            run_time=3
        )

        # Single word prediction
        out_arrow = Vector(1.5 * RIGHT, thickness=5)
        out_arrow.next_to(machine[0][-1], RIGHT)
        prediction = Text("France", font_size=72)
        prediction.next_to(out_arrow, RIGHT)

        self.animate_text_input(
            text_mob, machine,
            position_text_over_machine=False,
        )
        self.play(
            LaggedStart(
                (TransformFromCopy(VectorizedPoint(machine.get_right()), letter)
                for letter in prediction),
                lag_ratio=0.05,
            ),
            GrowArrow(out_arrow)
        )
        self.wait()
        machine.replace_submobject(2, out_arrow)

        # Probability distribution
        self.play(FadeOut(prediction, DOWN))
        bar_groups = self.animate_prediction_ouptut(machine, self.cur_str)
        self.wait()

        # Show auto_regression
        self.play(
            Restore(text_group),
            FadeOut(in_arrow),
        )

        seed_label = Text("Seed text")
        seed_label.set_color(YELLOW)
        seed_label.next_to(text_mob, DOWN)

        self.play(
            FadeIn(seed_label, rate_func=there_and_back_with_pause),
            FlashAround(text_mob, time_width=2),
            frame.animate.reorient(0, 0, 0, (0.7, -0.01, 0.0), 8.52),
            run_time=2,
        )

        self.animate_random_sample(bar_groups)
        new_text_mob = self.animate_word_addition(
            bar_groups, text_mob, next_word_line,
        )

        # More!
        for n in range(20):
            text_mob = self.new_selection_cycle(
                text_mob, next_word_line, machine,
                quick=True,
                skip_anims=(n > 5),
            )
            self.wait(0.25)

    def get_machine_dials(self, blocks):
        dials = VGroup(
            Dial().get_grid(8, 12).set_width(0.9 * block.get_width()).move_to(block)
            for block in blocks
        )
        dials.set_stroke(opacity=0.5)
        for group in dials:
            for dial in group:
                dial.set_value(dial.get_random_value())
        flat_dials = VGroup(*it.chain(*dials))
        last_dials = dials[-1].copy()
        last_dials.set_stroke(opacity=0.1)

        return flat_dials, last_dials


class LotsOfTextIntoTheMachine(PredictTheNextWord):
    run_time = 25
    max_snippet_width = 3

    def construct(self):
        # Add machine
        text_mob, next_word_line, machine = self.init_text_and_machine()
        machine.scale(1.5)
        self.clear()
        self.add(machine)

        blocks, title = machine[:2]
        dials = Dial().get_grid(8, 12).set_width(0.9 * blocks[-1].get_width()).move_to(blocks[-1])
        dials.set_stroke(opacity=0.1)
        blocks[-1].add(dials)

        machine.center()
        machine[1].set_stroke(BLACK, 3)

        # Feed in lots of text
        snippets = self.get_text_snippets()
        text_mobs = VGroup(get_paragraph(snippet.split(" "), line_len=25) for snippet in snippets)
        directions = compass_directions(12, start_vect=UR)
        for text_mob, vect in zip(text_mobs, it.cycle(directions)):
            text_mob.set_max_width(self.max_snippet_width)
            text_mob.move_to(5 * vect).shift_onto_screen(buff=0.25)

        self.play(
            LaggedStart(
                (Succession(
                    FadeIn(text_mob),
                    text_mob.animate.set_opacity(0).move_to(machine.get_center()),
                )
                for text_mob in text_mobs),
                lag_ratio=0.05,
                run_time=self.run_time
            )
        )
        self.remove(text_mobs)
        self.wait()

    def get_text_snippets(self):
        facts = Path(DATA_DIR, "pile_of_text.txt").read_text().split("\n")
        random.shuffle(facts)
        return facts
