#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Declare variables
    int height = -1;

    while(height < 0 || height > 23)
    {
        // Ask for height
        printf("Height: ");

        height = get_int();
    }

    for(int i = 1; height - i >= 0; i++)
    {
        for(int j = 0; j < height - i; j++)
        {
            printf(" ");
        }
        for(int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("  ");
        for(int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");
    }

}