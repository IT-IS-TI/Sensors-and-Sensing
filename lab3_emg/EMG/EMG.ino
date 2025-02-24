const int emgPin = A0;  // EMG sensor connected to Analog pin A0
const int numSamples = 10;  // Number of samples for moving average filter
int readings[numSamples];    
int readIndex = 0;
int total = 0;
int average = 0;

// High-pass filter (50 Hz)
float hp_alpha = 0.95; // Adjust filter strength
float hp_prev = 0, hp_filtered = 0;

// Low-pass filter (200 Hz)
float lp_alpha = 0.2; // Adjust for smoothing
float lp_prev = 0, bp_filtered = 0;

void setup() {
    Serial.begin(115200);
    pinMode(emgPin, INPUT);

    for (int i = 0; i < numSamples; i++) {
        readings[i] = 0;
    }
}

void loop() {
    // Read raw EMG signal
    int rawValue = analogRead(emgPin);
    
    // Ignore noise below threshold
    if (rawValue < 70) rawValue = 0;
    
    // Convert to float
    float emgValue = (float)rawValue;

    // Apply High-pass filter (50 Hz)
    hp_filtered = hp_alpha * (hp_prev + emgValue - hp_prev);
    hp_prev = emgValue;

    // Apply Low-pass filter (200 Hz) to form Bandpass (50-200 Hz)
    bp_filtered = lp_alpha * hp_filtered + (1 - lp_alpha) * lp_prev;
    lp_prev = bp_filtered;

    // Moving average filter for noise reduction
    total = total - readings[readIndex]; // Remove oldest reading
    readings[readIndex] = (int)bp_filtered;  // Store new reading
    total = total + readings[readIndex]; // Add the new reading
    readIndex = (readIndex + 1) % numSamples; // Move index forward

    // Compute the final filtered output
    average = total / numSamples;

    // Print both raw and filtered values
    Serial.print("Raw: ");
    Serial.print(rawValue);
    Serial.print("  Filtered: ");
    Serial.println(average);

    delay(10); // Adjust based on signal needs
}
