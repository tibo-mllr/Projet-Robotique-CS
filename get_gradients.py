import tensorflow as tf
import tensorflow.keras as keras
import numpy as np


@tf.function
def gradients(function, inputs):

    with tf.GradientTape() as grad_tape:

        grad_tape.watch(inputs)

        output = function(inputs)

    grads = grad_tape.gradient(output, inputs)

    return grads


if __name__ == '__main__':

    def fun(x):

        return tf.stack([2*x[0, 0] + 3*x[0, 1] - 2*x[1, 0]**2 - 3*x[1, 1], x[0, 0]**2 + 3*x[0, 1] - x[1, 0]**2 - x[1, 1]])

    print(gradients(fun, tf.constant([[3, 4], [4, 1]], dtype=tf.float32)))
