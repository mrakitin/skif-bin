// Пример использования подставляемых функций
// и включения файла заголовка

#include "task6.7.hpp" // не забудьте включить файл заголовка!
//using namespace std;

Cat::Cat(int initialAge) //конструктор
{
  itsAge = initialAge;
}

Cat::~Cat() // деструктор, не выполняет никаких действий
{}

// Создаем виртуальную кошку, устанавливаем ее возраст, разрешаем
// ей мяукнуть, сообщаем ее возраст, затем снова "мяукаем" и изменяем возраст кошки.
int main()
{
  Cat Frisky(5);
  Frisky.Meow();
  cout << "Frisky is а cat who is ";
  cout << Frisky.GetAge()  << " years old.\n";
  Frisky.Meow();
  Frisky.SetAge(7);
  cout << "Now Frisky is " ;
  cout  << Frisky.GetAge()  << " years old.\n";
  return 0;
}

