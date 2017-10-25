#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) 
{ 
    int flags, opt;
    int i,arglen;

    while ((opt = getopt(argc, argv, "h")) != -1) {
	switch (opt) {
	case 'h':
	default: /* '?' */
	    fprintf(stderr, "Usage: %s [-h] words\n",
		    argv[0]);
	    exit(EXIT_FAILURE);
	}
    }

    if (optind >= argc) {
	fprintf(stderr, "Expected argument. Use -h option for usage.\n");
	exit(EXIT_FAILURE);
    }
    arglen = strlen(argv[optind]);
    for (i = 0; i < arglen; i++) {
	printf("%c ", argv[optind][i]);
    }
    printf("\n");
    for (i = 1; i < arglen; i++) {
	printf("%c \n", argv[optind][i]);
    }

    /* Other code omitted */

    exit(EXIT_SUCCESS);
}
