/*
  Código para o Arduino enviar dados automaticamente.
  Ele define os valores de motoId e alaId diretamente no código
  e os envia pela porta serial em um ciclo contínuo.
*/

void setup() {
  // 1. Inicia a comunicação serial
  Serial.begin(9600);

  // 2. Espera um pouco para garantir que a ponte Python esteja pronta
  delay(2000); 

  // --- DADOS A SEREM ENVIADOS UMA ÚNICA VEZ ---
  int motoId = 26; 
  int alaId = 3; 
  // ---------------------------------------------

  // 3. Monta a string
  String dataToSend = String(motoId) + "," + String(alaId);

  // 4. Envia os dados pela porta serial
  Serial.println(dataToSend);
}

void loop() {
  // A função loop fica vazia, pois não queremos que nada se repita.
}