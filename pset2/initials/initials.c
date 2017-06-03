#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>

int main()
{
    //printf("User name: \n");
    
    string username =get_string();
    printf("%c",toupper(username[0]));
    
    for (int i=0,n=strlen(username);i<n;i++)
    {
        if(username[i]==' ' && username[i+1]!= '\0')
        {
            printf("%c",toupper(username[i+1]));
            i++;
            
        }
    }
    printf("\n");
}
    