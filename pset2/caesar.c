#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{

    // Declaring variables
    int k;
    string plaintext;

    // Check for command-line argument
    if(argc == 2 && argv[1] >= 0)
    {
        k = atoi(argv[1]);
    }
    else
    {
        // Error message
        printf("Please enter a single non-negative integer\n");
        return 1;
    }

    // Prompt for input
    printf("plaintext: ");

    // Get input
    plaintext = get_string();

    // Calculating length of input
    int length = strlen(plaintext);

    // Start printing output
    printf("ciphertext: ");

    // Start encrypting message
    for(int i = 0; i < length; i++)
    {
        // Rotate Uppercase Letters
        if(plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            printf("%c", 'A' + (plaintext[i] - 'A' + k)%26);
        }
        // Rotating Lowercase Letters
        else if(plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            printf("%c", 'a' + (plaintext[i] - 'a' + k)%26);
        }
        // Printing off non-letters
        else
        {
            printf("%c",plaintext[i]);
        }

    }

    printf("\n");

    return 0;

}