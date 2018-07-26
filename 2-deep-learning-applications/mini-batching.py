from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

n_input = 784
n_classes = 10

mnist = input_data.read_data('/datasets/ud730/mnist', one_hot=True)
train_features = mnist.train.images
test_features = mnist.test.images

train_labels = mnist.train.labels.astype(np.float32)
test_labels = mnist.test.labels.astype(np.float32)

weights = tf.Variable(tf.random_normal([n_input, n_classes]))
bias = tf.Variable(tf.zeros([n_classes]))
