#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Declaring variables
    string k;
    string plaintext;

    // Check for command-line argument
    if(argc == 2 && argv[1] >= 0)
    {
        k = argv[1];

        // Check if all entries in k are letters
        for(int i = 0; i < strlen(k); i++)
        {
            if(!(k[i] >= 'A' && k[i] <= 'Z') && !(k[i] >= 'a' && k[i] <= 'z'))
            {
                printf("Entered key has non-letter entry\n");
                return 1;
            }
        }
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
    int inputLength = strlen(plaintext);
    int keyLength = strlen(k);

    // Start printing output
    printf("ciphertext: ");

    // Start encrypting message
    for(int i = 0, j = 0; i < inputLength; i++)
    {
        if(j == keyLength)
        {
            j = 0;
        }
        // Rotate Uppercase Letters
        if(plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            printf("%c", 'A' + (plaintext[i] - 'A' + tolower(k[j]) - 'a')%26);
            j++;
        }
        // Rotating Lowercase Letters
        else if(plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            printf("%c", 'a' + (plaintext[i] - 'a' + tolower(k[j]) - 'a')%26);
            j++;
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