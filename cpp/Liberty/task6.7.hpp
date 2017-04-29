#include <iostream>
using namespace std;

class Cat
{
public:
  Cat (int initialAge);
  ~Cat();
  int GetAge() const { return itsAge;} // подставляемая функция!
  void SetAge (int age) { itsAge = age;} // подставляемая функция!
  void Meow() const { cout << "Мяу.\n";} // подставляемая функция!
private:
  int itsAge;
};

