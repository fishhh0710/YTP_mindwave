#include "iostream"
#include <thread>
#include <chrono>
using namespace std;
int main(){
    for(int i=0;i<10;i++){
        // if(i%4==0)cout<<"PoorSignal"<<endl;
        // else if(i%4==1)cout<<"GreatSignal"<<endl;
        // else if(i%4==2)cout<<"Click!"<<endl;
        // else if(i%4==3)cout<<"Cd_ends"<<endl;
        this_thread::sleep_for(std::chrono::seconds(3));
        cout<<"Click!"<<endl;
    }
}