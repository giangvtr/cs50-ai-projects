# CNN Architecture comparison results
## Initial model, a very simple CNN
I started off with a network with only 1 convolutional layer and one dense hidden layer. All of them using reLu as activation function.

Result: `Accuracy 0.0558 — Loss: 3.5031`, meaning that there are a lot of things could be improved here. 

First of all, the model was too shallow for an image network to extract meaningful patterns. The model is extremely underfitting
```python
    model = tf.keras.models.Sequential([
        # 1st layer
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # Max-pooling layer, using 2x2 pool size
        # Downsamples the image
        tf.keras.layers.MaxPooling2D(2, 2),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # The output layer
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='relu'),
    ])
```

## Adding depth (3 convolutional layers)
Here I added 2 more layers, so now we have in total 3 layers. The network depth is increased to extract higher-level features.
The number of filters is gradually increased for each layer (32-64-128).

I was happy with the new result, with 97,05 % accuracy.
But I wanted to experiment a bit, so I carried on my small experiment.

Result: `accuracy: 0.9705 - loss: 0.1154`

## Fewer layers and more aggressive pooling
As you can see in this model, the pooling size was indeed increased for each layer, meaning stronger downsampling. 
The network is more likely to filter out important details at the very first stage of the convolution.

Result: Accuracy: 0.9161 — Loss: 0.2978

```python
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # Max-pooling layer, using 2x2 pool size
        # Downsamples the image
        tf.keras.layers.MaxPooling2D(3, 3),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((3, 3)),

```

## Another pooling strategy

Here I tried reducing pooling strength gradually (3 → 2 → 1). The final layer uses (1,1) pooling, meaning no downsampling.

Result: `Accuracy: 0.9161 — Loss: 0.2978`

```python
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # Max-pooling layer, using 2x2 pool size
        # Downsamples the image
        tf.keras.layers.MaxPooling2D(3, 3),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((1, 1)),

```

## Reducing dropout to 0.1
I put back to the best network, where I had gained 97% in accuracy. I changed to drop-out rate to 0.1 only, 
hoping that the network will learn more expressive features. 

However it didn't turn out the way I have expected, the accuracy drop and the training took longer. The model was
likely overfitted faster due to less regularization.

Result: `accuracy: 0.8090 - loss: 0.7991`

## Increasing dropout to 0.9
This indeed, turned out as I would predict. The accuracy collapsed back to the level of a random classifier. The model 
cannot learn useful features when almost all neurons are dropped.

Result : `accuracy: 0.0576 - loss: 3.5058`

