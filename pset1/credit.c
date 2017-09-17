#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Declare variables
    long long number;
    long long temp;
    int digits = 1;

    // Ask for input
    printf("Number: ");

    number = get_long_long();
    temp = number;

    // Find # of digits in number
    while(temp > 0)
    {
        digits++;
        temp = temp/(digits * 10);
    }






}