#模拟运行时间过长的情况，可以根据需要调整i值
```c
#include<stdio.h>
int main(){
 long long time =1000000000;
 int i=0;
 for(i=0;i<3;i++)
 {
   while(time--){}
   time=1000000000;
 }
 return 0;
}
```
