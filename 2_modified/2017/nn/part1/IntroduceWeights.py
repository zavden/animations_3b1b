# ==============================================================================
# Scene:      IntroduceWeights
# Source:     videos/_2017/nn/part1.py (lines 2237-2617)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceWeights.py IntroduceWeights -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
#   - Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
#   - `Tex(` here is the NEW GL class (different piece splitting, 'Tex' vs 'OldTex'); the Cairo code meant TexMobject -> OldTex.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from manim_imports_ext import *
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WrappedImage(Group):
    CONFIG = {
        "rect_kwargs" : {
            "color" : BLUE,
            "buff" : SMALL_BUFF,
        }
    }
    def __init__(self, image_mobject, **kwargs):
        Group.__init__(self, **kwargs)
        rect = SurroundingRectangle(
            image_mobject, **self.rect_kwargs
        )
        self.add(rect, image_mobject)


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height" : 2,
    }
    def __init__(self, image_mobject, **kwargs):
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width = 0, 
                    fill_opacity = rgba[3]/255.0,
                    fill_color = rgba_to_color(rgba/255.0),
                )
                self.add(square)
        self.arrange_in_grid(
            *image_mobject.pixel_array.shape[:2],
            buff = 0
        )
        self.replace(image_mobject)


class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs):
        PixelsAsSquares.__init__(self,
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )


class MNistMobject(WrappedImage):
    def __init__(self, vect, **kwargs):
        WrappedImage.__init__(self, 
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )


