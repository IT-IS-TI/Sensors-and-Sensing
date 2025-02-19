int sensorPin = A0;    
float sensorValue = 0;  
float alpha = 0.2;  // Smoothing factor for low-pass filter

void setup() {
  Serial.begin(115200);
}

void loop() {
  float rawValue = analogRead(sensorPin);
  sensorValue = alpha * rawValue + (1 - alpha) * sensorValue;  // Apply low-pass filter
  float weight = sensorValue * 1024 / 100;
  
  Serial.println(weight, 2);  // Print value with 2 decimal places
  delay(50);
}
