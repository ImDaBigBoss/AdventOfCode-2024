#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h> // Include OpenMP
#include <stdint.h>

// Function to read input file and store integers in an array
int* read_input(const char* file, uint64_t* size) {
    FILE* f = fopen(file, "r");
    if (f == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    int* stones = NULL;
    *size = 0;
    char line[1024];

    while (fgets(line, sizeof(line), f)) {
        char* token = strtok(line, " \n");
        while (token != NULL) {
            stones = realloc(stones, (*size + 1) * sizeof(int));
            if (stones == NULL) {
                perror("Memory allocation failed");
                exit(EXIT_FAILURE);
            }
            stones[*size] = atoi(token);
            (*size)++;
            token = strtok(NULL, " \n");
        }
    }

    fclose(f);
    return stones;
}

// Function to count the number of digits in a number
int count_digits(uint64_t value) {
    return (value == 0) ? 1 : (int) log10(value) + 1;
}

// Recursive function to count stones after a given number of iterations
uint64_t count_stones_after_iteration(uint64_t value, uint64_t remaining_deepness) {
    if (remaining_deepness == 0) {
        return 1;
    }

    if (value == 0) {
        return count_stones_after_iteration(1, remaining_deepness - 1);
    } else {
        int len = count_digits(value);

        if (len % 2 == 0) {
            int half_len = len / 2;

            uint64_t left_value = value / (uint64_t) pow(10, half_len);
            uint64_t right_value = value % (uint64_t) pow(10, half_len);

            uint64_t left, right;
            #pragma omp task shared(left)
            {
                left = count_stones_after_iteration(left_value, remaining_deepness - 1);
            }
            #pragma omp task shared(right)
            {
                right = count_stones_after_iteration(right_value, remaining_deepness - 1);
            }
            #pragma omp taskwait

            return left + right;
        } else {
            return count_stones_after_iteration(value * 2024, remaining_deepness - 1);
        }
    }
}

int main() {
    const char* filename = "input.txt";
    uint64_t stone_count;
    int* stones = read_input(filename, &stone_count);

    printf("There are initially %lu stones.\n", stone_count);

    int iteration_count = 75;
    uint64_t total_stones = 0;

    omp_set_nested(1); // Enable nested parallelism
    omp_set_num_threads(12);

    // Parallelize using OpenMP
    #pragma omp parallel for reduction(+:total_stones)
    for (int i = 0; i < stone_count; i++) {
        total_stones += count_stones_after_iteration(stones[i], iteration_count);
    }

    printf("After %d iterations, there are %lu stones.\n", iteration_count, total_stones);

    free(stones);
    return 0;
}
