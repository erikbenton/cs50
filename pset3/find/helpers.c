/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include <stdio.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    // Binary search


    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    // Bubble sort

    // Declare variables
    int swaps = 0;  // Number of swaps
    int temp;       // Holder for temperorary value

    // Go thru the array and swap so smallest to largest
    for(int i = 0; i < n-1; i++)
    {
        // If current val is smaller than next val
        // Swap them using temp
        // Increment number of swaps
        if(values[i] > values[i+1])
        {
            temp = values[i];
            values[i] = values[i+1];
            values[i+1] = temp;
            swaps++;
        }

        // If i is at the end and we've swapped at least once
        // Start back over and keep swapping
        if(i == n-2 && swaps > 0)
        {
            swaps = 0;
            i = -1;
        }

    }

    return;
}
