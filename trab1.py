import math
class Except(Exception):
    pass

class Trem:
    def __init__(self, N):
        self._N = N
        self._data = [None]*N
        self._front = 0
        self._top = 0
        self._ptr = 0
        self._size = 0
    

    def __str__(self):
        if self.is_empty():
            return 'trem vazio'
        else:
            lista_temp = []
            strSize = 0
            self.rewind()
            while strSize < self._size:
                lista_temp.append(self.next())
                strSize += 1
            return str(lista_temp)
    

    def get_size(self):
        return self._size
    

    def rewind(self):
        self._ptr = self._front
    

    def next(self):
        if self.is_empty():
            return None
        else:
            e = self._data[self._ptr]
            self._ptr += 1
            if self._ptr==self._N:
                self._ptr = 0
            return e
    

    def getVC(self): #Get vetor circular com elementos do deque circulando
        if self.is_empty():
            return 'Vetor vazio'
        else:
            return self._data
    

    def is_empty(self):
        return self._size==0
    

    def is_full(self):
        return self._size == self._N
    

    def add_first(self, e):
        if self.is_full():
            raise Except('Trem cheio!')
        if self.is_empty():
            self._data[self._front] = e
        else:
            self._front -= 1
            if self._front == -1:
                self._front = self._N - 1
            self._data[self._front] = e
        self._size +=1
    

    def add_last(self, e):
        if self.is_full():
            raise Except('Trem cheio!')
        elif self.is_empty():
            self._data[self._front] = e
        else:
            self._top += 1
            if self._top == self._N:
                self._top = 0
            self._data[self._top] = e
        self._size +=1
    

    def delete_first(self):
        if self.is_empty():
            raise Except('Trem vazio!')
        else:
            e_front = self._data[self._front]
            self._data[self._front] = None
            self._size -= 1
            self._front += 1
            if self._front == self._N:
                self._front = 0
            return e_front
    

    def delete_last(self):
        if self.is_empty():
            raise Except('Trem vazio!')
        else:
            e_top = self._data[self._top]
            self._data[self._top] = None
            self._size -= 1
            self._top -= 1
            if self._top == -1:
                self._top = 0
            return e_top
    

    def first(self):
        if self.is_empty():
            return None
        else:
            return self._data[self._front]
    

    def last(self):
        if self.is_empty():
            return None
        else:
            return self._data[self._top]
    

    def get_peso_total(self):
        peso_total = 0
        vagoes = self.getVC()
        for vagao in vagoes:
            if vagao is not None:
                peso_total += vagao.peso
        if peso_total > 0:
            return peso_total
        else:
            raise RuntimeError('Peso do vagão igual a 0')
    

    def get_potencia_total(self):
        pot_total = 0
        locomotivas = [loc for loc in self.getVC() if isinstance(loc, Locomotiva)]
        for loc in locomotivas:
            pot_total += loc.pot
        if pot_total > 0:
            return pot_total
        else:
            raise RuntimeError(f'Potencia total tem que ser maior que 0\nPotencia total: {pot_total}')


    def check_potencia(self):
        peso_total = self.get_peso_total()
        pot_total = self.get_potencia_total()
        pot_loc = [loc for loc in self.getVC() if isinstance(loc, Locomotiva)][0].pot
        pot_aceitavel = peso_total * 1.05
        if pot_aceitavel > pot_total:
            #Potencia não é o suficiente
            pot_faltante = pot_aceitavel - pot_total
            n_locs = math.ceil(pot_faltante/pot_loc)
            return f'A Potencia está abaixo do necessario.\nPotencia faltante: {pot_faltante}\nPrecisa-se adicionar {n_locs} locomotivas.'
        else:
            return f'Potencia total ({pot_total}) é acima da potencia necessaria\nPotencia disponivel: {pot_total - pot_aceitavel}'
    

    def check_lenght(self):
        train = self.getVC()
        locs = []
        vagsPass = []
        vagsCarg = []
        for i in train:
            if isinstance(i, Locomotiva):
                locs.append(i)
            elif isinstance(i, VagPass):
                vagsPass.append(i)
            elif isinstance(i, VagCarga):
                vagsCarg.append(i)
        
        total_lenght = (2* (len(train) - 1)) + (20 * len(locs)) + (15 * len(vagsPass)) + (18 * len(vagsCarg))
        if total_lenght < 0:
            raise RuntimeError('Tamanho da locomotiva tem que ser maior que 0')
        return f'O tamanho da locomotiva é: {total_lenght} m'


    def check_pass(self):
        vagoes_pass = [pas for pas in self.getVC() if isinstance(pas, VagPass)]
        passags = 0
        for vagao in vagoes_pass:
            passags += vagao.passags
        return passags
    

    def check_load(self):
        vagoes_carga = [carg for carg in self.getVC() if isinstance(carg, VagCarga)]
        total_load = 0
        for vagao in vagoes_carga:
            total_load += vagao.carga
        return total_load


class Locomotiva:
    def __init__(self, peso):
        self.comprimento = 20.0
        if peso <100 or peso > 200:
            raise RuntimeError('Peso da locomotiva não pode ser menor do que 100 ou maior do que 200')
        self.peso = peso
        self.pot = 80.0*peso - 6000 #Regressão linear para pegar valor equivalente ao peso


class VagPass:
    def __init__(self, peso: float, passags: int):
        self.comprimento = 15.0
        peso_total = peso + passags*0.088 #Calculando peso total em toneladas
        if passags > 30:
            raise RuntimeError(f'Numero de passageiros não pode ser maior que 30.\nNumero de passageiros: {passags}')
        if peso_total <30 or peso_total >50:
            raise RuntimeError(f'Peso do vagão não pode ser menor do que 30 ou maior do que 50.\nPeso: {peso_total}')
        self.passags = passags
        self.peso = peso_total


class VagCarga:
    def __init__(self, peso):
        self.comprimento = 18.0
        if peso < 80 or peso > 100:
            raise RuntimeError(f'Peso total do vagão de carga não pode ser menor do que 80 ou maior do que 100\nPeso total: {peso}')
        self.peso = peso*0.25
        self.carga = peso*0.75
