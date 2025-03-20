@wireflow
def verifica_sconto(totale: float, sopra_media: bool):
	sconto: float = 0.05 * totale if totale > 800 else 0.0
	saldo_finale: float = totale - sconto
	if sopra_media and saldo_finale > 750:
		return 1
	if saldo_finale > 500:
		return 2
	return 3
@wireflow
def analizza_vendite():
	vendite_giornaliere: [float] = [150.5, 200.0, 120.25, 180.75, 250.0]
	totale_vendite: float = 0.0
	for i in range(5):
		totale_vendite += vendite_giornaliere[i]
	media_vendite: float = totale_vendite / 5
	sopra_media: bool = True
	for i in range(5):
		if vendite_giornaliere[i] <= media_vendite:
			sopra_media = False
			break
	return verifica_sconto(totale_vendite, sopra_media)
