#include <SPI.h>

// Use the NeoPixel library rather than through ReSpeaker
// can't include <respeaker.h> due to ISR conflict
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIXEL_PIN      11
#define NUMPIXELS      12
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

char spi_buf[64];
volatile byte spi_buf_index = 0;
volatile byte spi_event = 0;

uint32_t oncolor = pixels.Color(0,0,255);
uint32_t offcolor = pixels.Color(0,0,0);

// SPI interrupt handler
ISR (SPI_STC_vect){
  char c = SPDR;  // read SPI Data Register
  if (spi_buf_index >= sizeof(spi_buf)) {
    spi_buf_index = 0;
  }

  if ('\n' == c) {
    spi_event = 1;
    spi_buf[spi_buf_index] = '\0';
  } else {
    spi_buf[spi_buf_index] = c;
    spi_buf_index++;
  }
}


void setPixels(uint32_t c){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, c);
  }
    
  pixels.show();
}

void spi_slave_init(){
  pinMode(MOSI, INPUT);
  pinMode(MISO, OUTPUT);
  pinMode(SCK, INPUT);
  pinMode(SS, INPUT);

  // enable SPI slave mode
  SPCR |= _BV(SPE);

  SPI.attachInterrupt();
}

void setup() {
  Serial.begin(57600);
  delay(1000);

  spi_slave_init();

  pixels.begin();
  pixels.setBrightness(10);
  
  setPixels(offcolor);
}

void loop() {
  if (spi_event) {
    spi_event = 0;
    spi_buf_index = 0;
    Serial.print("spi rx:");
    Serial.println(spi_buf);

    if(strcmp(spi_buf, "on") == 0){
      setPixels(oncolor);
    }
    else if(strcmp(spi_buf, "off") == 0){
      setPixels(offcolor);
    }
  }
}
