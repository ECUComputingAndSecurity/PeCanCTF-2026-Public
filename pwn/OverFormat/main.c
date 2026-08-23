#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <limits.h>

char* get_flag() {
  FILE* fp = NULL;

  fp = fopen("flag.txt", "r");

  if (!fp) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  char *flag = malloc(41);
  if (!flag) {
    perror("maloc");
    exit(1);
  }

  fread(flag, 1, 40, fp);
  flag[41] = "\0";

  fclose(fp);

  return flag;
}

int main() {
  char thankyou_message[44] = "Thanks for your message, I will reply soon\n";
  char user_message[32];

  printf("Please submit your greviance:\n");
  fflush(stdout);
  
  gets(user_message);

  char *flag = get_flag();

  printf(thankyou_message);

  return 0;
}
