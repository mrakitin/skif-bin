// Пример объявления конструктора и
// деструктора в классе Cat

#include <iostream> // для объекта cout
using namespace std;

class Cat // начало объявления класса
{
public: // начало открытого раздела
  Cat(int initialAge); // конструктор
  ~Cat(); //деструктор
  int GetAge(); // метод доступа
  void SetAge(int age); // метод доступа
  void Meow();
private: // начало закрытого раздела
  int itsAge; // переменная-член
};
 
// конструктор класса Cat
Cat::Cat(int initialAge)
{
  itsAge = initialAge;
}

Cat::~Cat() // деструктор, не выполняющий действий
{}

// GetAge, открытая функция обеспечения доступа,
// возвращает значение переменной-члена itsAge
int Cat::GetAge()
{
  return itsAge;
}

// Определение SetAge, открытой
// функции обеспечения доступа

void Cat::SetAge(int age)
{
  // устанавливаем переменную-член itsAge равной
  // значению, переданному параметром age
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

// Создаем виртуальную кошку, устанавливаем ее возраст, разрешаем
// ей мяукнуть, сообщаем ее возраст, затем снова "мяукаем" и изменяем возраст кошки.
int main()
{
  Cat Frisky(5);
  Frisky.Meow();
  cout << "Frisky is а cat who is ";
  cout << Frisky.GetAge() << " years old.\n";
  Frisky.Meow();
  Frisky.SetAge(7);
  cout << "Now Frisky is ";
  cout << Frisky.GetAge() << " years old.\n";
  return 0;
}
