#include <stdio.h>
#include <cs50.h>
int main()
{
    int height;
    do
    {
        printf("Height: \n");
        height=get_int();
        
    } while(height <=0 || height >=24);
    
    for(int rows=0;rows<height;rows++)
    {
        for(int spaces=0;spaces < height-rows-1;spaces++ )
        {
            printf("%s", " ");
        }
        for (int hashes= 0; hashes < rows+2; hashes++)
        {
            printf("#");
        }
        printf("\n");
    }
}
