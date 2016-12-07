#include <msp430.h>

#include <stdio.h>
#include <stdlib.h>

#include "tutorial.pb-c.h"

int main (int argc, const char * argv[]) 
{
  
  Tutorial__Person testPerson = TUTORIAL__PERSON__INIT;  // AMessage
  void *buf;                     // Buffer to store serialized data
  unsigned len;                  // Length of serialized data

  testPerson.has_id = 1;
  testPerson.id = 1;

  len = tutorial__person__get_packed_size(&testPerson);
  buf = malloc(len);
  tutorial__person__pack(&testPerson,buf);

  //fprintf(stderr,"Writing %d serialized bytes!\n",len); // See the length of message
  //fwrite(buf,len,1,stdout); // Write to stdout to allow direct command line piping

  free(buf); // Free the allocated serialized buffer


  WDTCTL = WDTPW | WDTHOLD;               // Stop watchdog timer
  PM5CTL0 &= ~LOCKLPM5;                   // Disable the GPIO power-on default high-impedance mode
                                          // to activate previously configured port settings
  P1DIR |= 0x01;                          // Set P1.0 to output direction

  for(;;) {
      volatile unsigned int i;            // volatile to prevent optimization

      P1OUT ^= 0x01;                      // Toggle P1.0 using exclusive-OR

      i = 50000;                          // SW Delay
      do i--;
      while(i != 0);
  }

  return 0;
}