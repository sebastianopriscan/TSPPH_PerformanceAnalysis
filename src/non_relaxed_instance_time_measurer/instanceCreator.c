#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    if(argc != 5)
    {
        fprintf(stderr, "Usage: ./exName seed number size path\n") ;
        exit(1) ;
    }

    char *endptr ;

    int seed, number, size ;

    seed = strtol(argv[1], &endptr, 10) ;

    if(*endptr != '\0') return 1 ;

    number = strtol(argv[2], &endptr, 10) ;

    if(*endptr != '\0') return 1 ;

    size = strtol(argv[3], &endptr, 10) ;

    if(*endptr != '\0') return 1 ;

    srand(seed) ;

    char *filename ;

    int nameSize = strlen(argv[1]) + strlen(argv[2]) + strlen(argv[3]) + 2 +4 ;

    if((filename = malloc(sizeof(char) * (nameSize +1 + strlen(argv[4])))) == NULL)
    {
        perror("Error in allocating memory") ;
        exit(1) ;
    }

    char *position = stpcpy(filename, argv[4]) ;
    position = stpcpy(position, argv[1]) ;
    *position = '_' ;
    position++ ;
    position = stpcpy(position, argv[2]) ;
    *position = '_' ;
    position++ ;
    position = stpcpy(position, argv[3]) ;
    stpcpy(position, ".txt") ;

    printf("%s\n", filename) ;

    FILE *file ;

    if((file = fopen(filename, "w")) == NULL)
    {
        perror("Error in opening file") ;
        exit(1) ;
    }

    fprintf(file, "%s %s\n", argv[2], argv[3]) ;

    for (int count = 0 ; count < number ; count++)
    {
        for (int i = 0; i < size; i++)
        {
            for (int j = 0; j < size; j++)
            {
                if(i == j)
                {
                    fprintf(file, "%d ", 0) ;
                }
                else
                {
                    int num = rand() % 10000 ;
                    fprintf(file, "%d ", num) ;
                }
            }

            fprintf(file, "\n") ;
        }

        fprintf(file, "\n") ;
    }

}