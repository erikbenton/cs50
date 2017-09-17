#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

#include "helpers.h"

int main(void)
{
    int test[] = {3, 4, 5, 1};

    sort(test, 4);

    for(int i = 0; i < 4; i++)
    {
        printf("%i ", test[i]);
    }
    printf("\n");
}