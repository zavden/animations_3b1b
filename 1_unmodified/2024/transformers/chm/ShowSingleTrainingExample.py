# ==============================================================================
# Scene:      ShowSingleTrainingExample
# Source:     videos/_2024/transformers/chm.py (lines 1111-1217)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/generation.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ShowSingleTrainingExample.py ShowSingleTrainingExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import warnings
from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel
import torch
import openai


# ----- From _2024/transformers/helpers.py -----

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


class ShowMachineWithDials(PredictTheNextWord):
    words = ['worst', 'age', 'worse', 'best', 'most', 'end', 'very', 'blur']
    logprobs = [4.0, 2.15, 1.89, 1.4, 0.1, -0.18, -0.23, -0.61]

    def construct(self):
        # Show machine (same position as in PredictTheNextWord)
        frame = self.frame
        self.set_floor_plane("xz")
        blocks, llm_text, flat_dials, last_dials = self.get_blocks_and_dials()

        self.clear()
        self.add(frame)
        frame.reorient(0, 0, 0, (-0.17, -0.12, 0.0), 4.50)
        self.add(blocks, llm_text, last_dials)

        # Prepare dial highlight
        last_dials.target = last_dials.generate_target()
        self.fix_dials(last_dials.target)

        small_rect = SurroundingRectangle(last_dials[0], buff=0.025)
        small_rect.set_stroke(BLUE, 2)
        big_rect = small_rect.copy().scale(4)
        big_rect.next_to(blocks, UP, buff=SMALL_BUFF, aligned_edge=LEFT + OUT)
        big_rect.shift(1.5 * RIGHT)
        big_dial = last_dials[0].copy().scale(4).set_stroke(opacity=1)
        big_dial.move_to(big_rect)
        rect_lines = VGroup(
            Line(small_rect.get_corner(UL), big_rect.get_corner(DL)),
            Line(small_rect.get_corner(UR), big_rect.get_corner(DR)),
        )
        rect_lines.set_stroke(WHITE, width=(1, 3))
        highlighed_parameter_group = VGroup(small_rect, rect_lines, big_rect, big_dial)

        last_dials.set_stroke(width=1, opacity=1)
        self.play(
            MoveToTarget(last_dials),
            FadeOut(llm_text),
            FadeIn(small_rect),
        )

        # Show an example input and output
        example = self.get_example(blocks)
        in_text, in_arrow, out_arrow, bar_groups = example
        logprobs = example.logprobs
        true_probs = 100 * softmax(logprobs)
        bar_groups = self.get_output_distribution(self.words, 0.1 * logprobs, out_arrow)

        self.play(
            LaggedStart(
                ShowCreation(rect_lines, lag_ratio=0),
                TransformFromCopy(small_rect, big_rect),
                TransformFromCopy(last_dials[0], big_dial),
                FadeIn(in_text),
                GrowArrow(in_arrow),
                FadeIn(bar_groups),
                GrowArrow(out_arrow),
            ),
            frame.animate.reorient(0, 0, 0, (-0.43, 0.38, 0.0), 7.05),
            run_time=2
        )
        self.play(
            last_dials[0].animate_set_value(0.8),
            big_dial.animate_set_value(0.8),
            LaggedStart(
                (dial.animate_set_value(dial.get_random_value())
                for dial in last_dials[1:]),
                lag_ratio=1.0 / len(last_dials),
            ),
            *(
                self.bar_group_change_animation(bg, value)
                for bg, value in zip(bar_groups[:-1], true_probs)
            ),
            run_time=3
        )
        self.wait()

        # Play around tweaking the parameters, and seeing the output change
        self.play(
            LaggedStart(
                (dial.animate_set_value(0)
                for dial in last_dials[:12]),
                lag_ratio=0.01,
            ),
            big_dial.animate_set_value(0),
            self.bar_group_change_animation(bar_groups[0], 50),
            self.bar_group_change_animation(bar_groups[1], 34),
            self.bar_group_change_animation(bar_groups[2], 5),
            run_time=4,
        )
        self.play(
            LaggedStart(
                (dial.animate_set_value(1)
                for dial in last_dials[:12]),
                lag_ratio=0.01,
            ),
            big_dial.animate_set_value(1),
            self.bar_group_change_animation(bar_groups[0], 80),
            self.bar_group_change_animation(bar_groups[1], 5),
            self.bar_group_change_animation(bar_groups[2], 15),
            run_time=4,
        )
        self.wait()

        # Mention randomness
        random_words = Text("Initially random")
        random_words.next_to(blocks, UP)
        random_words.set_color(RED)
        out_dots = Tex(R"...", font_size=120)
        out_dots.next_to(out_arrow, RIGHT)

        self.play(
            FadeOut(big_rect),
            Uncreate(rect_lines, lag_ratio=0),
            FadeOut(small_rect),
            Transform(big_dial, last_dials[0])
        )
        self.play(
            Write(random_words),
            LaggedStart(
                (dial.animate_set_value(dial.get_random_value())
                for dial in last_dials),
                lag_ratio=0.5 / len(last_dials),
                run_time=2
            ),
            FadeOut(bar_groups),
        )
        self.play(Write(out_dots))
        self.wait()
        self.play(
            FadeOut(dots),
            FadeOut(random_words),
            FadeIn(bar_groups),
        )

        # Show many many parameters
        example.save_state()
        blocks.save_state()
        last_dials.save_state()
        all_dials = VGroup(*flat_dials, *last_dials)
        all_dials.generate_target()
        all_dials.target.space_out_submobjects(3)
        new_dials = VGroup(
            all_dials.target.copy().shift(3 * 2 * x * (flat_dials.get_center() - last_dials.get_center()))
            for x in range(1, 9)
        )

        self.play(
            FadeOut(example),
            FadeOut(blocks),
            FadeIn(flat_dials),
            FadeOut(bar_groups),
            FadeOut(out_arrow),
        )
        self.play(
            FadeOut(highlighed_parameter_group),
            MoveToTarget(all_dials),
            LaggedStart(
                (TransformFromCopy(all_dials.copy().set_opacity(0), nd)
                for nd in new_dials),
                lag_ratio=0.05,
            ),
            frame.animate.reorient(-9, 0, 0, (-0.71, -0.07, -0.06), 9.64),
            run_time=4
        )
        self.wait()

    def get_blocks_and_dials(self):
        machine = self.get_transformer_drawing()
        machine.move_to(ORIGIN)
        self.machine = machine

        blocks = machine[0]
        llm_text = machine[1]
        llm_text.set_backstroke(BLACK, 2)
        flat_dials, last_dials = self.get_machine_dials(blocks)
        return blocks, llm_text, flat_dials, last_dials

    def get_example(self, blocks):
        in_text = Text("It was the best\nof times it was\nthe _", alignment="LEFT")
        in_text[-1].stretch(4, 0, about_edge=LEFT)
        in_text.next_to(blocks, LEFT, LARGE_BUFF)
        in_arrow = Arrow(in_text, blocks)

        out_arrow = Vector(RIGHT)
        out_arrow.next_to(blocks[-1], RIGHT, buff=0.1)
        logprobs = np.array(self.logprobs)
        bar_groups = self.get_output_distribution(self.words, logprobs, out_arrow)
        example = VGroup(in_text, in_arrow, out_arrow, bar_groups)
        example.logprobs = logprobs
        return example

    def fix_dials(self, dials):
        for dial in dials:
            dial.set_stroke(width=1, opacity=1)
            dial.needle.set_stroke(width=(2, 0))
        return dials

    def bar_group_change_animation(self, bar_group, new_value):
        text, rect, value_mob = bar_group
        buff = value_mob.get_left() - rect.get_right()
        factor = new_value / value_mob.get_value()

        return AnimationGroup(
            rect.animate.stretch(factor, 0, about_edge=LEFT),
            ChangeDecimalToValue(value_mob, new_value),
            UpdateFromFunc(text, lambda m: value_mob.move_to(rect.get_right() + buff, LEFT)),
        )

    def get_output_distribution(self, words, logprobs, out_arrow):
        probs = softmax(logprobs)
        bar_groups = self.get_distribution(words, probs, self.machine, width_100p=1.0)
        bar_groups.next_to(out_arrow, RIGHT)
        return bar_groups


