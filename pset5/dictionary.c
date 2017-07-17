

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

#include "dictionary.h"

typedef struct node
{
    bool is_word;
    struct node* childnode[27];
}
node;

node* root_node;


void freeing(node* childnode)
{
    for (int i = 0; i < 27; i++)
    {
        if (childnode->childnode[i] != NULL)
        {
            freeing(childnode->childnode[i]);
        }
    }

    free(childnode);
}

// create global variable to count size
int dict_Size = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char* word)
{
    int index;

    node* path = root_node;

    for (int i = 0; word[i] != '\0'; i++)
    {

        if (word[i] == '\'')
        {
            index = 26;
        }
        else

        {
            index = tolower(word[i]) - 'a';
        }


        path = path->childnode[index];
       if (path == NULL)
        {
            return false;
        }
    }
    if (path->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}
bool load(const char* dictionary)
{
    FILE* filepointer = fopen(dictionary, "r");
    int index;
    char word[LENGTH+1];

    // if cannot open file, return false
    if (filepointer == NULL)
    {
        return false;
    }

    // Creating Tries and initialize default value & pointer
root_node= malloc(sizeof(node));
 root_node->is_word = false;
    for (int j = 0; j < 27; j++)
    {
         root_node->childnode[j] = NULL;
    }


    while(fscanf(filepointer, "%s\n", word) != EOF)
    {

        node* path =  root_node;
        for (int i = 0; word[i] != '\0'; i++)
        {
            if (word[i] == '\'')
            {
                index = 26;
            }
            else

            {
                index = tolower(word[i]) - 'a';
            }

            if (path->childnode[index] == NULL)
            {

                node* nodenew = malloc(sizeof(node));
                nodenew->is_word = false;
                for (int k = 0; k < 27; k++)
                {
                    nodenew->childnode[k] = NULL;
                }
                // and set children[index] to point at it
                path->childnode[index] = nodenew;
            }
            // move traversal pointer to it
            path = path->childnode[index];
        }
        // At end of word, set is_word true;
        path->is_word = true;
        dict_Size++;
    }


    fclose(filepointer);
 return true;
}


unsigned int size(void)
{
    return dict_Size;
}


bool unload(void)
{
    node* path =  root_node;
    freeing(path);
    return true;
}

