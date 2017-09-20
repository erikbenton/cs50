/**
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize size infile outfile\n");
        return 1;
    }
    else if(atoi(argv[1]) > 100 || atoi(argv[1]) < 0)
    {
        fprintf(stderr, "size must be positive and <= 100\n");
        return 1;
    }

    // remember filenames
    int size = atoi(argv[1]);
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

    // determine old padding for scanlines
    int oldPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    printf("bfSize: %x  biSizeImage: %x  biWidth: %x   biHeight: %x  padding: %x\n",
            bf.bfSize, bi.biSizeImage, bi.biWidth, bi.biHeight, oldPadding);

    bi.biWidth = bi.biWidth * size;
    bi.biHeight = bi.biHeight * size;


    // determine new padding for scanlines
    int newPadding = (oldPadding * size) % 4;

    bi.biSizeImage = (bi.biWidth * sizeof(RGBTRIPLE) + newPadding )* abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + 0x36;

    printf("bfSize: %x  biSizeImage: %x  biWidth: %x   biHeight: %x  padding: %x\n",
            bf.bfSize, bi.biSizeImage, bi.biWidth, bi.biHeight, newPadding);

     // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i = i + size)
    {

        long beg = ftell(inptr);

        for(int l = 0; l < size; l++)
        {

            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j = j + size)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for(int m = 0; m < size; m++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // skip over padding, if any
            fseek(inptr, oldPadding, SEEK_CUR);

            // then add it back (to demonstrate how)
            for (int k = 0; k < newPadding; k++)
            {
                fputc(0x00, outptr);
            }

            if(l < size-1)
            {
                fseek(inptr, beg, SEEK_SET);
            }

        }

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
