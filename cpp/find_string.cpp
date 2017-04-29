#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <algorithm>
using namespace std;

int main()
{
    ifstream f("/home/max/calc/test_slurm/Fe54/Fe54.scf");
    string s(":ENE");

    istreambuf_iterator<char> eof;
    if(eof == search(istreambuf_iterator<char>(f), eof, s.begin(), s.end()) )
        cout << "String \"" << s << "\" was NOT found in the file " << endl;
    else
        cout << "String \"" << s << "\" was found in the file " << endl;

    cout << "=== eof" << f <<  endl; 
}
