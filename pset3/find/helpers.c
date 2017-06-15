/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    int low=0;
    int high=n-1;
    while(low <= high)
    {
        int midterm=low + ((high-low)/2);
        if(value == values[midterm])
        {
            return true;
        }
        else if (value < values [midterm])
        {
            high=midterm-1;
        }
        else if (value > values [midterm])
        {
            low=midterm +1;
        }
        
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int temp;
    for(int i = 0;i<n;i++)
    {
        int smallest=i;
        for(int j=i+1;j<n;j++)
        {
            if (values[smallest] > values[j] )
            {
                smallest=j;
            }
        }
        temp=values[smallest];
        values[smallest]=values[i];
        values[i]=temp;
    }
    
    return;
}
