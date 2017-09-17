#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int minutes;

    printf("Minutes: ");
    minutes = get_int();

    printf("Bottles: %i\n", (192 * minutes) / 16);

}