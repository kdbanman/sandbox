/*
  Analog input, data register storage, serial output
 
 Reads an analog input pin for UltraCap voltage from the voltage divider, and
 maps the input back to the actual voltage range derived in paper documentation.
 Reads an analog input pin for Hydrogen Pressure from the pressure transducer, and
 maps the input back to the actual pressure dreived in the paper documentation.
 
 Paper documentation: http://imgur.com/a/gUoLr
 
 adapted from Tom Igoe's AnalogInOutSerial example
 24 Feb 2012
 by Kirby Banman
 
 This code is in the public domain.
 
 */


const int UltraCapInPin = A0;  // Analog input pin that the ultracap voltage divider is attached to
const int HPressureInPin = A1; // Analog input pin that the pressure transducer is attached to

int UltraCapInput = 0;          // value to be read from voltage divider
int UltraCapVoltage = 0;        // value to be read by the master board.  ACTUAL VOLTAGE IS ONE TENTH THIS VALUE

int HPressureInput = 0;         // value to be read from pressure transducer
int HPressure = 0;              // value to be read by master board.  ACTUAL PRESSURE IS ONE TENTH THIS VALUE

int data[3];

//TODO:  integrate into modbus library.

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  
  // read the analog input for UltraCap and tank pressure
  UltraCapInput = analogRead(UltraCapInPin);    
  HPressureInput = analogRead(HPressureInPin);
  
  // map ultracap voltage input, ranging from 0 (0 V) to 1023 (5 V), 
  // to the ultracap voltage in (1/10th)volts
  UltraCapVoltage = map(UltraCapInput, 0, 1023, 0, 5520);
  
  // map h pessure analog input, ranging from 204 (0.995 V) to 1023 (5 V),
  // to the tank pressure in (1/10th)psi
  HPressure = map(HPressureInput, 203, 1023, 145, 25000);
  
  // store pressure and voltage in data[] array to be read by master board
  data[1] = HPressure;
  data[2] = UltraCapVoltage;

  // print the results to the serial monitor
  // for debugging and testing, serial functions can be removed for proper function
  Serial.print("\nultra cap input = ");                       
  Serial.print(UltraCapInput);      
  Serial.print("\t ultra cap voltage = ");      
  Serial.print(UltraCapVoltage);   
  Serial.print("\t h pressure input =");
  Serial.print(HPressureInput);
  Serial.print("\t h pressure = ");
  Serial.print(HPressure);
                    
}
