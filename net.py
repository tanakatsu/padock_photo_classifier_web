import chainer
import chainer.functions as F
import chainer.links as L


class CNN(chainer.Chain):

    def __init__(self, outputSize=1, train=True):
        # initializer = chainer.initializers.GlorotNormal()
        initializer = chainer.initializers.HeNormal()
        super(CNN, self).__init__(
            conv1=L.Convolution2D(3, 32, 3, initialW=initializer),
            conv2=L.Convolution2D(32, 64, 3, initialW=initializer),
            conv3=L.Convolution2D(64, 128, 3, initialW=initializer),
            l1=L.Linear(None, 800, initialW=initializer),
            l2=L.Linear(800, 400, initialW=initializer),
            l3=L.Linear(400, outputSize, initialW=initializer),
        )
        self.train = train

    def __call__(self, x):
        h = F.max_pooling_2d(F.relu(self.conv1(x)), 2)
        h = F.relu(self.conv2(h))
        h = F.max_pooling_2d(F.relu(self.conv3(h)), 2)
        h = F.dropout(F.relu(self.l1(h)), train=self.train)
        h = F.dropout(F.relu(self.l2(h)), train=self.train)
        y = self.l3(h)
        return y
