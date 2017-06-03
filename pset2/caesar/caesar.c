#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
#include<stdlib.h>

int main(int argc,string argv[])
{
    string key= argv[1];
    if(argc!=2)
    {
        printf ("Give the valid key \n");
        return 1;
    }
    else
    {
        int i=atoi(key) %26;
        if(i==0)
        {
            printf("invalid Key!try again \n");
            return 1;
        }
        printf("plaintext:");
       string plaintext=get_string();
       printf("ciphertext:");
       if (plaintext!=NULL)
       {
           for(int k=0,n=strlen(plaintext);k<n;k++)
           {
               int cipher=0;
               if(isalpha(plaintext[k]))
               {
                   
               
               if (isupper(plaintext[k]))
               {
                   cipher=(((int)plaintext[k]- 65+ i) %26)+65;
                   printf("%c", (char)cipher);
               }
               else  
               {
                   cipher=(((int)plaintext[k]- 97+ i) %26)+97;
                   printf("%c", (char)cipher);
               }
               }
               else
               {
                  printf("%c",plaintext[k]); 
               }
               
           }
           printf("\n");
           return 0;
       }
    }
}