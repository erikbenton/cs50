#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFFER_SIZE 512

int main(int argc, char *argv[])
{

    // Checks for the right command-line inputs
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    // remember filename
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // Bool for if a JPEG has been found
    int foundJPEG = 0;

    // Create place to hold block of bytes
    unsigned char buffer[BUFFER_SIZE];

    // Pointer for writing to file
    FILE *outptr = NULL;

    // Count of how many JPEGs found
    int count = 0;

    // Read from file until no more blocks
    while(fread(buffer, BUFFER_SIZE, 1, inptr) == 1)
    {

        // Check for beginning of block
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            if(foundJPEG == 1)
            {
                fclose(outptr);
            }
            else
            {
                foundJPEG = 1;
            }

            count++;
            char outfile [8];
            sprintf (outfile, "%03i.jpg",count);

            outptr = fopen(outfile, "w");

        }

        if(foundJPEG == 1)
        {
            fwrite(&buffer, BUFFER_SIZE, 1, outptr);
        }

    }

    fclose(outptr);
    fclose(inptr);

    return 0;

}