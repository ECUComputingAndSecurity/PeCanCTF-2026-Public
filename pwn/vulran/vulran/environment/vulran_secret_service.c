#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h> 
#include <unistd.h>

/*
* Author: Gina H., unpaid intern at Vulran
*/

const char *banner =
    "              _                     _       _             _          _       _     _              \n"
    " /\\   /\\_   _| |_ __ __ _ _ __     /_\\  ___| |_ _ __ __ _| |   /\\/\\ (_)_ __ (_)___| |_ _ __ _   _ \n"
    " \\ \\ / / | | | | '__/ _` | '_ \\   //_\\\\/ __| __| '__/ _` | |  /    \\| | '_ \\| / __| __| '__| | | |\n"
    "  \\ V /| |_| | | | | (_| | | | | /  _  \\__ \\ |_| | | (_| | | / /\\/\\ \\ | | | | \\__ \\ |_| |  | |_| |\n"
    "   \\_/  \\__,_|_|_|  \\__,_|_| |_| \\_/ \\_/___/\\__|_|  \\__,_|_| \\/    \\/_|_| |_|_|___/\\__|_|   \\__, |\n"
    "                                                                                            |___/ \n";

const char *help = 
    "Welcome to the Vulran Astral Ministry Secret Service.\n"
    "Author: Gina H., unpaid intern."
    "To get started, familiarise yourself with the following commands.\n"
    "  'auth' to authenticate.\n"
    "  'read' to read a document.\n"
    "  'readl' to read a document with a large file name.\n"
    "  'list' to list all documents.\n"
    "  'launch' to launch all nuclear missiles from Astral arsenal.\n"
    "  'exit' to exit the service.\n";
char password[32];

char *authSuccess = "Authentication success.";
char *authFail = "Authentication fail: incorrect password.";

int isAuthenticated = 0;


void welcome(){ 
    printf("%s\n", banner);
    printf("%s\n", help);
    char *t = "> ";
    printf("\n");
}

void load_password(){
    FILE *f = fopen("password.txt", "rb");
    if(f == NULL){
        perror("fopen");
        return;
    }
    size_t bytes_read = fread(password, 1, 31, f);
    
    if (ferror(f)) {
        perror("fread");
        fclose(f);
        return;
    }
    fclose(f);
}

typedef struct AuthStruct {  
    char input_password[32];
    int *isAuthenticatedLocation;
    char *outputMessage;
} AuthStruct;

int auth(){
    int retval = 0;
    AuthStruct s;
    s.isAuthenticatedLocation = &isAuthenticated;
    s.outputMessage = NULL;
    printf("Enter password: ");
    fgets(s.input_password, 48, stdin);
    
    if(*s.isAuthenticatedLocation == 1){
        printf("Already authenticated.\n");
        retval = 1;
        return retval;
    }

    if(s.outputMessage == NULL){
        int len = strlen(password);
        if(strncmp(s.input_password, password, len) == 0){
            isAuthenticated = 1;
            s.outputMessage = authSuccess;
        }else{
            isAuthenticated = 0;
            s.outputMessage = authFail;
        }
    }

    printf("%s\n", s.outputMessage);
     
}

FILE *open_allowed(const char *path)
{
    if(strchr(path, '/') != NULL)
        goto NICE_TRY;

    struct stat requested, flag;

    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd == -1)
        return NULL;

    if (fstat(fd, &requested) == -1 ||
        stat("./flag/flag.txt", &flag) == -1 ||
        (requested.st_dev == flag.st_dev &&
         requested.st_ino == flag.st_ino)) {
        close(fd);
        NICE_TRY:
            printf("nice try lol\n");
            return NULL;
    }

    FILE *file = fdopen(fd, "r");
    if (file == NULL)
        close(fd);

    return file;
}

void displayFile(char *fileName){
    FILE *file = open_allowed(fileName);
    if(file == NULL) return;
    char buffer[1024];
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        fwrite(buffer, 1, bytes_read, stdout);
    }

    if (ferror(file))
        perror("Error reading file");

    fclose(file);
}

typedef struct ReadFileState { 
    char buffer[32];
    int shortMode;
    char *whitelist[4];
    char *blacklist[4];
} ReadFileState;

