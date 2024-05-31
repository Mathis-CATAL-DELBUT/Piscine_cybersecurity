#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    char local_4c, local_4b, local_4a, local_49;
    char local_48[31];
    char local_29[9];
    unsigned long local_20;
    int local_18, local_14, local_10;
    int iVar2;
    size_t sVar3;
    unsigned long uVar1;
    int bVar4;

    printf("Please enter key: ");
    local_10 = scanf("%30s", local_48);
    if (local_10 != 1) {
        printf("Nope.\n");
        return 1;
    }
    if (local_48[1] != '2') {
        printf("Nope.\n");
        return 1;
    }
    if (local_48[0] != '4') {
        printf("Nope.\n");
        return 1;
    }
    fflush(stdin);
    memset(local_29, 0, 9);
    local_29[0] = '*';
    local_49 = 0;
    local_20 = 2;
    local_14 = 1;

    while (1) {
        sVar3 = strlen(local_29);
        uVar1 = local_20;
        bVar4 = 0;
        if (sVar3 < 8) {
            sVar3 = strlen(local_48);
            bVar4 = uVar1 < sVar3;
        }
        if (!bVar4) break;

        local_4c = local_48[local_20];
        local_4b = local_48[local_20 + 1];
        local_4a = local_48[local_20 + 2];
        char letter[4] = {local_4c, local_4b, local_4a, '\0'};
        iVar2 = atoi(letter);
        local_29[local_14] = (char)iVar2;
        local_20 += 3;
        local_14++;
    }
    local_29[local_14] = '\0';
    local_18 = strcmp(local_29, "********");
    if (local_18 == 0) {
        printf("Good job.\n");
        return 0;
    } 
    else
        printf("Nope.\n");
    return 1;
}
