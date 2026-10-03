class A:
    def __init__(self,nombre):
        self._nombre = nombre

class B(A):
    def __init__(self, nombre, edad):
        super().__init__(nombre)
        self._edad = edad

b = B('Pepe',18)
print(b.__dict__)