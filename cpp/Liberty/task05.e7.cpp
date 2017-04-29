#include <iostream>
using namespace std;

typedef unsigned short USHORT;
typedef unsigned long ULONG;
double GetPower(USHORT n, USHORT power);

int main()
{
   USHORT number, power;
   ULONG answer;
   cout << "Enter a number: ";
   cin >> number;
   cout << "To what power? ";
   cin >> power;
   answer = GetPower(number,power);
   cout << number << " to the " << power << "th power is " << answer << endl;
   return 0;
}

double GetPower(USHORT n, USHORT power)
{
   if(power == 1)
      return n;
   else
     {
      return (n * GetPower(n,power-1));
      cout << " n = " << n << " power = " << power;
     }
}

