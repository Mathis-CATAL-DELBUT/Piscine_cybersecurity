#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char buf[2048];
    printf("Please enter key: ");
    scanf("%s", buf);
    if (strcmp(buf, "__stack_check") == 0) 
        printf("Good job.\n");
    else
        printf("Nope.\n");
}
