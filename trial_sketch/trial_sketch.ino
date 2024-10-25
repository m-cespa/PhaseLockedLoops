// int pin1=13;
// int pin2=12;

int helper() {
  DDRB=B110000;
  Serial.begin(9600);
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
  PORTB=B100000;
  delayMicroseconds(38);
  PORTB=B000000;
  delayMicroseconds(38);
  // put your main code here, to run repeatedly:
}


