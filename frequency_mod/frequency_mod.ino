int pin = 13;
float half_period = 1000;
int end = 1000;

int helper() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin, OUTPUT);
  Serial.println(0);
}

void setup() {
  helper();
  Serial.flush();
}

void loop() {
  // put your main code here, to run repeatedly:
  sei();
  if (Serial.available() > 0) {
    String obj = Serial.readStringUntil('#');Serial.read();Serial.read();
    int hashIndex = obj.indexOf('#');

    half_period = obj.substring(0, hashIndex).toFloat();
    
    Serial.println(String(obj));
  }

  for (int i=0; i<end; i++) {
    digitalWrite(pin, LOW);
    delayMicroseconds(half_period);
    digitalWrite(pin, HIGH);
    delayMicroseconds(half_period);
  }
}
