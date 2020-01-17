#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """

    for i in range(length):
        hash_table_insert(ht, weights[i], i)

    for j in range(length):
        weight_difference = limit - weights[j]

        difference_key = hash_table_retrieve(ht, weight_difference)

        if difference_key != None:
            if difference_key >= j:
                return (difference_key, j)
            else:
                return (j, difference_key)
    
    return None

def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
