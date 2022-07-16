class Studente:
    def __init__(self,nome,cognome,eta):
        self.n = nome
        self.g = cognome
        self.e = eta

primo_Studente = Studente("Giovanni","Rossi", 20)
secondo_Studente = Studente("Mario","Draghi", 22)

if (primo_Studente.e == secondo_Studente.e):
    print(f'{primo_Studente.n} è coetaneo {secondo_Studente.n} ')
else:
    print(f'{primo_Studente.n} è NON coetaneo {secondo_Studente.n} ')