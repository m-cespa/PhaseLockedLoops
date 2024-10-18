int pin_1 = 13;
int pin_2 = 12;
int half_period = 100;
int phase_shift = 10;

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
  cli();
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // received code is used as the period shift parameter
    String obj = Serial.readStringUntil('#'); Serial.read();
    int commaIndex = obj.indexOf(',');
    int hashIndex = obj.indexOf('#');

    half_period = obj.substring(0, commaIndex).toInt();
    phase_shift = obj.substring(commaIndex + 1, hashIndex).toInt();

    // long incoming_code = Serial.parseInt(); Serial.read();
  }
  digitalWrite(pin_1, HIGH);
  delayMicroseconds(phase_shift);
  digitalWrite(pin_2, HIGH);
  delayMicroseconds(half_period - phase_shift);
  digitalWrite(pin_1, LOW);
  delayMicroseconds(phase_shift);
  digitalWrite(pin_2, LOW);
  delayMicroseconds(half_period - phase_shift);
}
