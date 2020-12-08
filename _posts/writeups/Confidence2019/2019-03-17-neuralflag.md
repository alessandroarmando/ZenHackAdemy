---
author: zangobot
ctf: Confidence 2019
challenge: neural flag
categories: [advml]
tags: [ ctf, challenge, write-up, machine learning, adversarial ]
layout: writeup
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>

Another week, another neural CTF to pwn!

We have a model of a pre-trained neural network. This model recognizes the flag as class 1, while everything else is 0.
As already discussed in the previous write-up (that you can [find here](/advml/2019/03/10/facesafe.html)), we may use the gradient of the model to navigate the input space.

But, surprise surprise, things are different!

The model has been trained on lot of data that seems the flag but they aren't.
It is a naive implementation of [Adversarial retraining](https://arxiv.org/pdf/1702.06280.pdf), as the developer adds well-crafted noise to teach the network how ad adversarial examples is made.

Hence, in theory the output model should be more robust w.r.t. an aware attacker... but in practice this defence is useless!
An attacker can still navigate the output space with gradients AND an attacker may still find portion of space full of adversarial examples that are not being taken into account by the retraining (and they may be A LOT).

The provided network takes in input a 50 x 11 image and returns ```[1 ,0]``` or ```[0, 1]```: the latter is the target class we want to obtain.
Hence, we may use a black image and see how the gradient toward that class modifies the input.

**BUT THE GRADIENT IS ALWAYS ZERO!**

If you try just to compute the gradient of the output neuron w.r.t. the input, you'll find nothing but a bunchesof zeros.
Why????

Because of the naive adversarial retraining above! All around the flag, everything is "forced" to drop to zero.
It's like being stuck on a flat field, you cannot even see the mountains from there!
In addition, the ```softmax``` function saturates. Let's dig into this.

The softmax function is defined as:

$$
\sigma(x) = \frac{e^x}{\sum_{j=1}^d e^{x_j}}
$$

while its derivative, w.r.t. each entry can be written as:

$$
\frac{\partial \sigma}{\partial x_i}(x_j) = -\sigma(x_j)\sigma(x_i)
\\
\frac{\partial \sigma}{\partial x_i}(x_i) = \sigma(x_i)(1 - \sigma(x_i))
$$

So, it is clear that, if $$\sigma(x_i)$$ is very low, then $$\sigma(x_j)$$ is very close to 1 (because the resulting vector sums up to 1), and viceversa.
The resulting vector is zero, and the model believes that is a local / absolute minimum or maximum.
So, we are stuck in a 0-gradient region: it's like a sail boat that tries to navigate without any wind!

So, how can we explore the space?
We can get rid of the output neuron and check the gradient of the second-last layer, that is a fully connected layer!
The vector that we obtain is, by construction of the network, a direction $$g \in \mathbb{R}^{550}$$, where 550 is just the total number of pixels.
How can I use this long vector?

Remember that the gradient is the direction of maximum ascent.
So, if I compute the gradient of a sample that is labelled as ```[1, 0]```, the gradient will point to direction that increses the first component.
On the other hand, by flipping the sign, we will ride the direciton that decreases the first component.
As a consequence, following this direciton will increase the second component: **we have out direction towards the target class!**

**BUT APPLYING THE Fast Sign Gradient Method (FSGM) IT IS NOT ENOUGH (see previous write-up for attack details)!**

The FSGM attack perturbs mostly all the pixels of the image, because of the sign applied to the gradient.
If you barely apply FSGM, you'll obtain a useless image, still classified as ```[0, 1]```.
How to overcome this problem?
*Just remove the sign from the formula*. Problem solved.

The flag will appear from the input image you'll provide!

And this is the python code for doing this trick!

```python
import numpy as np
import keras
from keras.models import load_model
import keras.backend as K
import matplotlib.pyplot as plt
import os

features = 50*11

x0 = np.ones((1, 11, 50), dtype=float)*100
model = load_model('model2.h5')

eps = 1
target = np.array([0, 1])

#If you want to find the 0 gradient, just plug this loss inside the derivative.
loss = keras.losses.categorical_crossentropy(target, model.output)

# Gradient wrt to last dense layer! Why?
# Because the softmax flattens everything to zero (try and see, just swap the definitions)

session = K.get_session()
d_model_d_x = K.gradients(model.layers[2].output, model.input)
# d_model_d_x = K.gradients(model.output, model.input)

prediction = model.predict(x0)
while np.argmax(prediction) != 1:

    # Thank you Keras + Tensorflow!
    # That [0][0] is just ugly, but it is needed to obtain the value as an array.
    eval_grad = session.run(d_model_d_x, feed_dict={model.input: x0})
    eval_grad = eval_grad[0][0]

    # We don't need to cap the sign, hence, we need to craft the flag point.
    # The FSGM resude uniformly the image in general, because it flattens the gradient to barely +/-1.
    # We need pixels to be modified according to the value of the gradient in their position.
    fsgm = eps * eval_grad

    # The gradient always points to maximum ascent direction, but we need to minimize.
    # Hence, we swap the sign of the gradient.
    x0 = x0 - fsgm

    # We do not need to clip, as we don't need to save the result as a regular image.
    prediction = model.predict(x0)
    print(prediction)

# I will rescale the output for visualization purpouses.
plt.imshow(x0[0] / np.max(x0[0]) - np.min(x0[0]))
plt.show()
```
The flag is `p4{nn_is_ez}`

You can find all the code [just HERE](/assets/writeups/Confidence2019/neuralflag/neuralflag.zip), with the code above and the model.
