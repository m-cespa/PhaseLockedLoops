int pin_1 = 11;
float period = 1000;
float voltage = 2.5;

int helper() {
  Serial.begin(9600);
  pinMode(pin_1, OUTPUT);
 
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
  // sei();
  if (Serial.available() > 0) {
    // received code is used as the period shift parameter
    String obj = Serial.readStringUntil('#');Serial.read();Serial.read();
    int commaIndex = obj.indexOf(',');
    int hashIndex = obj.indexOf('#');

    period = obj.substring(0, commaIndex).toInt();
    voltage = obj.substring(commaIndex + 1, hashIndex).toFloat();
    
    // long incoming_code = Serial.parseInt(); Serial.read();
    Serial.println(obj);
    Serial.println(String(period) + " | " + String(voltage));
    analogWrite(pin_1, int (voltage * 255.0 / 5.0));
  }
  delay(100);
}