from sklearn.neural_network import MLPClassifier

class MLPClassifierOverride(MLPClassifier):

    # Overriding _init_coef method
    def _init_coef(self, fan_in, fan_out):
        coef_init, intercept_init = super._init_coef(self, fan_in, fan_out)
        # if self.activation == 'logistic':
        #     init_bound = np.sqrt(2. / (fan_in + fan_out))
        # elif self.activation in ('identity', 'tanh', 'relu'):
        #     init_bound = np.sqrt(6. / (fan_in + fan_out))
        # else:
        #     raise ValueError("Unknown activation function %s" %
        #                     self.activation)
        # coef_init = ### place your initial values for coef_init here

        # intercept_init = ### place your initial values for intercept_init here
        print(coef_init, intercept_init)
        return coef_init, intercept_init