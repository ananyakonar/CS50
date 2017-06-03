#include<stdio.h>
#include<cs50.h>
int main()
{
    int min;
    do
    {
        printf("minutes: \n");
        min = get_int();
        
    } while (min<0);
    
    int bottles=(128 * (1.5 * min))/16;
    printf("bottles: %i \n",bottles);
}
