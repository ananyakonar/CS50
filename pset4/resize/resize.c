/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include<math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    int n = atoi(argv[1]);
    if(n < 0 || n>100)
    {
        printf("n must be betwwen 0 to 100\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    int prevwidth=bi.biWidth;
    //int prevheight=bi.biHeight;
    
    bi.biWidth=bi.biWidth * n;
    bi.biHeight=bi.biHeight * n;
    
    int newwidth=bi.biWidth;

    int newheight=abs(bi.biHeight);
   // int old_padding =  (4 - (prevwidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding =  (4 - (newwidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    bi.biSizeImage = abs(newheight )* ((newwidth * sizeof(RGBTRIPLE)) + padding);
    
    //Updated bi.biSizeImage = (Updated bi.biWidth * sizeof(RGBTRIPLE) + padding) * absolute value of Updated bi.biHeight
    
    bf.bfSize=bi.biSizeImage + sizeof(BITMAPFILEHEADER)+ sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
     int length = sizeof(RGBTRIPLE) * prevwidth;
     RGBTRIPLE* scanline = malloc(length);
     int x;
     for (int i = 0; i < newheight; i++) 
     {
          int y = i / n;
          if (y > x || i == 0) 
          {
              fseek(inptr, (54 + (length * y)), SEEK_SET);
              for (int j = 0; j < prevwidth; j++)
              {
                   fread((scanline + j), sizeof(RGBTRIPLE), 1, inptr);
              }
              
              
          }
          for (int k = 0; k < newwidth; k++) {
            
            RGBTRIPLE pixel;   

            
            int s = k / n;
            pixel = scanline[s];
            
            fwrite(&pixel, sizeof(RGBTRIPLE), 1, outptr);
        }
        if (padding > 0) {
            for (int l = 0; l < padding; l++)
            {
                fputc(0x00, outptr); 
            }
        }
        x = y; 
     }
     free(scanline);
    


    

           

    //fseek(inptr, old_padding, SEEK_CUR);        

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
