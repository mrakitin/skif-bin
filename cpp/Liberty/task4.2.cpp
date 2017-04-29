// Листинг 4.2. Пример вычитания с
// переполнением целого числа
#include <iostream>
using namespace std;

int main()
{
  unsigned int difference;
  unsigned int bigNumber = 100;
  unsigned int smallNumber = 50;
  difference = bigNumber - smallNumber;
  cout << "Difference is: " << difference;
  difference = smallNumber - bigNumber;
  cout << "\nNow difference is: " << difference << endl;
  return 0;
}
