# -*- coding: utf-8 -*-
"""8.1ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wvgkGidDK0z6y8b87RcFET50QfwFHvT6
"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Layer, Activation
from keras.datasets import mnist
from keras import backend as K
from keras.utils import np_utils
import tensorflow as tf

class Antirectifier(Layer):
   #Это комбинация выборочного
#Нормализация L2 с объединением
#положительной части входных данных с отрицательной частью
#из входных данных. Результатом является тензор выборок, которые
#в два раза больше входных выборок.

#Его можно использовать вместо холодильника.

# Форма ввода
#2D тензор формы (выборок, n)

# Форма вывода
#2D тензор формы (выборки, 2*n)

# Теоретическое обоснование
#При применении ReLU, предполагая, что распределение
#значение предыдущего вывода приблизительно сосредоточено вокруг 0.,
#вы отбрасываете половину своих входных данных. Это неэффективно.

#Анти-выпрямитель позволяет возвращать все положительные выходные сигналы, такие как ReLU,
#без отбрасывания каких-либо данных.

#Тесты на MNIST показывают, что анти-выпрямитель позволяет обучать сети
#с вдвое меньшими параметрами, но с сопоставимыми
#точность классификации в качестве эквивалентной сети на основе ReLU.


    def compute_output_shape(self, input_shape):
        shape = list(input_shape) #входные-список
        assert len(shape) == 2  # only valid for 2D tensors
        shape[-1] *= 2
        return tuple(shape) # возвращает кортеж

    def call(self, inputs):
        inputs -= K.mean(inputs, axis=1, keepdims=True)
        inputs = K.l2_normalize(inputs, axis=1)
        pos = K.relu(inputs)
        neg = K.relu(-inputs)
        return K.concatenate([pos, neg], axis=1)

# global parameters
batch_size = 128
nb_classes = 10
nb_epoch = 10

# the data, shuffled and split between train and test sets - данные перетасованы и разделенны между наборами train и test
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)   #Придает новую форму массиву без изменения его данных
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices -преобразование векторов классов в двоичные матрицы
Y_train = np_utils.to_categorical(y_train, nb_classes)   #Преобразует вектор класса (целые числа) в бинарную матрицу класса
Y_test = np_utils.to_categorical(y_test, nb_classes)

# build the model
model = Sequential()
model.add(Dense(256, input_shape=(784,)))
model.add(Antirectifier())
model.add(Dropout(0.1)) # метод борьбы с переобучением нейронной сети,процент отсеиваемых нейтронов
model.add(Dense(256)) #размерность выходного пространства 
model.add(Antirectifier())
model.add(Dropout(0.1)) # метод борьбы с переобучением нейронной сети,процент отсеиваемых нейтронов 
model.add(Dense(10))
model.add(Activation('softmax'))  #Softmax преобразует вектор значений в распределение вероятностей

# compile the model #компилируем модель
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# train the model      #обучаем модель
model.fit(X_train, Y_train,
          batch_size=batch_size, epochs=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))

tf.keras.utils.plot_model(model, show_shapes=True, dpi=64) # Преобразует модель Keras в точечный формат и сохраняет в файл.