int readFile(int longFileName){
    int retval = 0;
    ReadFileState s;
    char *bufLocation;
    size_t size;
    
    s.shortMode = !longFileName; 
    
    if(s.shortMode){ 
        if(!isAuthenticated) {
            printf("Please authenticate first.\n");
            return 1;
        }
        bufLocation = s.buffer;
    }else{
        bufLocation = malloc(128);
    }
    
    s.blacklist[0] = "password.txt";
    s.blacklist[1] = "launch_codes.txt";
    s.blacklist[2] = "presidents_search_history.txt";
    s.blacklist[3] = "vulran_secret_service.c";
    
    s.whitelist[0] = "vulran_secret_service";
    s.whitelist[1] = "enemies_of_the_state.txt";
    s.whitelist[2] = "how_to_defend_against_the_sky_creatures.txt";
    s.whitelist[3] = "last_words.txt";

    printf("Enter the name of document you'd like to read. Type \"done\" to finish.\n");
    
    while(1) {
        LOOP:
        printf("read ");
        printf("> ");
        int size = s.shortMode ? 33 : 128;
        fgets(bufLocation, size, stdin); 
        bufLocation[strcspn(bufLocation, "\r\n")] = '\0';
        int isDone = strncmp(bufLocation, "done", 4) == 0;
        if(isDone) break;
        size_t len = strlen(bufLocation);
        for(int i = 0; i < 4; i++)
            if(len == strlen(s.blacklist[i]) && strncmp(bufLocation, s.blacklist[i], len)==0){
                printf("Sorry, this document is blacklisted from reading.\n"); 
                goto LOOP;
            }
        
        int isWl = 0;
        for(int i = 0; i < 4; i++){
            if(len == strlen(s.whitelist[i]) && strncmp(bufLocation, s.whitelist[i], len) == 0){
                isWl = 1;
                break;
            }
        }
        if(!isWl){
            printf("Sorry, this document is not whitelisted for reading.\n");
            continue;
        }
        displayFile(bufLocation); 
    }
    return retval;
}

void win(void){
    char flag[128];

    FILE *file = fopen("./flag/flag.txt", "r");
    if (file == NULL) {
        perror("fopen");
        return;
    }

    size_t count = fread(flag, 1, 127, file);
    flag[count] = '\0';

    printf("%s\n", flag);
    fclose(file);
}

void launch(){
    char buffer[64];
    char input[64];
    printf("Enter the nuclear launch codes: \n");
    printf("launch > ");
    fgets(input, 64, stdin); 
    size_t len1 = strlen(input);
    if(input[len1-1] == '\r' || input[len1-1] == '\n'){
        len1--;
        input[len1] = '\0';
    }
    FILE *file = fopen("launch_codes.txt", "r"); 
    if(file == NULL) {
        perror("fopen");
        return;
    }
    size_t count = fread(buffer, 1, 16, file);
    buffer[count] = '\0';
    fclose(file);
    size_t len2 = strlen(buffer);
    if(len1 == len2 && strncmp(input, buffer, len1) == 0){
        char flag_buffer;
        printf("Initiating attack...\n");
        win();
    }else{
        printf("Incorrect launch code.\n");
    }
}

void list(){
    printf("Documents on system: \n"); 
    printf("    presidents_search_history.txt\n");
    printf("    enemies_of_the_state.txt\n");
    printf("    vulran_secret_service\n");
    printf("    password.txt\n");
    printf("    launch_codes.txt\n");
    printf("    vulran_secret_service.c\n");
    printf("    how_to_defend_against_the_sky_creatures.txt\n");
    printf("    last_words.txt\n");
    return; 
}

void processCommand(char *command){
    if(strncmp(command, "auth", 4) == 0){
        auth(); 
        return;
    }else if(strncmp(command, "readl", 5) == 0){
        readFile(1);
        return;
    }else if(strncmp(command, "read", 4) == 0){
        readFile(0);
        return;
    }else if(strncmp(command, "list", 4) == 0){
        list();
        return;
    }else if(strncmp(command, "launch", 5) == 0){
        launch();         
        return;
    }
}

int main(){

    setvbuf(stdout, NULL, _IONBF, 0);  

    load_password();
    welcome();
    int isExit = 0; 
        
    char command[8];

    while(1){
        printf("> ");
        fgets(command, 8, stdin);
        isExit = strncmp(command, "exit", 4) == 0;
        if(isExit) break;
        processCommand(command);
    }

    return 0;
}
