# ==============================================================================
# Scene:      MoreHonestMNistNetworkPreview
# Source:     videos/_2017/nn/part1.py (lines 1400-1437)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MoreHonestMNistNetworkPreview.py MoreHonestMNistNetworkPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
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


class MoreHonestMNistNetworkPreview(IntroduceEachLayer):
    CONFIG = {
        "network_mob_config" : {
            "edge_propogation_time" : 1.5,
        }
    }
    def construct(self):
        PreviewMNistNetwork.construct(self)

    def get_image_to_layer_one_animation(self, image, start_neurons):
        neurons = VGroup()
        for pixel in image:
            neuron = Circle(
                radius = pixel.get_width()/2,
                stroke_width = 1,
                stroke_color = WHITE,
                fill_color = WHITE,
                fill_opacity = pixel.fill_rgb[0]
            )
            neuron.move_to(pixel)
            neurons.add(neuron)
        neurons.scale(1.2)
        neurons.next_to(image, DOWN)
        n = len(start_neurons)
        point = VectorizedPoint(start_neurons.get_center())
        target = VGroup(*it.chain(
            start_neurons[:n//2],  # CHANGE: Python 2 integer division used as an index/count -> //.
            [point.copy() for x in range(len(neurons)-n)],
            start_neurons[n//2:],  # CHANGE: Python 2 integer division used as an index/count -> //.
        ))
        mover = image.copy()
        self.play(Transform(mover, neurons))
        return Transform(
            mover, target, 
            run_time = 2,
            lag_ratio = 0.5,
            remover = True
        )
