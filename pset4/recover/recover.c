#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

typedef struct
{
    BYTE first;
    BYTE second;
    BYTE third;
    BYTE fourth;
} __attribute__((__packed__))
BLOCK;



int main(int argc, char *argv[])
{
    int count = 0;
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    while(count < 50)
    {
        BLOCK block;

        // read BLOCK from infile
        fread(&block, sizeof(BLOCK), 1, inptr);

        if(block.first == 0xff && block.second == 0xd8 && block.third == 0xff)
        {
            printf("HERE\n");

            count++;
            char outfile [7];
            sprintf (outfile, "%03i.jpg",count);

            FILE *outptr = fopen(outfile, "w");
            // write outfile's BITMAPINFOHEADER
            fwrite(&block, sizeof(BLOCK), 1, outptr);



        }

        fseek(inptr, 512-sizeof(BLOCK), SEEK_CUR);
    }

}