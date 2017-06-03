#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
int getkey(int lettercipher,string k);
int main(int argc,string argv[])
{
    if(argc!=2)
    {
        printf ("Give the valid keyword \n");
       
        return 1;
        //exit;
    }
    string k = argv[1];
    for(int j=0,length=strlen(k);j<length;j++)
    {
        if(!isalpha(k[j]))
        {
            printf("Invalid keyword \n");
            return 1;
            //exit;
        }
    }
    printf("plaintext:");
    string plaintext = get_string();
    
    int lettercipher =0;
    printf("ciphertext:");
    for(int i =0,n=strlen(plaintext);i<n;i++)
    {
        char c=plaintext[i];
        
        if (isupper(c))
        {
            char newc =(((c-65) + getkey(lettercipher,k)) %26) +65;
            printf("%c",newc);
            lettercipher++;
            
        }
        else if (islower(c))
        {
           
            char newc =(((c-97) + getkey(lettercipher,k)) %26) +97;
            printf("%c",newc);
            lettercipher++; 
        }
        else
        {
            printf("%c",c);
            
        }
    }
        printf("\n");
        return 0;
    
    
}
int getkey(int lettercipher,string k)
{
    int l=strlen(k);
    return tolower(k[lettercipher % l])-97;
}