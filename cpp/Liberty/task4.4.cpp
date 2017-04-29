// Листинг 4.4. Демонстрирует использование
// префиксных и постфиксных операторов
// инкремента и декремента

#include <iostream>
using namespace std;

int main()
{
   int myAge = 39;  // инициализируем две целочисленные переменные
   int yourAge = 39;
   cout << "I am: " << myAge << " years old.\n";
   cout << "You are: " << yourAge << " years old\n";
   myAge++;    // постфиксный инкремент
   ++yourAge;   // префиксный инкремент
   cout << "One year passes...\n";
   cout << "I am: " << myAge << " years old.\n";
   cout << "You are: " << yourAge << " years old\n";
   cout << "Another year passes\n";
   cout << "I am: " << myAge++ << " years old.\n";
   cout << "You are: " << ++yourAge << " years old\n";
   cout << "Let's print it again.\n";
   cout << "I am: " << myAge << " years old.\n";
   cout << "You are: " << yourAge << " years old\n";

   return 0;
}
