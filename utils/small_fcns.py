from keras.models import Model
from keras.layers import Input, Deconv2D, Concatenate, GlobalAveragePooling2D
from keras.layers import Conv2D, BatchNormalization, Dense
from keras import optimizers
from keras.optimizers import SGD

class FCN:
    def __init__(self, num_channels=1024):
        self.num_channels = num_channels
        self.model = self.load()

    def load(self):
        input_parent = Input(shape=(None, None, self.num_channels), name='parent')
        input_template = Input(shape=(None, None, self.num_channels), name='template')
        input = Concatenate(axis=-1)(input_parent, input_template)
        x = Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same')(input)
        x = BatchNormalization()(x)
        x = Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = Conv2D(filters=16, kernel_size=(3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = Conv2D(filters=8, kernel_size=(3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = Conv2D(filters=4, kernel_size=(3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = Conv2D(filters=2, kernel_size=(3, 3), activation='sigmoid', padding='same')(x)
        matched_template = Conv2D(filters=1, kernel_size=(1, 1), activation='sigmoid', padding='same')(x)
        sgd = SGD(lr=0.001, momentum=0.9)
        model = Model(inputs=[input_parent, input_template], outputs=matched_template)
        model.compile(loss='binary_crossentropy', optimizer=sgd)

        return model


class IndicatorNN:
    def __init__(self, num_channels=1024):
        self.num_channels = num_channels
        self.model = self.load()

    def load(self):
        input_parent = Input(shape=(None, None, self.num_channels), name='parent')
        input_template = Input(shape=(None, None, self.num_channels), name='template')
        input = Concatenate(axis=-1)([input_parent, input_template])
        x = Dense(units=32, activation='relu')(input)
        x = BatchNormalization()(x)
        x = Dense(units=16, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dense(units=8, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dense(units=4, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dense(units=2, activation='relu')(x)
        x = BatchNormalization()(x)
        matched_template = Dense(units=1, activation='sigmoid')(x)
        sgd = SGD(lr=0.00001, momentum=0.9)
        model = Model(inputs=[input_parent, input_template], outputs=matched_template)
        model.compile(loss='binary_crossentropy', optimizer=sgd)

        return model


