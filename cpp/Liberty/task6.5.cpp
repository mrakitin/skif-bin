// Пример ошибки компиляции, связанной
// с нарушениями соглашений интерфейса класса

#include <iostream> // для объекта cout
using namespace std;

class Cat
{
public:
  Cat(int initialAge);
  ~Cat();
  int GetAge() const; // метод доступа const
  void SetAge (int age);
  void Meow();
private:
  int itsAge;
};

// конструктор класса Cat
Cat::Cat(int initialAge)
{
  itsAge = initialAge;
  cout << "Cat constructor\n";
}

Cat::~Cat() // деструктор, который не выполняет никаких действий
{
  cout << "Cat destructor\n";
}

// функция GetAge объявлена как const,
// но мы нарушаем это условие!
int Cat::GetAge() const
{
  return (itsAge++); // это нарушение соглашения интерфейса!
}

// определение функции SetAge как открытого
// метода доступа к данным класса
void Cat::SetAge(int age)
{
  // присваиваем переменной-члену itsAge
  // значение переданного парйметра age
  itsAge = age;
}

// Определение метода Meow
// возвращает void
// параметров нет
// используется для вывода на экран текста "Meow"
void Cat::Meow()
{
  cout << "Meow.\n";
}

// демонстрирует различные нарушения
// интерфейса, что приводит к ошибкам компиляции
int main()
{
  Cat Frisky; // не соответствует обьявлению
  Frisky.Meow();
  Frisky.Bark(); // Нет, кошки не лают.
  Frisky.itsAge = 7; // переменная itsAge закрыта
  return 0;
}

