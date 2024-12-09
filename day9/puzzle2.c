#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct fs_block {
    bool present;
    uint16_t block_id;
    uint8_t block_size;
    struct fs_block* prev;
    struct fs_block* next;
} fs_block_t;

void free_fs(fs_block_t* fs) {
    fs_block_t* current = fs;
    while (current != NULL) {
        fs_block_t* next = current->next;
        free(current);
        current = next;
    }
}

fs_block_t* read_file(char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return NULL;
    }

    fs_block_t* head = NULL;
    fs_block_t* current = NULL;

    //Read the file character by character
    char c = 0;
    bool empty_space = false;
    uint16_t current_id = 0;

    while (fread(&c, 1, 1, file) == 1) {
        //Interpret the character, it shoud be a character from '0' to '9'
        if (c == '\n') {
            continue;
        } else if (c < '0' || c > '9') {
            free_fs(head);
            return NULL;
        } else {
            c = c - '0';
        }

        if (c == 0) { //Block with null size
            empty_space = !empty_space;
            continue;
        }

        fs_block_t* block = (fs_block_t*) malloc(sizeof(fs_block_t));
        if (empty_space) {
            block->present = false;
        } else {
            block->present = true;
            block->block_id = current_id;
            current_id++;
        }

        block->block_size = c;
        block->prev = current;
        block->next = NULL;

        if (head == NULL) {
            head = block;
        }
        if (current != NULL) {
            current->next = block;
        }

        current = block;
        empty_space = !empty_space;
    }

    return head;
}

void debug_print_fs(fs_block_t* fs) {
    printf("FS: ");
    fs_block_t* current = fs;
    while (current != NULL) {
        if (current->present) {
            for (int i = 0; i < current->block_size; i++) {
                printf("%d", current->block_id);
            }
        } else {
            for (int i = 0; i < current->block_size; i++) {
                printf(".");
            }
        }
        current = current->next;
    }
    printf("\n");
}

bool is_minimised(fs_block_t* fs) {
    fs_block_t* current = fs;
    bool found_empty = false;

    while (current != NULL) {
        if (current->present && found_empty) {
            return false;
        }
        current = current->next;
    }

    return false;
}

fs_block_t* find_last_block(fs_block_t* head) {
    fs_block_t* current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    return current;
}

fs_block_t* merge_next(fs_block_t* block) {
    if (block->next == NULL) {
        return block;
    }
    if (block->next->present) {
        return block;
    }

    fs_block_t* next = block->next;
    block->block_size += next->block_size;
    block->next = next->next;
    if (next->next != NULL) {
        next->next->prev = block;
    }
    free(next);

    return block;
}

fs_block_t* merge_prev(fs_block_t* block) {
    if (block->prev == NULL) {
        return block;
    }
    if (block->prev->present) {
        return block;
    }

    fs_block_t* prev = block->prev;
    prev->block_size += block->block_size;
    prev->next = block->next;
    if (block->next != NULL) {
        block->next->prev = prev;
    }
    free(block);

    return prev;
}

void minimise_fs(fs_block_t* fs) {
    fs_block_t* last_block = find_last_block(fs);
    if (last_block == NULL) {
        return;
    }

    while (last_block != NULL && !is_minimised(fs)) {
        //Move the last block to the first empty space

        if (!last_block->present) {
            //Skip empty blocks
            last_block = last_block->prev;
        } else {
            //Find the first empty block that is large enough
            fs_block_t* current = fs;
            bool found = false;
            while (current != NULL) {
                if (current == last_block) { // Don't go past the last block
                    break;
                }
                if (!current->present && current->block_size >= last_block->block_size) {
                    found = true;
                    break;
                }
                current = current->next;
            }

            if (found) {
                uint16_t free_after = current->block_size - last_block->block_size;
                current->block_size = last_block->block_size;
                current->block_id = last_block->block_id;
                current->present = true;

                if (free_after != 0) {
                    fs_block_t* new_block = (fs_block_t*) malloc(sizeof(fs_block_t));
                    new_block->block_size = free_after;
                    new_block->present = false;
                    new_block->prev = current;
                    new_block->next = current->next;
                    current->next = new_block;
                    if (new_block->next != NULL) {
                        new_block->next->prev = new_block;
                    }
                }

                last_block->present = false;
                last_block = merge_prev(merge_next(last_block));
            } else {
                //No empty block is large enough, move on
                last_block = last_block->prev;
            }
        }
    }
}

uint64_t compute_checksum(fs_block_t* fs) {
    uint64_t checksum = 0;

    fs_block_t* current = fs;
    int current_offset = 0;

    while (current != NULL) {
        if (current->present) {
            for (int i = 0; i < current->block_size; i++) {
                checksum += current_offset * current->block_id;
                current_offset++;
            }
        } else {
            current_offset += current->block_size;
        }

        current = current->next;
    }

    return checksum;
}

int main() {
    printf("Reading file...\n");
    fs_block_t* fs = read_file("input.txt");
    if (fs == NULL) {
        printf("Error reading file\n");
        return 1;
    }

    //debug_print_fs(fs);
    minimise_fs(fs);
    //debug_print_fs(fs);
    uint64_t checksum = compute_checksum(fs);

    printf("Minimised checksum: %lu\n", checksum);

    free_fs(fs);
    return 0;
}
