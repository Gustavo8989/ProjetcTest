#include <iostream> 
#include <string> 

using namespace std;

int main(){
    cout << "Conversor de Tempetura" << endl;
    double celsius;
    double fahrenheit;
    string escolha;
    cout << "Digite qual medida de temperatura você quer? " << endl;
    cin >> escolha;
    if (escolha == "fahrenheit"){
        cout << "Será transformado de fahrenheit para celsius" << endl;
        cout << "Digite a temperatura" << endl;
        cin >> fahrenheit;
        double conversao = 5/9 * (fahrenheit - 32);
        cout << conversao << endl;
    }
    else if(escolha == "celsius"){
        cout << "Será transformado de celsius para fahrenheit" << endl;
        cout << "Digite a temperatura" << endl;
        cin >>  celsius;
        double conversao = (celsius * 9/5) + 32;
        cout << conversao << endl;
    }

}
