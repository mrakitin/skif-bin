// Пример объявление класса с
// открытыми членами

#include <iostream> // для использования cout
using namespace std;

class Cat // объявляем класс
{
   
  public: // следующие члены являются открытыми
    int itsAge;
    int itsWeight;
};

int main()
{
  Cat Frisky;
  Frisky.itsAge=5; // присваиваем значение переменной-члену
  cout << "Frisky is а cat who is ";
  cout << Frisky.itsAge << " years old.\n";
  return 0;
}

