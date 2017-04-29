// Листинг 4.7. Пример сложной конструкции с
// вложенными операторами if
#include <iostream>
using namespace std;

int main()
{
   // Запрашиваем два числа
   // Присваиваем числа переменным bigNumber и littleNumber
   // Если значение bigNumber больше значения littleNumber,
   // проверяем, делится ли большее число на меньшее без остатка
   // Если да, проверяем, не равны ли они друг другу

   int firstNumber, secondNumber;
   cout << "Enter two numbers.\nFirst: ";
   cin >> firstNumber;
   cout << "\nSecond: ";
   cin >> secondNumber;
   cout << "\n\n";

   if (firstNumber >= secondNumber)
   {
     if ( (firstNumber % secondNumber) == 0) // evenly divisible?
     {
       if (firstNumber == secondNumber)
         cout << "They are the same!\n";
       else
         cout << "They are evenly divisible!\n";
     }
     else
       cout << "They are not evenly divisible!\n";
   }
   else
     cout << "Hey! The second one is larger!\n";

   return 0;
}

