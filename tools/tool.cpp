#include "iostream"
using namespace std;
string dict[15][5];
string table = "1234567890qwertyuiopasdfghjkl;zxcvbnm,.?";
void rec(int x0,int y0,int x1,int y1,string temp){
    if(x0==x1&&y0==y1){
        dict[x0][y0] = temp;   
        return ;
    }
    if(x0!=x1){
        int m = (x0+x1)/2;
        rec(x0,y0,m,y1,temp+"1");
        rec(m+1,y0,x1,y1,temp+"0");
    }
    else{
        int m = (y0+y1)/2;
        rec(x0,y0,x1,m,temp+"1");
        rec(x0,m+1,x1,y1,temp+"0");
    }
}
int main(){
    rec(0,0,9,3,"");
    cout<<"{";
    for(int i=0;i<4;i++){
        for(int j=0;j<10;j++){
            cout<<"\""<<dict[j][i]<<"\":\""<<table[i*10+j]<<"\",";
        }
    }
}