const int redPin = 6;
const int greenPin = 5;
const int bluePin = 3;
const int sensorPin = A0;

void setup() {
    Serial.begin(115200);
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
}

void loop() {
    int redValue = measureColor(redPin);
    int greenValue = measureColor(greenPin);
    int blueValue = measureColor(bluePin);

    Serial.print("R: ");
    Serial.print(redValue);
    Serial.print(" G: ");
    Serial.print(greenValue);
    Serial.print(" B: ");
    Serial.println(blueValue);

    delay(100);
}

int measureColor(int ledPin) {
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, LOW);
    digitalWrite(bluePin, LOW);
    
    digitalWrite(ledPin, HIGH);
    delay(100);
    int value = analogRead(sensorPin);
    digitalWrite(ledPin, LOW);

    return value;
}
