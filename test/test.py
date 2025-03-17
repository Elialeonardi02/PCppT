@wireflow
def aggiorna_parametri():
	base: int = 10        # Dichiarazione con type hint e inizializzazione
	incremento: float     # Dichiarazione senza inizializzazione (valore assegnato dopo)
	incremento = 2.5      # Assegnazione separata con inferenza di tipo
	risultato = base * incremento  # Inferenza di tipo (float)

	fattori: [int] = [1, 2, 3]      # Array con inferenza della dimensione
	pesi: [float, 3] = [0.5, 1.5, 2.0]  # Array con dimensione esplicita

	base += 5        # Assegnazione composta valida
	risultato /= 2   # Assegnazione composta valida

	return risultato  # Restituisce un singolo valore