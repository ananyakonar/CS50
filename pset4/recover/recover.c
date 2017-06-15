#include<stdio.h>
#include<string.h>
#include<cs50.h>

int main(int argc, char *argv[])
{
    if(argc!=2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1; 
    }
    //string s=argv[1];
    
    FILE* inputfile;
    inputfile= fopen(argv[1],"r");
    if ( inputfile == 0 )
        {
            printf( "Could not open file\n" );
            return 2;
        }
    char buf[512]={0};
    char jpeg1[4] = {0xff, 0xd8, 0xff, 0xe0};    
    char jpeg2[4] ={0xff, 0xd8, 0xff, 0xe1}; 
    char filename[50];
    int fileno=0;
    FILE* outputfile;
    int c=0;
    while (c != EOF) {

        for (int k = 0; k < 512; k++)
        {
            buf[k] = c = fgetc(inputfile);
        }
    
        if (memcmp(buf, jpeg1, 4) == 0 || memcmp(buf, jpeg2, 4) == 0) {

            
            if (outputfile) 
            {
                fclose(outputfile);
            }

            
            int x;
            fileno++;
            x = sprintf(filename, "%03d.jpg", fileno);
            
            outputfile=fopen(filename,"w");
            if (!outputfile) 
            {
                printf("Error opening outfile.\n");
                return 2;
            }
            fwrite(buf, 1, 512, outputfile);
        }
        else if (outputfile)
        {
           fwrite(buf, 1, 512, outputfile); 
        }
    }
    fclose(inputfile);
    if (outputfile!=NULL) 
    {
        fclose(outputfile);
    }

    //printf("Success.\n");
    return 0;
            
            
}
