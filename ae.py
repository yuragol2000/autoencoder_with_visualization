# (C) 2019 Griffin Bishop - http://griffinbishop.com #
# Video in action: https://gfycat.com/inconsequentialesteemeddartfrog
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model

import os



bottleneck_size = 2

input_img = Input(shape=(784,))

encoded = Dense(512, activation='relu')(input_img)
encoded = Dense(128, activation='relu')(encoded)
encoded = Dense(64, activation='relu')(encoded)
encoded = Dense(bottleneck_size, activation='linear')(encoded)
encoder = Model(input_img, encoded)


encoded_input = Input(shape=(bottleneck_size,))
decoded = Dense(64, activation='relu')(encoded_input)
decoded = Dense(128, activation='relu')(decoded)
decoded = Dense(512, activation='relu')(decoded)
decoded = Dense(784, activation='sigmoid')(decoded)
decoder = Model(encoded_input, decoded)

full = decoder(encoder(input_img))
ae = Model(input_img, full)
ae.compile(optimizer='adam', loss='mean_squared_error')


######
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32')  / 255.
x_train = x_train.reshape(x_train.shape[0], 784)
x_test = x_test.reshape(x_test.shape[0], 784)


###########
if "model.h5" in os.listdir():
    ae = load_model('model.h5')
    encoder = load_model('encoder.h5')
    decoder = load_model('decoder.h5')
else:
    ae.fit(x_train, x_train, 
        epochs = 10,
        batch_size=256,
        validation_data=(x_test, x_test))
    ae.save('model.h5')
    encoder.save('encoder.h5')
    decoder.save('decoder.h5')


encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)




fig, ax = plt.subplots(1, 2)
ax[0].scatter(encoded_imgs[:,0],encoded_imgs[:,1],
	c=y_test, s=8, cmap='tab10')


def onclick(event):
    global flag
    ix, iy = event.xdata, event.ydata
    latent_vector = np.array([[ix, iy]])
    
    decoded_img = decoder.predict(latent_vector)
    decoded_img = decoded_img.reshape(28, 28)
    ax[1].imshow(decoded_img, cmap='gray')
    plt.draw()

# button_press_event
# motion_notify_event
cid = fig.canvas.mpl_connect('motion_notify_event', onclick)



plt.show() 


