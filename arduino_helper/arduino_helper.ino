int pin_1 = 13;
int pin_2 = 12;
float half_period = 1000;
float phase_shift = 100;
int end = 1000;

int helper() {
  Serial.begin(9600);
  pinMode(pin_1, OUTPUT);
  pinMode(pin_2, OUTPUT);
  Serial.println(0);
  //Serial.close()
}

void setup() {
  // pin 13 set to PWM out
  helper();
  // flush remaining data from serial
  Serial.flush();
  // cli();
  // put your setup code here, to run once:
}

void loop() {
  //put your main code here, to run repeatedly:
  sei();
  if (Serial.available() > 0) {
    // received code is used as the period shift parameter
    String obj = Serial.readStringUntil('#');// Serial.read();
    int commaIndex = obj.indexOf(',');
    int hashIndex = obj.indexOf('#');

    half_period = obj.substring(0, commaIndex).toInt();
    phase_shift = obj.substring(commaIndex + 1, hashIndex).toInt();

    long incoming_code = Serial.parseInt(); Serial.read();
    Serial.println(obj);
    Serial.println(String(half_period) + " | " + String(phase_shift));
  }

  // cli();

  for (int i=0; i<end; i++)  {
    digitalWrite(pin_1, HIGH);
    delayMicroseconds(phase_shift);
    digitalWrite(pin_2, HIGH);
    delayMicroseconds(half_period - phase_shift);
    digitalWrite(pin_1, LOW);
    delayMicroseconds(phase_shift);
    digitalWrite(pin_2, LOW);
    delayMicroseconds(half_period - phase_shift);
  }
}

