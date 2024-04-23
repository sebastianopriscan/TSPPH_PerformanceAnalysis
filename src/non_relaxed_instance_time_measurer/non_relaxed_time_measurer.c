#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <time.h>

#include "model.h"
#include "../solvers/highsSolver.h"

#define PRINT_LOOP(PTR, SIZE, STREAM) {\
        for(int j = 0 ; j < SIZE ; j++) {\
            for(int q = 0 ; q < SIZE ; q++) {\
                fprintf(STREAM, "%d; ", PTR[j*SIZE + q]) ;\
            }\
            fprintf(STREAM, "\n") ;\
        }}\

#define TRIALS 64

DIR *directory ;
struct dirent *directory_struct ;

FILE *file ;

char nameBuffer[4096] ;
char *position ;

char lineBuffer[1048576] ;
char arranged_name[4096] ;

int failure = 0;

int main(void)
{

    FILE *time_results, *adjacencies ;

    if((time_results = fopen("./extra/time_results.txt", "w+")) == NULL) {
        perror("Error opening time_results file. Exiting...") ;
        exit(1) ;
    }
    if((adjacencies = fopen("./extra/time_adjacencies.txt", "w+")) == NULL) {
        perror("Error opening time_results file. Exiting...") ;
        exit(1) ;
    }

    fprintf(time_results, "Filename ; Size ; Time ; Cost\n") ;

    position = stpcpy(nameBuffer, "./extra/time_measurement/") ;
    if((directory = opendir("./extra/time_measurement")) == NULL)
    {
        perror("Error in opening resources dir, Exiting...") ;
        exit(1) ;
    }

    while ((directory_struct = readdir(directory)) != NULL)
    {
        if(strcmp(directory_struct->d_name, ".") == 0|| strcmp(directory_struct->d_name, "..") == 0)
            continue;

        strcpy(position, directory_struct->d_name) ;
    
        if((file = fopen(nameBuffer, "r")) == NULL)
        {

            fprintf(stderr, "Error opening file %s ", nameBuffer) ;
            perror("") ;
            exit(1) ;
        }

        int numberOfInstances, instanceSize ;

        fgets(lineBuffer, 1048576, file) ;

        char *token = strtok(lineBuffer, " ") ;

        if(token == NULL)
        {
            fprintf(stderr, "Wrong string format") ;
            exit(1) ;
        }

        char *nptr ;

        numberOfInstances = (int) strtol(token, &nptr, 10) ;

        if(*nptr != '\0' || nptr == token)
        {
            perror("Wrong string format") ;
            exit(1) ;
        }

        token = strtok(NULL, "\n") ;
        instanceSize = (int) strtol(token, &nptr, 10) ;

        if(*nptr != '\0' || nptr == token)
        {
            perror("Wrong string format") ;
            exit(1) ;
        }

        for(int i = 0; i < numberOfInstances; i++) {

            double *costMatrix ;

            if((costMatrix = malloc(sizeof (double) * instanceSize * instanceSize)) == NULL)
            {
                perror("Error allocating instance memory") ;
                exit(1) ;
            }

            fgets(lineBuffer, 1048576, file) ;

            for (int j = 0; j < instanceSize ; j++)
            {
                token = strtok(lineBuffer, " ") ;

                for (int q = 0; q < instanceSize ; q++)
                {
                    if(token == NULL)
                    {
                        perror("Wrong string format") ;
                    }

                    costMatrix[j * instanceSize + q] = (double) strtol(token, &nptr, 10) ;

                    token = strtok(NULL, " ") ;
                }

                fgets(lineBuffer, 1048576, file) ;
            }

            struct TSP_instance *instance = create_instance(instanceSize, costMatrix) ;

            struct timespec time_start, time_end ;
            clock_gettime(CLOCK_BOOTTIME, &time_start) ;
            
            TSP_heuristic_algorithm(instance, min_derivation_function_minRec, min_reconstruction_function, highs_solver, 1000000) ;

            clock_gettime(CLOCK_BOOTTIME, &time_end) ;

            long long elapsed_time = (time_end.tv_sec - time_start.tv_sec) * 1000000000LL +
                time_end.tv_nsec - time_start.tv_nsec ;

            double cost = get_solution_cost(instance) ;

            fprintf(time_results, "%s_%d ; %d ; %lld ; %e\n", nameBuffer, i ,instanceSize, elapsed_time, cost) ;

            fprintf(adjacencies, "%s_%d\n", nameBuffer, i) ;

            PRINT_LOOP(instance->adjacencies, instanceSize, adjacencies) ;

            if(fflush(time_results) == EOF) {
                perror("Error flushing temp file. Exiting...") ;
                exit(1) ;
            }
            if(fflush(adjacencies) == EOF) {
                perror("Error flushing temp file. Exiting...") ;
                exit(1) ;
            }
            
            if(check_instance_is_correct(instance) != 0 || check_instance_connection(instance) != 0)
            {
                fprintf(stderr, "Instance of file %s is not correct\n", nameBuffer) ;
                failure = 1 ;
            }
            destroy_instance(instance) ;

            free(costMatrix) ;
        }
    }

    return failure ;
}