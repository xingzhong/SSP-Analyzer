import numpy as np
class RN:
    def __init__(self, deg):
        self.net = {}
        self.deg = deg
        self.theta = 0.5
        self.lam = 0.2 #learning rate
        

    def addNet(self, name):
        initNet = np.ones(self.deg)
        if not self.net.has_key(name):
            self.net[name] = initNet

    def forward(self, input, type):
        #input should be feature vectors
        #make sure weight and input have equal length
        weight = self.net[type]
        num = input.shape[1]
        w = np.matrix(weight[:num]).getT()
        d = input * w 
        d = np.squeeze(np.asarray(d))
        output = self.sigmoid(d + self.theta)
        return output

    def sigmoid(self, x):
        a = 1.0
        return 1.0/(1.0 + np.exp(-a*x))

    def training(self, tree):
        self.tree = tree
        output = tree.forward()
        self.training_1(self.tree.root, output - self.tree.input['y'])
    
    def training_1(self, node, err):
        type = self.tree.net.node[node]['kind']
        z = self.tree.net.node[node]['feature']
        error = z * (1-z) * err
        dthe = self.lam * error
        dw = dthe * self.get_input(node)
        dw = np.squeeze(np.asarray(dw))
        dw = np.array(dw, ndmin=1)
        weight = self.net[type]
        self.updateWeight(node, dw)
        succ = self.tree.get_succ(node)
        for i in range(len(succ)):
            n = succ[i]
            w = weight[i]
            if self.tree.net.out_degree(n) > 0:
                self.training_1(n, w*error)

    
    def updateWeight(self, node, dw):
        type = self.tree.net.node[node]['kind']
        print type, dw, self.net[type]
        for i in range(len(dw)):
            self.net[type][i] = self.net[type][i] + dw[i]

    def error(self, real, desire):
        diff = real * (1-real) * (real - desire)
        dtheta = self.lam * diff
        return dtheta

    def get_input(self, node): #get input data vector for one node
        x = np.matrix( map(lambda x: self.tree.net.node[x]['feature'],\
                self.tree.get_succ(node)) ).getT()
        return x

    def debug(self):
        for i in self.net.items():
            print i
