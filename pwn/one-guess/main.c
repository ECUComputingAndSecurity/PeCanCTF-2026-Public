#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <limits.h>

struct game {
  unsigned int target;
  unsigned int guess;
  int count;
};

void win() {
  FILE* fp = NULL;
  char flag[64];

  fp = fopen("flag.txt", "r");

  if (!fp) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  fread(flag, 1, 64, fp);

  printf("Right on the money! Here's the flag: %s.", flag);
}

void init_game(struct game *game) {
  int fd = open("/dev/urandom", O_RDONLY);

  if (fd < 0) {
    exit(EXIT_FAILURE);
  }

  read(fd, &game->target, sizeof(game->target));
  close(fd);

  game->count = 0;
}

void play_game(struct game *game) {
  printf("I'm thinking of a number between %u and %u.\n", 0, UINT_MAX);

  while (game->count < 1) {
    printf("What's your guess? ");

    if (scanf("%lu", &game->guess) < 1) {
      break;
    }

    if (game->guess < game->target)
      puts("Too low!");
    else if (game->guess > game->target)
      puts("Too high!");
    else
      win();

    ++game->count;
  }
}

int main() {
  struct game game;

  setbuf(stdout, NULL);

  init_game(&game);
  play_game(&game);

  puts("Try again later.");
}
