/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"


// Linked List Nodes
    // word - array for holding the word
    // *next - pointer for next node in LL
// Declaration:
    // node *node1 = malloc(sizeof(node));
// Usage:
    // strcpy(node1->word, "Hello");
typedef struct node
{
    char word[LENGTH+1];
    struct node *next;
}
node;

node *hashTable[26];


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    int index = tolower(word[0]) - 'a';

    //node *checked_word = malloc(sizeof(node));
    node *checked_word = hashTable[index];

    if(checked_word == NULL)
    {
        free(checked_word);
        return false;
    }

    while(checked_word != NULL)
    {
        if(strcmp(checked_word->word, word) == 0)
        {
            free(checked_word);
            return true;
        }

        checked_word = checked_word->next;

    }

    free(checked_word);
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{

    for(int i = 0; i < 26; i++)
    {
        hashTable[i] = NULL;
    }

    FILE *outptr = fopen(dictionary, "r");

    char word[LENGTH+1];


    while(fscanf(outptr, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        if(new_node == NULL)
        {
            // unload()
            fclose(outptr);
            return false;
        }
        strcpy(new_node->word, word);

        int index = tolower(new_node->word[0]) - 'a';

        new_node->next = hashTable[index];
        hashTable[index] = new_node;

    }

    fclose(outptr);

    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{

    int count = 0;

    for(int i = 0; i < 26; i++)
    {
        //node *currWord = malloc(sizeof(node));
        node *currWord = hashTable[i];

        if(currWord == NULL)
        {
            continue;
        }

        while(currWord != NULL)
        {
            count++;

            currWord = currWord->next;

        }
        free(currWord);

    }


    return count;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for(int i = 0; i < 26; i++)
    {

        //node *cursor = malloc(sizeof(node));

        node *cursor = hashTable[i];

        while(cursor != NULL)
        {
            //node *temp = malloc(sizeof(node));
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
