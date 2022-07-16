
from studente import Studente
name = input("Inserisci il nome = ")
surname = input("Inserisci il cognome = ")
nuovo_allievo = Studente(name, surname)

print(nuovo_allievo.nome)
print(nuovo_allievo.cognome)
#print(dir(nuovo_allievo))