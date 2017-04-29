// Пример определения методов в
// объявлении класса

#include <iostream> // для объекта cout
using namespace std;

class Cat // начало объявления класса
{
public: // начало раздела public
  int GetAge(); // метод доступа
  void SetAge (int age); // метод доступа
  void Meow(); // обычный метод
private: // начало раздела
  int itsAge; // переменная-член
};

// GetAge, открытая функция доступа,
// возвращает значение переменной-члена itsAge
int Cat::GetAge()
{
  return itsAge;
}

// Определение открытой функции доступа SetAge
// Функция SetAge
// инициирует переменную-член itsAge
void Cat::SetAge(int age)
{
  // устанавливаем переменную-член itsAge равной
  // значению, переданному с помощью параметра age
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
// ей мяукнуть, сообщаем ее возраст, затем снова "мяукаем".
int main()
{
  Cat Frisky;
  Frisky.SetAge(5);
  Frisky.Meow();
  cout << "Frisky is а cat who is ";
  cout << Frisky.GetAge() << " years old.\n";
  Frisky.Meow();
  return 0;
}

