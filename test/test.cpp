int verifica_sconto(float totale, bool sopra_media)
{
  float sconto = (totale > 800 ? 0.05 * totale : 0.0);
  float saldo_finale = totale - sconto;
  if (sopra_media && saldo_finale > 750) {
    return 1;
  }
  if (saldo_finale > 500) {
    return 2;
  }
  return 3;
}

int analizza_vendite()
{
  float vendite_giornaliere[] = {150.5f, 200.0f, 120.25f, 180.75f, 250.0f};
  float totale_vendite = 0.0;
  for (char i = 0; i < 5; ++i) {
    totale_vendite += vendite_giornaliere[i];
  }
  float media_vendite = totale_vendite / 5;
  bool sopra_media = true;
  for (char i = 0; i < 5; ++i) {
    if (vendite_giornaliere[i] <= media_vendite) {
      sopra_media = false;
      break;
    }
  }
  return verifica_sconto(totale_vendite, sopra_media);
}

