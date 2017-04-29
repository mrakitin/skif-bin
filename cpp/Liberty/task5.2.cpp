#include <iostream>
using namespace std;

float Convert(float);
int main()
{
   float TempFer;
   float TempCel;

   cout << "Please enter the temperature in Fahrenheit: ";
   cin >> TempFer;
   TempCel = Convert(TempFer);
   cout << "\nHere's the temperature in Celsius: ";
   cout << TempCel << endl;
   return 0;
}

float Convert(float FerTemp)
{
    float CelTemp;
    CelTemp = ((FerTemp - 32) * 5) / 9;
    return CelTemp;
}
