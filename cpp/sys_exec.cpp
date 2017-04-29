/* system example : DIR */
#include <stdio.h>
#include <stdlib.h>

int main ()
{
  char i;
  printf ("Checking if processor is available...");
  if (system(NULL)) puts ("Ok");
    else exit (1);
  printf ("Executing command DIR...\n");
  i=system ("grep :ENE /home/max/calc/Fe53MeH/Fe53ScH/Fe53ScH_01/Fe53ScH_01.scf | tail -1 | awk -F= '{print $2}' | awk '{print $1}'");
  printf ("The value returned was: %d.\n",i);
  return 0;
}


