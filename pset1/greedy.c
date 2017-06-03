#include<stdio.h>
#include<cs50.h>
#include<math.h>
int main()
{
    float amount=0;
    int cent=0;
    int quarter=0;
    int dime=0;
    int nickel=0;
    int amount_left=0;
    int count=0;
    do
    {
        printf ("How much change is owed? \n");
        amount=get_float();
        
    }while(amount<=0);
      
      cent = (int)round(amount*100);
      //for quarter
      quarter=cent/25;
      amount_left=cent%25;
      //for dime
      dime=amount_left/10;
      amount_left=amount_left%10;
      //for nickel
      nickel=amount_left/5;
      amount_left=amount_left%5;
      count= quarter + dime + nickel + amount_left;
      printf("%d \n",count);
      return 0;
      
}
