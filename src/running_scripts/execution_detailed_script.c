#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <time.h>
#include <sys/stat.h>

#include "model.h"
#include "sampler.h"
#include "../solvers/highsSolver.h"

#define TEMP_FOR(ATTR) \
    FILE *temp_##ATTR ;\
    if((temp_##ATTR = fopen("./results/tmp_"#ATTR".txt", "w+")) == NULL) {\
        perror("Error opening temp file. Exiting...") ;\
        exit(1) ;\
    }\
    changeOutputOf(ATTR, temp_##ATTR) ;\

#define FLUSH_CLOSE_AND_RENAME(ATTR) \
    if(fflush(temp_##ATTR) == EOF) {\
        perror("Error flushing temp file. Exiting...") ;\
        exit(1) ;\
    }\
    if(fclose(temp_##ATTR) == EOF) {\
        perror("Error closing temp file. Exiting...") ;\
        exit(1) ;\
    }\
    sprintf(lineBuffer, "./results/%s_"#ATTR"_detailed_%s_thr_%d.txt", arranged_name, names[j][q], ALGO_THRESHOLD) ;\ 
    if(rename("./results/tmp_"#ATTR".txt", lineBuffer) == -1) {\
        perror("Error renaming file. Please recover manually") ;\
        exit(1) ;\
    }\
    
#define REDIRECT_TO_NULL() {\
    changeOutputOf(costs, dev_null) ; \
    changeOutputOf(adjacencies, dev_null) ; \
    changeOutputOf(partitions, dev_null) ;} \

int TRIALS = 64 ;

DIR *directory ;
struct dirent *directory_struct ;

FILE *file ;

FILE *dev_null ;

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

int ALGO_THRESHOLD = 2 ;

int main(int argc, char **argv)
{
    if((dev_null = fopen("/dev/null", "r+")) == NULL) {
        perror("Unable to open /dev/null. Exiting... ") ;
        exit(1) ;
    }

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
                sprintf(lineBuffer, "./results/%s_times_detailed_%s_thr_%d.txt", arranged_name, names[j][q], ALGO_THRESHOLD) ;                

                struct stat buffer ;
                if(stat(lineBuffer, &buffer) == 0) {
                    fprintf(stderr, "Combination has already been processed. Skipping...\n") ;
                    continue ;
                }

                resetState() ;
                TEMP_FOR(costs) ;
                TEMP_FOR(adjacencies) ;
                TEMP_FOR(partitions) ;
                TEMP_FOR(times) ;

                if(instanceSize < 500) {
                    TRIALS = 64 ;
                }else if(500 <= instanceSize && instanceSize < 1000) {
                    TRIALS = 32 ;
                } else
                    TRIALS = 5 ;

                for(int k = 0; k < TRIALS; k++) {

                    if(k == 1) REDIRECT_TO_NULL() ;
                    resetState() ;
                    struct TSP_instance *instance = create_instance(instanceSize, costMatrix) ;

                    TSP_heuristic_algorithm(instance, derivation_functions[j][q], reconstruction_functions[j], highs_solver, ALGO_THRESHOLD) ;
                    printState() ;

                    if(check_instance_is_correct(instance) != 0 || check_instance_connection(instance) != 0)
                    {
                        fprintf(stderr, "Instance of file %s is not correct with policy combo %d,%d\n", nameBuffer, j, q) ;
                        failure = 1 ;

                        if(k == 0) {
                            fprintf(temp_adjacencies, "Cost : %e\n", 0.0) ;
                        }
                    }
                    else {
                        if(k == 0) {
                            fprintf(temp_adjacencies, "Cost : %e\n", get_solution_cost(instance)) ;
                        }
                    }

                    destroy_instance(instance) ;
                }

                FLUSH_CLOSE_AND_RENAME(costs) ;
                FLUSH_CLOSE_AND_RENAME(adjacencies) ;
                FLUSH_CLOSE_AND_RENAME(partitions) ;
                FLUSH_CLOSE_AND_RENAME(times) ;
            }

        free(costMatrix) ;
    }

    return failure ;
}