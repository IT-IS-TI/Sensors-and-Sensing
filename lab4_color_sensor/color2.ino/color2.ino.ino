const int redPin = 6;
const int greenPin = 5;
const int bluePin = 3;
const int sensorPin = A0;

// Calibration measurements
int redReference = 240;
int greenReference = 350;
int blueReference = 390;

void setup() {
  Serial.begin(115200);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  // Measure intensity for each color
  int redValue = measureColor(redPin);
  int greenValue = measureColor(greenPin);
  int blueValue = measureColor(bluePin);

  Serial.print("Measured R: ");
  Serial.print(redValue);
  Serial.print(" G: ");
  Serial.print(greenValue);
  Serial.print(" B: ");
  Serial.println(blueValue);

  // Recognize color
  String detectedColor = recognizeColor(redValue, greenValue, blueValue);
  Serial.print("Detected Color: ");
  Serial.println(detectedColor);

  delay(500);
}

int measureColor(int ledPin) {
  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);

  digitalWrite(ledPin, HIGH);
  delay(100); // Let the light reflect
  int value = analogRead(sensorPin);
  digitalWrite(ledPin, LOW);

  return value;
}

String recognizeColor(int r, int g, int b) {
  // Calculate squared Euclidean distances to each reference
  int distRed = sq(r - redReference) + sq(g - greenReference) + sq(b - blueReference);
  int distGreen = sq(r - greenReference) + sq(g - redReference) + sq(b - blueReference); // green dominated
  int distBlue = sq(r - blueReference) + sq(g - greenReference) + sq(b - redReference);  // blue dominated

  if (distRed <= distGreen && distRed <= distBlue) return "Red";
  else if (distGreen <= distRed && distGreen <= distBlue) return "Green";
  else return "Blue";
}
