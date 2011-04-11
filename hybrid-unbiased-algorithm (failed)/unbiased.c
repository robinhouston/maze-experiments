#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <bitstring.h>

#define ROWS 10
#define COLS 10

#define REPETITIONS 100000

#define cell_row(cell) (cell / COLS)
#define cell_col(cell) (cell % COLS)
#define make_cell(row, col) (row * COLS + col)

int rand_lt(int n) {
  int mask = 1;
  while (mask <= n) mask = mask << 1;
  mask--;
  
  for (;;) {
    long r = random() & mask;
    if (r < n) return r;
  }
}

int random_cell() {
  return rand_lt(ROWS * COLS);
}

int random_neighbour(int cell) {
  int row = cell_row(cell),
      col = cell_col(cell);
  
  for (;;) {
    int new_row = row, new_col = col;
    switch(random() & 3) {
      case 0: new_row++; break;
      case 1: new_row--; break;
      case 2: new_col++; break;
      case 3: new_col--; break;
    }
    if (new_row >= 0 && new_col >= 0 && new_row < ROWS && new_col < COLS)
      return make_cell(new_row, new_col);
  }
}

void wilson(bitstr_t *cells_filled, int cell, int *num_steps_p, int *num_filled_p) {
  int path[ROWS * COLS];
  int path_len = 0;
  bitstr_t *path_set = bit_alloc(ROWS * COLS);
  
  while (!bit_test(cells_filled, cell)) {
    ++*num_steps_p;
    path[path_len++] = cell;
    bit_set(path_set, cell);
    cell = random_neighbour(cell);
    if (bit_test(path_set, cell)) {
      do {
        bit_clear(path_set, path[path_len - 1]);
        path_len--;
      } while (path[path_len] != cell);
    }
  }
  
  for (int i = 0; i < path_len; i++)
    bit_set(cells_filled, path[i]);
  *num_filled_p += path_len;
  free(path_set);
}

int num_steps(int threshold) {
  int num_filled = 0;
  int num_steps = 0;
  
  bitstr_t *cells_filled = bit_alloc(ROWS * COLS);
  int cell = random_cell();
  
  /* Do a random walk till we reach the threshold */
  while (num_filled < threshold) {
    if (!bit_test(cells_filled, cell)) {
      bit_set(cells_filled, cell);
      num_filled++;
    }
    cell = random_neighbour(cell);
    num_steps++;
  }
  
  /* Now do Wilson's algorithm till it's all filled */
  while (num_filled < ROWS * COLS) {
    bit_ffc(cells_filled, ROWS * COLS, &cell);
    if (cell < 0) break;
    wilson(cells_filled, cell, &num_steps, &num_filled);
  }
  
  free(cells_filled);
  return num_steps;
}

int main() {
  srandomdev();
  
  for (int threshold = 1; threshold < 100; threshold += 2) {
    int total_steps = 0;
    for (int j = 0; j < REPETITIONS; j++) {
      total_steps += num_steps(threshold);
    }
    printf("%d,%d\n", threshold, total_steps);
  }
  
  return 0;
}