class NetworkMobject(VGroup):
    CONFIG = {
        "neuron_radius" : 0.15,
        "neuron_to_neuron_buff" : MED_SMALL_BUFF,
        "layer_to_layer_buff" : LARGE_BUFF,
        "neuron_stroke_color" : BLUE,
        "neuron_stroke_width" : 3,
        "neuron_fill_color" : GREEN,
        "edge_color" : GREY_B,
        "edge_stroke_width" : 2,
        "edge_propogation_color" : YELLOW,
        "edge_propogation_time" : 1,
        "max_shown_neurons" : 16,
        "brace_for_large_layers" : True,
        "average_shown_activation_of_large_layer" : True,
        "include_output_labels" : False,
    }
    def __init__(self, neural_network, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.neural_network = neural_network
        self.layer_sizes = neural_network.sizes
        self.add_neurons()
        self.add_edges()

    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size)
            for size in self.layer_sizes
        ])
        layers.arrange(RIGHT, buff = self.layer_to_layer_buff)
        self.layers = layers
        self.add(self.layers)
        if self.include_output_labels:
            self.add_output_labels()

    def get_layer(self, size):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius = self.neuron_radius,
                stroke_color = self.neuron_stroke_color,
                stroke_width = self.neuron_stroke_width,
                fill_color = self.neuron_fill_color,
                fill_opacity = 0,
            )
            for x in range(n_neurons)
        ])   
        neurons.arrange(
            DOWN, buff = self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = OldTex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)

    def get_edge(self, neuron1, neuron2):
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff = self.neuron_radius,
            stroke_color = self.edge_color,
            stroke_width = self.edge_stroke_width,
        )

    def get_active_layer(self, layer_index, activation_vector):
        layer = self.layers[layer_index].deepcopy()
        self.activate_layer(layer, activation_vector)
        return layer

    def activate_layer(self, layer, activation_vector):
        n_neurons = len(layer.neurons)
        av = activation_vector
        def arr_to_num(arr):
            return (np.sum(arr > 0.1) / float(len(arr)))**(1./3)

        if len(av) > n_neurons:
            if self.average_shown_activation_of_large_layer:
                indices = np.arange(n_neurons)
                indices *= int(len(av)/n_neurons)
                indices = list(indices)
                indices.append(len(av))
                av = np.array([
                    arr_to_num(av[i1:i2])
                    for i1, i2 in zip(indices[:-1], indices[1:])
                ])
            else:
                av = np.append(
                    av[:n_neurons//2],  # CHANGE: Python 2 integer division used as an index/count -> //.
                    av[-n_neurons//2:],  # CHANGE: Python 2 integer division used as an index/count -> //.
                )
        for activation, neuron in zip(av, layer.neurons):
            neuron.set_fill(
                color = self.neuron_fill_color,
                opacity = activation
            )
        return layer

    def activate_layers(self, input_vector):
        activations = self.neural_network.get_activation_of_all_layers(input_vector)
        for activation, layer in zip(activations, self.layers):
            self.activate_layer(layer, activation)

    def deactivate_layers(self):
        all_neurons = VGroup(*it.chain(*[
            layer.neurons
            for layer in self.layers
        ]))
        all_neurons.set_fill(opacity = 0)
        return self

    def get_edge_propogation_animations(self, index):
        edge_group_copy = self.edge_groups[index].copy()
        edge_group_copy.set_stroke(
            self.edge_propogation_color,
            width = 1.5*self.edge_stroke_width
        )
        return [ShowCreationThenDestruction(
            edge_group_copy, 
            run_time = self.edge_propogation_time,
            lag_ratio = 0.5
        )]

    def add_output_labels(self):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = OldTex(str(n))
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift(neuron.get_width()*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)


class MNistNetworkMobject(NetworkMobject):
    CONFIG = {
        "neuron_to_neuron_buff" : SMALL_BUFF,
        "layer_to_layer_buff" : 1.5,
        "edge_stroke_width" : 1,
        "include_output_labels" : True,
    }

    def __init__(self, **kwargs):
        network = get_pretrained_network()
        NetworkMobject.__init__(self, network, **kwargs)


class NetworkScene(Scene):
    CONFIG = {
        "layer_sizes" : [8, 6, 6, 4],
        "network_mob_config" : {},
    }
    def setup(self):
        self.add_network()

    def add_network(self):
        self.network = Network(sizes = self.layer_sizes)
        self.network_mob = NetworkMobject(
            self.network,
            **self.network_mob_config
        )
        self.add(self.network_mob)

    def feed_forward(self, input_vector, false_confidence = False, added_anims = None):
        if added_anims is None:
            added_anims = []
        activations = self.network.get_activation_of_all_layers(
            input_vector
        )
        if false_confidence:
            i = np.argmax(activations[-1])
            activations[-1] *= 0
            activations[-1][i] = 1.0
        for i, activation in enumerate(activations):
            self.show_activation_of_layer(i, activation, added_anims)
            added_anims = []

    def show_activation_of_layer(self, layer_index, activation_vector, added_anims = None):
        if added_anims is None:
            added_anims = []
        layer = self.network_mob.layers[layer_index]
        active_layer = self.network_mob.get_active_layer(
            layer_index, activation_vector
        )
        anims = [Transform(layer, active_layer)]
        if layer_index > 0:
            anims += self.network_mob.get_edge_propogation_animations(
                layer_index-1
            )
        anims += added_anims
        self.play(*anims)

    def remove_random_edges(self, prop = 0.9):
        for edge_group in self.network_mob.edge_groups:
            for edge in list(edge_group):
                if np.random.random() < prop:
                    edge_group.remove(edge)


class PreviewMNistNetwork(NetworkScene):
    CONFIG = {
        "n_examples" : 15,
        "network_mob_config" : {},
    }
    def construct(self):
        self.remove_random_edges(0.7) #Remove?

        training_data, validation_data, test_data = load_data_wrapper()
        for data in test_data[:self.n_examples]:
            self.feed_in_image(data[0])

    def feed_in_image(self, in_vect):
        image = PixelsFromVect(in_vect)
        image.next_to(self.network_mob, LEFT, LARGE_BUFF, UP)
        image.shift_onto_screen()
        image_rect = SurroundingRectangle(image, color = BLUE)
        start_neurons = self.network_mob.layers[0].neurons.copy()
        start_neurons.set_stroke(WHITE, width = 0)
        start_neurons.set_fill(WHITE, 0)

        self.play(FadeIn(image), FadeIn(image_rect))
        self.feed_forward(in_vect, added_anims = [
            self.get_image_to_layer_one_animation(image, start_neurons)
        ])
        n = np.argmax([
            neuron.get_fill_opacity()
            for neuron in self.network_mob.layers[-1].neurons
        ])
        rect = SurroundingRectangle(VGroup(
            self.network_mob.layers[-1].neurons[n],
            self.network_mob.output_labels[n],
        ))
        self.play(ShowCreation(rect))
        self.reset_display(rect, image, image_rect)

    def reset_display(self, answer_rect, image, image_rect):
        self.play(FadeOut(answer_rect))
        self.play(
            FadeOut(image),
            FadeOut(image_rect),
            self.network_mob.deactivate_layers,
        )

    def get_image_to_layer_one_animation(self, image, start_neurons):
        image_mover = VGroup(*[
            pixel.copy()
            for pixel in image
            if pixel.fill_rgb[0] > 0.1
        ])
        return Transform(
            image_mover, start_neurons, 
            remover = True,
            run_time = 1,
        )

    ###

    def add_network(self):
        self.network_mob = MNistNetworkMobject(**self.network_mob_config)
        self.network = self.network_mob.neural_network
        self.add(self.network_mob)


class IntroduceEachLayer(PreviewMNistNetwork):
    CONFIG = {
        "network_mob_config" : {
            "neuron_stroke_color" : WHITE,
            "neuron_stroke_width" : 2,
            "neuron_fill_color" : WHITE,
            "average_shown_activation_of_large_layer" : False,
            "edge_propogation_color" : YELLOW,
            "edge_propogation_time" : 2,
        }
    }
    def construct(self):
        self.setup_network_mob()
        self.break_up_image_as_neurons()
        self.show_activation_of_one_neuron()
        self.transform_into_full_network()
        self.show_output_layer()
        self.show_hidden_layers()
        self.show_propogation()

    def setup_network_mob(self):
        self.remove(self.network_mob)

    def break_up_image_as_neurons(self):
        self.image_map = get_organized_images()
        image = self.image_map[9][0]
        image_mob = PixelsFromVect(image)
        image_mob.set_height(4)
        image_mob.next_to(ORIGIN, LEFT)
        rect = SurroundingRectangle(image_mob, color = BLUE)
        neurons = VGroup()
        for pixel in image_mob:
            pixel.set_fill(WHITE, opacity = pixel.fill_rgb[0])
            neuron = Circle(
                color = WHITE,
                stroke_width = 1,
                radius = pixel.get_width()/2
            )
            neuron.move_to(pixel)
            neuron.set_fill(WHITE, pixel.get_fill_opacity())
            neurons.add(neuron)
        neurons.scale(1.2)
        neurons.space_out_submobjects(1.3)
        neurons.to_edge(DOWN)

        braces = VGroup(*[Brace(neurons, vect) for vect in (LEFT, UP)])
        labels = VGroup(*[
            brace.get_tex("28", buff = SMALL_BUFF) 
            for brace in braces
        ])

        equation = OldTex("28", "\\times", "28", "=", "784")
        equation.next_to(neurons, RIGHT, LARGE_BUFF, UP)

        self.corner_image = MNistMobject(image)
        self.corner_image.to_corner(UP+LEFT)

        self.add(image_mob, rect)
        self.wait()
        self.play(
            ReplacementTransform(image_mob, neurons),
            FadeOut(rect),
            FadeIn(braces),
            FadeIn(labels),
        )
        self.wait()
        self.play(
            ReplacementTransform(labels[0].copy(), equation[0]),
            Write(equation[1]),
            ReplacementTransform(labels[1].copy(), equation[2]),
            Write(equation[3]),
            Write(equation[4]),
        )
        self.wait()

        self.neurons = neurons
        self.braces = braces
        self.brace_labels = labels
        self.num_pixels_equation = equation
        self.image_vect = image

    def show_activation_of_one_neuron(self):
        neurons = self.neurons
        numbers = VGroup()
        example_neuron = None
        example_num = None
        for neuron in neurons:
            o = neuron.get_fill_opacity()
            num = DecimalNumber(o, num_decimal_places = 1)
            num.set_width(0.7*neuron.get_width())
            num.move_to(neuron)
            if o > 0.8:
                num.set_fill(BLACK)
            numbers.add(num)
            if o > 0.25 and o < 0.75 and example_neuron is None:
                example_neuron = neuron
                example_num = num
                example_neuron.save_state()
                example_num.save_state()
        example_neuron.generate_target()
        example_neuron.target.set_height(1.5)
        example_neuron.target.next_to(neurons, RIGHT)
        example_num.target = DecimalNumber(
            example_neuron.get_fill_opacity()
        )
        example_num.target.move_to(example_neuron.target)

        def change_activation(num):
            self.play(
                example_neuron.set_fill, None, num,
                ChangingDecimal(
                    example_num,
                    lambda a : example_neuron.get_fill_opacity(),
                ),
                UpdateFromFunc(
                    example_num,
                    lambda m : m.set_fill(
                        BLACK if example_neuron.get_fill_opacity() > 0.8 else WHITE
                    )
                )
            )

        self.play(LaggedStartMap(FadeIn, numbers))
        self.play(
            MoveToTarget(example_neuron),
            MoveToTarget(example_num)
        )
        self.wait()
        curr_opacity = example_neuron.get_fill_opacity()
        for num in 0.3, 0.01, 1.0, curr_opacity:
            change_activation(num)
            self.wait()

        rect = SurroundingRectangle(example_num, color = YELLOW)
        activation = OldTexText("``Activation''")
        activation.next_to(example_neuron, RIGHT)
        activation.set_color(rect.get_color())
        self.play(ShowCreation(rect))
        self.play(Write(activation, run_time = 1))
        self.wait()
        change_activation(1.0)
        self.wait()
        change_activation(0.2)
        self.wait()

        self.play(
            example_neuron.restore,
            example_num.restore,
            FadeOut(activation),
            FadeOut(rect),
        )
        self.play(FadeOut(numbers))

    def transform_into_full_network(self):
        network_mob = self.network_mob
        neurons = self.neurons
        layer = network_mob.layers[0]
        layer.save_state()
        layer.rotate(np.pi/2)
        layer.center()
        layer.brace_label.rotate(-np.pi/2)
        n = network_mob.max_shown_neurons//2  # CHANGE: Python 2 integer division used as an index/count -> //.

        rows = VGroup(*[
            VGroup(*neurons[28*i:28*(i+1)])
            for i in range(28)
        ])

        self.play(
            FadeOut(self.braces),
            FadeOut(self.brace_labels),
            FadeOut(VGroup(*self.num_pixels_equation[:-1]))
        )

        self.play(rows.space_out_submobjects, 1.2)
        self.play(
            rows.arrange, RIGHT, buff = SMALL_BUFF,
            path_arc = np.pi/2,
            run_time = 2
        )
        self.play(
            ReplacementTransform(
                VGroup(*neurons[:n]), 
                VGroup(*layer.neurons[:n]),
            ),
            ReplacementTransform(
                VGroup(*neurons[n:-n]), 
                layer.dots,
            ),
            ReplacementTransform(
                VGroup(*neurons[-n:]), 
                VGroup(*layer.neurons[-n:]),
            ),
        )
        self.play(
            ReplacementTransform(
                self.num_pixels_equation[-1],
                layer.brace_label
            ),
            FadeIn(layer.brace),
        )
        self.play(layer.restore, FadeIn(self.corner_image))
        self.wait()
        for edge_group, layer in zip(network_mob.edge_groups, network_mob.layers[1:]):
            self.play(
                LaggedStartMap(FadeIn, layer, run_time = 1),
                ShowCreation(edge_group),
            )
        self.wait()

    def show_output_layer(self):
        layer = self.network_mob.layers[-1]
        labels = self.network_mob.output_labels
        rect = SurroundingRectangle(
            VGroup(layer, labels)
        )
        neuron = layer.neurons[-1]
        neuron.set_fill(WHITE, 0)
        label = labels[-1]
        for mob in neuron, label:
            mob.save_state()
            mob.generate_target()
        neuron.target.scale(4)
        neuron.target.shift(1.5*RIGHT)
        label.target.scale(1.5)
        label.target.next_to(neuron.target, RIGHT)

        activation = DecimalNumber(0)
        activation.move_to(neuron.target)

        def change_activation(num):
            self.play(
                neuron.set_fill, None, num,
                ChangingDecimal(
                    activation,
                    lambda a : neuron.get_fill_opacity(),
                ),
                UpdateFromFunc(
                    activation,
                    lambda m : m.set_fill(
                        BLACK if neuron.get_fill_opacity() > 0.8 else WHITE
                    )
                )
            )

        self.play(ShowCreation(rect))
        self.play(LaggedStartMap(FadeIn, labels))
        self.wait()
        self.play(
            MoveToTarget(neuron),
            MoveToTarget(label),
        )
        self.play(FadeIn(activation))
        for num in 0.5, 0.38, 0.97:
            change_activation(num)
            self.wait()
        self.play(
            neuron.restore,
            neuron.set_fill, None, 1,
            label.restore,
            FadeOut(activation),
            FadeOut(rect),
        )
        self.wait()

    def show_hidden_layers(self):
        hidden_layers = VGroup(*self.network_mob.layers[1:3])
        rect = SurroundingRectangle(hidden_layers, color = YELLOW)
        name = OldTexText("``Hidden layers''")
        name.next_to(rect, UP, SMALL_BUFF)
        name.set_color(YELLOW)
        q_marks = VGroup()
        for layer in hidden_layers:
            for neuron in layer.neurons:
                q_mark = OldTexText("?")
                q_mark.set_height(0.8*neuron.get_height())
                q_mark.move_to(neuron)
                q_marks.add(q_mark)
        q_marks.set_color_by_gradient(BLUE, YELLOW)
        q_mark = OldTexText("?").scale(4)
        q_mark.move_to(hidden_layers)
        q_mark.set_color(YELLOW)
        q_marks.add(q_mark)

        self.play(
            ShowCreation(rect),
            Write(name)
        )
        self.wait()
        self.play(Write(q_marks))
        self.wait()
        self.play(
            FadeOut(q_marks),
            Animation(q_marks[-1].copy())
        )

    def show_propogation(self):
        self.revert_to_original_skipping_status()
        self.remove_random_edges(0.7)
        self.feed_forward(self.image_vect)


class IntroduceWeights(IntroduceEachLayer):
    CONFIG = {
        "weights_color" : GREEN,
        "negative_weights_color" : RED,
    }
    def construct(self):
        self.zoom_in_on_one_neuron()
        self.show_desired_pixel_region()
        self.ask_about_parameters()
        self.show_weights()
        self.show_weighted_sum()
        self.organize_weights_as_grid()
        self.make_most_weights_0()
        self.add_negative_weights_around_the_edge()

    def zoom_in_on_one_neuron(self):
        self.network_mob.to_edge(LEFT)
        layers = self.network_mob.layers
        edge_groups = self.network_mob.edge_groups

        neuron = layers[1].neurons[7].deepcopy()

        self.play(
            FadeOut(edge_groups),
            FadeOut(VGroup(*layers[1:])),
            FadeOut(self.network_mob.output_labels),
            Animation(neuron),
            neuron.edges_in.set_stroke, None, 2,
            lag_ratio = 0.5,
            run_time = 2
        )

        self.neuron = neuron

    def show_desired_pixel_region(self):
        neuron = self.neuron
        d = 28

        pixels = PixelsAsSquares(ImageMobject(
            np.zeros((d, d, 4))
        ))
        pixels.set_stroke(width = 0.5)
        pixels.set_fill(WHITE, 0)
        pixels.set_height(4)
        pixels.next_to(neuron, RIGHT, LARGE_BUFF)
        rect = SurroundingRectangle(pixels, color = BLUE)

        pixels_to_detect = self.get_pixels_to_detect(pixels)

        self.play(
            FadeIn(rect),
            ShowCreation(
                pixels, 
                lag_ratio = 0.5,
                run_time = 2,
            )
        )
        self.play(
            pixels_to_detect.set_fill, WHITE, 1,
            lag_ratio = 0.5,
            run_time = 2
        )
        self.wait(2)

        self.pixels = pixels
        self.pixels_to_detect = pixels_to_detect
        self.pixels_group = VGroup(rect, pixels)

    def ask_about_parameters(self):
        pixels = self.pixels
        pixels_group = self.pixels_group
        neuron = self.neuron

        question = OldTexText("What", "parameters", "should exist?")
        parameter_word = question.get_part_by_tex("parameters")
        parameter_word.set_color(self.weights_color)
        question.move_to(neuron.edges_in.get_top(), LEFT)
        arrow = Arrow(
            parameter_word.get_bottom(),
            neuron.edges_in[0].get_center(),
            color = self.weights_color
        )

        p_labels = VGroup(*[
            OldTex("p_%d\\!:"%(i+1)).set_color(self.weights_color)
            for i in range(8)
        ] + [OldTex("\\vdots")])  # CHANGE: `Tex(` here is the NEW GL class (different piece splitting, ...
        p_labels.arrange(DOWN, aligned_edge = LEFT)
        p_labels.next_to(parameter_word, DOWN, LARGE_BUFF)
        p_labels[-1].shift(SMALL_BUFF*RIGHT)

        def get_alpha_func(i, start = 0):
            # m = int(5*np.sin(2*np.pi*i/128.))
            m = random.randint(1, 10)
            return lambda a : start + (1-2*start)*np.sin(np.pi*a*m)**2

        decimals = VGroup()
        changing_decimals = []
        for i, p_label in enumerate(p_labels[:-1]):
            decimal = DecimalNumber(0)
            decimal.next_to(p_label, RIGHT, MED_SMALL_BUFF)
            decimals.add(decimal)
            changing_decimals.append(ChangingDecimal(
                decimal, get_alpha_func(i + 5)
            ))
        for i, pixel in enumerate(pixels):
            pixel.func = get_alpha_func(i, pixel.get_fill_opacity())
        pixel_updates = [
            UpdateFromAlphaFunc(
                pixel,
                lambda p, a : p.set_fill(opacity = p.func(a))
            )
            for pixel in pixels
        ]

        self.play(
            Write(question, run_time = 2),
            GrowFromPoint(arrow, arrow.get_start()),
            pixels_group.set_height, 3,
            pixels_group.to_edge, RIGHT,
            LaggedStartMap(FadeIn, p_labels),
            LaggedStartMap(FadeIn, decimals),
        )
        self.wait()
        self.play(
            *changing_decimals + pixel_updates,
            run_time = 5,
            rate_func=linear
        )

        self.question = question
        self.weight_arrow = arrow
        self.p_labels = p_labels
        self.decimals = decimals

    def show_weights(self):
        p_labels = self.p_labels
        decimals = self.decimals
        arrow = self.weight_arrow
        question = self.question
        neuron = self.neuron
        edges = neuron.edges_in

        parameter_word = question.get_part_by_tex("parameters")
        question.remove(parameter_word)
        weights_word = OldTexText("Weights", "")[0]
        weights_word.set_color(self.weights_color)
        weights_word.move_to(parameter_word)

        w_labels = VGroup()
        for p_label in p_labels:
            w_label = OldTex(
                p_label.get_tex().replace("p", "w")
            )
            w_label.set_color(self.weights_color)
            w_label.move_to(p_label)
            w_labels.add(w_label)

        edges.generate_target()
        random_numbers = 1.5*np.random.random(len(edges))-0.5
        self.make_edges_weighted(edges.target, random_numbers)
        def get_alpha_func(r):
            return lambda a : (4*r)*a

        self.play(
            FadeOut(question),
            ReplacementTransform(parameter_word, weights_word),
            ReplacementTransform(p_labels, w_labels)
        )
        self.play(
            MoveToTarget(edges),
            *[
                ChangingDecimal(
                    decimal,
                    get_alpha_func(r)
                )
                for decimal, r in zip(decimals, random_numbers)
            ]
        )
        self.play(LaggedStartMap(
            ApplyMethod, edges,
            lambda m : (m.rotate, np.pi/24),
            rate_func = wiggle,
            run_time = 2
        ))
        self.wait()

        self.w_labels = w_labels
        self.weights_word = weights_word
        self.random_numbers = random_numbers

    def show_weighted_sum(self):
        weights_word = self.weights_word
        weight_arrow = self.weight_arrow
        w_labels = VGroup(*[
            VGroup(*label[:-1]).copy()
            for label in self.w_labels
        ])
        layer = self.network_mob.layers[0]

        a_vect = np.random.random(16)
        active_layer = self.network_mob.get_active_layer(0, a_vect)

        a_labels = VGroup(*[
            OldTex("a_%d"%d)
            for d in range(1, 5)
        ])

        weighted_sum = VGroup(*it.chain(*[
            [w, a, OldTex("+")]
            for w, a in zip(w_labels, a_labels)
        ]))
        weighted_sum.add(
            OldTex("\\cdots"),
            OldTex("+"),
            OldTex("w_n").set_color(self.weights_color),
            OldTex("a_n")
        )
        weighted_sum.arrange(RIGHT, buff = SMALL_BUFF)
        weighted_sum.to_edge(UP)

        self.play(Transform(layer, active_layer))
        self.play(
            FadeOut(weights_word),
            FadeOut(weight_arrow),
            *[
                ReplacementTransform(n.copy(), a)
                for n, a in zip(layer.neurons, a_labels)
            ] + [
                ReplacementTransform(n.copy(), weighted_sum[-4])
                for n in layer.neurons[4:-1]
            ] + [
                ReplacementTransform(
                    layer.neurons[-1].copy(), 
                    weighted_sum[-1]
                )
            ] + [
                Write(weighted_sum[i])
                for i in list(range(2, 12, 3)) + [-4, -3]
            ],
            run_time = 1.5
        )
        self.wait()
        self.play(*[
            ReplacementTransform(w1.copy(), w2)
            for w1, w2 in list(zip(self.w_labels, w_labels))[:4]  # CHANGE: Python 3: zip()/map()/filter() return iterators, wrap in list() before slicing.
        ]+[
            ReplacementTransform(w.copy(), weighted_sum[-4])
            for w in self.w_labels[4:-1]
        ]+[
            ReplacementTransform(
                self.w_labels[-1].copy(), weighted_sum[-2]
            )
        ], run_time = 2)
        self.wait(2)

        self.weighted_sum = weighted_sum

    def organize_weights_as_grid(self):
        pixels = self.pixels
        w_labels = self.w_labels
        decimals = self.decimals

        weights = 2*np.sqrt(np.random.random(784))-1
        weights[:8] = self.random_numbers[:8]
        weights[-8:] = self.random_numbers[-8:]

        weight_grid = PixelsFromVect(np.abs(weights))
        weight_grid.replace(pixels)
        weight_grid.next_to(pixels, LEFT)
        for weight, pixel in zip(weights, weight_grid):
            if weight >= 0:
                color = self.weights_color
            else:
                color = self.negative_weights_color
            pixel.set_fill(color, opacity = abs(weight))

        self.play(FadeOut(w_labels))
        self.play(
            FadeIn(
                VGroup(*weight_grid[len(decimals):]),
                lag_ratio = 0.5,
                run_time = 3
            ),
            *[
                ReplacementTransform(decimal, pixel)
                for decimal, pixel in zip(decimals, weight_grid)
            ]
        )
        self.wait()

        self.weight_grid = weight_grid

    def make_most_weights_0(self):
        weight_grid = self.weight_grid
        pixels = self.pixels
        pixels_group = self.pixels_group

        weight_grid.generate_target()
        for w, p in zip(weight_grid.target, pixels):
            if p.get_fill_opacity() > 0.1:
                w.set_fill(GREEN, 0.5)
            else:
                w.set_fill(BLACK, 0.5)
            w.set_stroke(WHITE, 0.5)

        digit = self.get_digit()
        digit.replace(pixels)

        self.play(MoveToTarget(
            weight_grid,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(Transform(
            pixels, digit,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(weight_grid.move_to, pixels)
        self.wait()
        self.play(
            ReplacementTransform(
                self.pixels_to_detect.copy(),
                self.weighted_sum,
                run_time = 3,
                lag_ratio = 0.5
            ),
            Animation(weight_grid),
        )
        self.wait()

    def add_negative_weights_around_the_edge(self):
        weight_grid = self.weight_grid
        pixels = self.pixels

        self.play(weight_grid.next_to, pixels, LEFT)
        self.play(*[
            ApplyMethod(
                weight_grid[28*y + x].set_fill, 
                self.negative_weights_color,
                0.5
            )
            for y in (6, 10)
            for x in range(14-4, 14+4)
        ])
        self.wait(2)
        self.play(weight_grid.move_to, pixels)
        self.wait(2)

    ####

    def get_digit(self):
        digit_vect = get_organized_images()[7][4]
        digit = PixelsFromVect(digit_vect)
        digit.set_stroke(width = 0.5)
        return digit

    def get_pixels_to_detect(self, pixels):
        d = int(np.sqrt(len(pixels)))
        return VGroup(*it.chain(*[
            pixels[d*n + d//2 - 4 : d*n + d//2 + 4]  # CHANGE: Python 2 integer division used as an index/count -> //.
            for n in range(7, 10)
        ]))

    def get_surrounding_pixels_for_edge(self, pixels):
        d = int(np.sqrt(len(pixels)))
        return VGroup(*it.chain(*[
            pixels[d*n + d//2 - 4 : d*n + d//2 + 4]  # CHANGE: Python 2 integer division used as an index/count -> //.
            for n in (6, 10)
        ]))

    def make_edges_weighted(self, edges, weights):
        for edge, r in zip(edges, weights):
            if r > 0:
                color = self.weights_color 
            else:
                color = self.negative_weights_color
            edge.set_stroke(color, 6*abs(r))
