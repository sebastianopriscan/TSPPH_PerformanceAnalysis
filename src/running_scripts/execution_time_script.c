#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <time.h>
#include <sys/stat.h>

#include "model.h"
#include "../solvers/highsSolver.h"

#define TRIALS 64

DIR *directory ;
struct dirent *directory_struct ;

FILE *file ;

char nameBuffer[4096] ;
char *position ;

int derivation_functions_types = 3, reconstruction_functions_types = 2 ;

double *(*(derivation_functions[2][3]))(struct TSP_instance *, struct partitions *) = {{min_derivation_function_minRec,
                                                                                      max_derivation_function_minRec,
                                                                                      average_derivation_function_minRec},
                                                                                     {min_derivation_function_saving,
                                                                                      max_derivation_function_saving,
                                                                                      average_derivation_function_saving}} ;

void (*(reconstruction_functions[2]))(struct meta_TSP_instance *) = {min_reconstruction_function,
                                                                    saving_reconstruction_function
                                                                   } ;

char *names[2][3] = {{"min_min",
                    "max_min",
                    "avg_min"},
                    {"min_sav",
                     "max_sav",
                     "avg_sav"}} ;


char lineBuffer[1048576] ;
char arranged_name[4096] ;

int failure = 0;

int ALGO_THRESHOLD = 3 ;

int main(int argc, char **argv)
{
    if(argc == 2) 
        ALGO_THRESHOLD = (int) strtol(argv[1], NULL, 10) ;

    position = stpcpy(nameBuffer, "./formatted_instances/") ;
    if((directory = opendir("./formatted_instances")) == NULL)
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

        int instanceSize ;
        char *nptr, *token ;

        fgets(lineBuffer, 1048576, file) ;

        instanceSize = (int) strtol(lineBuffer, &nptr, 10) ;

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

                costMatrix[j * instanceSize + q] = strtol(token, &nptr, 10) ;

                token = strtok(NULL, " ") ;
            }

            fgets(lineBuffer, 1048576, file) ;
        }


        for (int j = 0 ; j < reconstruction_functions_types ; j++)
            for (int q = 0 ; q < derivation_functions_types ; q++)
            {
                strcpy(arranged_name, directory_struct->d_name) ;
                arranged_name[strlen(directory_struct->d_name) -4] = '\0' ;
                sprintf(lineBuffer, "./results/%s_time_%s_thr_%d.txt", arranged_name, names[j][q], ALGO_THRESHOLD) ;                

                struct stat buffer ;
                if(stat(lineBuffer, &buffer) == 0) {
                    fprintf(stderr, "Combination has already been processed. Skipping...\n") ;
                    continue ;
                }

                FILE *temp ;

                if((temp = fopen("./results/tmp.txt", "w+")) == NULL) {
                    perror("Error opening temp file. Exiting...") ;
                    exit(1) ;
                }
                struct TSP_instance *instance = create_instance(instanceSize, costMatrix) ;

                for(int k = 0; k < TRIALS; k++) {

                    struct timespec time_start, time_end ;
                    clock_gettime(CLOCK_BOOTTIME, &time_start) ;
                    
                    TSP_heuristic_algorithm(instance, derivation_functions[j][q], reconstruction_functions[j], highs_solver, 2) ;

                    clock_gettime(CLOCK_BOOTTIME, &time_end) ;

                    long long elapsed_time = (time_end.tv_sec - time_start.tv_sec) * 1000000000LL +
                        time_end.tv_nsec - time_start.tv_nsec ;

                    fprintf(temp, "%lld\n", elapsed_time) ;
                }

                if(fflush(temp) == EOF) {
                    perror("Error flushing temp file. Exiting...") ;
                    exit(1) ;
                }

                if(fclose(temp) == EOF) {
                    perror("Error closing temp file. Exiting...") ;
                    exit(1) ;
                }


                if(rename("./results/tmp.txt", lineBuffer) == -1) {
                    perror("Error renaming file. Please recover manually") ;
                    exit(1) ;
                }
                
                if(check_instance_is_correct(instance) != 0 || check_instance_connection(instance) != 0)
                {
                    fprintf(stderr, "Instance of file %s is not correct with policy combo %d,%d\n", nameBuffer, j, q) ;
                    failure = 1 ;
                }
                destroy_instance(instance) ;
            }

        free(costMatrix) ;
    }

    return failure ;
}