// ==========================================
// Project "Black Hole"
// Build Alpha 0.0.1
// Status - I have not started. IDK probably very broken and very cursed
//===========================================

#include <iostream>
#include <string>
#include <fstream>
using namespace std;

void shop();
void combat();

int main() {

    string playerName;
    cout << "Enter name here: ";
    cin >> playerName;
    cout << "Welcome don't regret this " << playerName << "\n";

    cout << "Starting Game ... \n";
    cout << "Day 1 ... \n\n";
    cout << "Good luck I guess\n";

    cout << "Day 2 ... \n\n";
    cout << "Day 3 ... \n\n"; //o or maybe I don't have days

    int playerHealth = 200;
    cout << "[DEBUG] Player Health: " << playerHealth << "\n";

    //int m = 60 = yeah I forgot what this was for 
    //note to self never use single letters

    int enemyHealth = 100; 
    cout << "[DEBUG] Enemy Health: " <<enemyHealth << "\n\n";

    //TODO: add boss fight
    //TODO: fix bugs 
// part four of flag _r1ght?}
    //TODO: Actually finish this at some point?
    // And yes I did actually learn C++ with w3schools just to make this part of the challenge 

    ofstream save("save.txt");
    save <<playerName
    save <<playerName
    save.close();

    return 0;
}

    void shop () {
        //code for shop will go here
        cout << "You have entered a shop \n";
    char choice;
    cout << "Do you buy anything (y/n): \n";
    cin >> choice ;

    if (choice == 'y' || choice == 'Y') {
        cout << "Items available: \n";
        cout << "1. Sword \n";
        cout << "2. Poison \n";
        cout << "3. Healing Potion \n";
        cout << "4. Shield \n";
        cout <<"Shop system: INCOMPLETE\n";
    }

    else if (choice == 'n' || choice == 'N') {
        cout << "You leave the shop. \n";
    }

    else {
        cout << "Invalid choice. \n";
    }
}