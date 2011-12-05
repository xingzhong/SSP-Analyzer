import numpy as np
class RN:
    def __init__(self, deg):
        self.net = {}
        self.deg = deg
        self.theta = 0.5

    def addNet(self, name):
        initNet = np.zeros(self.deg)
        initNet[0] = 1
        initNet[1] = -1
        if not self.net.has_key(name):
            self.net[name] = initNet
        if name in ['ArraySubscriptExpr']:
            self.net[name] = np.zeros(self.deg)
            self.net[name][0] = -1
            self.net[name][1] = 1
        if name.endswith("Stmt") or name in ['root']:
            self.net[name] = np.ones(self.deg)

    def forward(self, input, type):
        #input should be feature vectors
        #make sure weight and input have equal length
        weight = self.net[type]
        d =  sum(input[i]*weight[i] for i in range(len(input)))
        output = self.sigmoid(d + self.theta)
        return output

    def sigmoid(self, x):
        a = 1.0
        return 1.0/(1.0 + np.exp(-a*x))

    def training(self, tree):
        print "Start training ..."
        print "Input "
        for i in tree.input:
            print i, tree.input[i]
        print "Desired Output"
        dout = tree.input['y']
        print dout
        print "Output"
        output = tree.forward()
        print output
        self.error(output, dout)

    def error(self, real, desire):
        diff = real - desire
        print diff

    def debug(self):
        for i in self.net.items():
            print i