class ShowSingleTrainingExample(ShowMachineWithDials):
    logprobs = [4.0, 6.15, 1.89, 1.4, 0.1, -0.18, -0.23, -0.61]

    def construct(self):
        # Add state from before
        frame = self.frame
        self.set_floor_plane("xz")

        blocks, llm_text, flat_dials, last_dials = self.get_blocks_and_dials()
        self.fix_dials(last_dials)
        example = self.get_example(blocks)
        in_text, in_arrow, out_arrow, bar_groups = example

        self.add(blocks, last_dials)

        # Show example up top
        parts = ("It was the best of times it was the", "worst")
        sentence = Text(" ".join(parts))
        start = sentence[parts[0]][0]
        end = sentence[parts[1]][0]
        sentence.set_width(10)
        sentence.next_to(blocks, UP, buff=1.5)

        start_rect = SurroundingRectangle(start)
        start_rect.set_stroke(BLUE, 2)
        start_rect.set_fill(BLUE, 0.2)
        end_rect = SurroundingRectangle(end)
        end_rect.match_height(start_rect, stretch=True).match_y(start_rect)
        end_rect.set_stroke(YELLOW, 2)
        end_rect.set_fill(YELLOW, 0.2)
        arrow = Arrow(start_rect.get_top(), end_rect.get_top(), path_arc=-90 * DEGREES, thickness=5)
        arrow.set_fill(border_width=1)

        frame.reorient(0, 0, 0, (-0.36, 0.97, 0.0), 7.52)
        self.play(FadeIn(sentence, UP))
        self.play(
            LaggedStartMap(DrawBorderThenFill, VGroup(start_rect, end_rect)),
            FadeIn(arrow),
        )
        self.remove(last_dials)
        self.play(LaggedStart(
            AnimationGroup(
                TransformFromCopy(start, in_text[:-1]),
                TransformFromCopy(end_rect, in_text[-1]),
                FadeIn(in_arrow)
            ),
            LaggedStart(
                (
                    block.animate.set_color(
                        block.get_color() if block is blocks[-1] else TEAL
                    ).set_anim_args(rate_func=there_and_back)
                    for block in blocks
                ),
                group=blocks,
                lag_ratio=0.1,
                run_time=1
            ),
            Animation(last_dials),
            GrowArrow(out_arrow),
            LaggedStartMap(GrowFromPoint, bar_groups, point=out_arrow.get_start()),
            lag_ratio=0.3
        ))
        self.wait()

        # Flag bad prediction
        out_rects = VGroup(
            SurroundingRectangle(bg)
            for bg in bar_groups[:2]
        )
        out_rects.set_stroke(RED, 3)
        annotations = VGroup(
            Tex(tex, font_size=60).next_to(rect, LEFT, buff=SMALL_BUFF)
            for rect, tex in zip(out_rects, [R"\uparrow", R"\downarrow"])
        )
        annotations.set_color(RED)

        self.play(
            FadeTransform(end_rect.copy(), out_rects[0]),
            Write(annotations[0]),
        )
        self.wait()
        self.play(
            FadeTransform(*out_rects),
            FadeTransform(*annotations),
        )
        self.wait()
        self.play(
            FadeOut(out_rects[1]),
            FadeOut(annotations[1]),
        )

        # Adjust
        self.play(
            LaggedStart(
                (dial.animate_set_value(dial.get_random_value())
                for dial in last_dials),
                lag_ratio=1.0 / len(last_dials),
            ),
            LaggedStart(
                (FlashAround(dial, stroke_width=2, color=YELLOW, time_width=1, buff=0.025) for dial in last_dials),
                lag_ratio=1.0 / len(last_dials),
            ),
            self.bar_group_change_animation(bar_groups[0], 70),
            self.bar_group_change_animation(bar_groups[1], 20),
            self.bar_group_change_animation(bar_groups[2], 8),
            run_time=6
        )
