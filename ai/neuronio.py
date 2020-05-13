import random
BIAS =0 

def ativacao(x):
    if x <0:
        return 0
    return x

class Neuronio():

    def __init__(self, quantidadeLigacoes=None):
        if(quantidadeLigacoes!=None):
            self.pesos = [random.randint(-1000,2000) for _ in range(0, quantidadeLigacoes)]
        else:
            self.pesos = []
        self.erro = 0
        self.saida = 1


class Camada():
    def __init__(self, qtdNeuronios, quantidadeLigacoes=None):
        self.neuronios = [Neuronio(quantidadeLigacoes) for _ in range(0, qtdNeuronios)]

    def quantidade_neuronios(self):
        return len(self.neuronios)

    def quantidadePesos(self):
        soma = 0
        for neuronio in self.neuronios:
            soma += len(neuronio.pesos)
        
        return soma

    def getSaida(self):
        saida = [] 
        for neuronio in self.neuronios:
            saida.append(neuronio.saida)

        return saida

class RedeNeural():
    def __init__(self, quantidadeEscondidas=1, qtdNeuroniosEntrada=6,
        qtdNeuroniosEscondida=tuple([6]), qtdNeuroniosSaida=3):

        qtdNeuroniosEntrada+=BIAS
        quantidadeEscondidas+=BIAS

        self.camadaEntrada = Camada(qtdNeuroniosEntrada)
        self.camadasEscondida = []
        self.camadaSaida = None

        for i in range(0, quantidadeEscondidas):
            if i ==0:
                self.camadasEscondida.append(Camada(qtdNeuroniosEscondida[i], 
                    qtdNeuroniosEntrada))
            else:
                self.camadasEscondida.append(Camada(qtdNeuroniosEscondida[i-1], 
                    qtdNeuroniosEscondida[i]))

        self.camadaSaida = Camada(qtdNeuroniosSaida, qtdNeuroniosEscondida[-1])

    def qtdEscondida(self):
        return len(self.camadasEscondida )

    def setPesos(self, pesos):
        j = 0
        for camadaEscondida in self.camadasEscondida:
            for neuronio in camadaEscondida.neuronios:
                for l in range(len(neuronio.pesos)):
                    neuronio.pesos[l] = pesos[j]
                    j+=1
        
        for neuronio in self.camadaSaida.neuronios:
            for l in range(len(neuronio.pesos)):
                neuronio.pesos[l] = pesos[j]
                j+=1

    def setEntrada(self, entrada):
        neuronios = self.camadaEntrada.neuronios
        for i in range(0, len(neuronios)):
            neuronios[i].saida = entrada[i]


    def quantidadePesos(self):
        soma = 0
        for camadaEscondida in self.camadasEscondida:
            soma += camadaEscondida.quantidadePesos()

        return soma + self.camadaSaida.quantidadePesos()

    def getSaida(self):
        return  self.camadaSaida.getSaida()

    def calcularSaida(self):
        # Calculando saidas entre a camada de entrada e a primeira camada escondida 
        for ner1 in self.camadasEscondida[0].neuronios:
            somatorio, j = 0, 0
            for nerEntrada in self.camadaEntrada.neuronios:
                somatorio += nerEntrada.saida * ner1.pesos[j]
                j+=1
            ner1.saida = ativacao(somatorio)
        
        # Calculando saidas entre a camada escondida k e a camada escondida k-1 
        for k in range(1,len(self.camadasEscondida)):
            for neuronio1 in self.camadasEscondida[k]:
                somatorio, j = 0, 0
                for neuronio2 in self.camadasEscondida[k-1]:
                    somatorio += neuronio2.saida * neuronio1.pesos[j]
                    j+=1
                neuronio1 = ativacao(somatorio)
        
        #Calculando saidas entre a camada de saida e a ultima camada escondida 
        for nerSaida in self.camadaSaida.neuronios:
            somatorio, j = 0, 0
            for ner in self.camadasEscondida[-1].neuronios:
                somatorio += ner.saida * nerSaida.pesos[j]
                j+=1
            nerSaida.saida = ativacao(somatorio)