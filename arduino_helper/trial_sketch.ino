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
<<<<<<< HEAD
  delayMicroseconds(38);
  PORTB=B000000;
  delayMicroseconds(38);
=======
  delay(1);
  PORTB=B110000;
  delay(0);
  PORTB=B010000;
  delay(1);
  PORTB=B000000;
  delay(0);
>>>>>>> 4e411aa5c2c5d211717e09f37d30ad40a5811aa1
  // put your main code here, to run repeatedly:
}


