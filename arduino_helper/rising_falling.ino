int pin_1 = 13;
int pin_2 = 12;

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
  // put your main code here, to run repeatedly:
  digitalWrite(pin_1, HIGH);
  delayMicroseconds(1000);
  digitalWrite(pin_1, LOW);
  delayMicroseconds(1000);
  digitalWrite(pin_1, HIGH);
  delayMicroseconds(1000);
  digitalWrite(pin_1, LOW);
  delayMicroseconds(1000);
  digitalWrite(pin_2, HIGH);
  delayMicroseconds(1000);
  digitalWrite(pin_2, LOW);
  delayMicroseconds(1000);
  digitalWrite(pin_2, HIGH);
  delayMicroseconds(1000);
  digitalWrite(pin_2, LOW);
  delayMicroseconds(1000);
}
