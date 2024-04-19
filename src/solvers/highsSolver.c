#include "highsSolver.h"
#include "interfaces/highs_c_api.h"

#include <math.h>

static inline unsigned char isPowOfTwo(unsigned int i, unsigned long node_number)
{
    i = ~(ULONG_MAX << node_number) & i ;
    return (i > 0) & ((i & (i-1)) == 0);
}

void highs_solver(struct TSP_instance *instance, unsigned char relaxed)
{
    if(instance->nodes == 2)
    {
        instance->adjacencies[instance->nodes * 0 + 1] = 1 ;
        instance->adjacencies[instance->nodes * 1 + 0] = 1 ;
        return ;
    }

    int numCol = (int)(instance->nodes * instance->nodes - instance->nodes) ;

    int numRows, numNz ;
    if(relaxed == RELAXED)
    {
        numRows = 2*(int)instance->nodes ;
        numNz = 2*(int)(instance->nodes * (instance->nodes -1)) ;
    }
    else if (relaxed == NOT_RELAXED)
    {
        numRows = (int) pow(2, (double) instance->nodes) -2 ;
        numNz = (int)(instance->nodes*(instance->nodes -1))*((int) pow(2, (double) (instance->nodes -2))) ;
    }
    else
    {
        perror("Error, only RELAXED/NON RELAXED macros can be passed. Exiting...") ;
        exit(1) ;
    }

    int sense = kHighsObjSenseMinimize ;
    const double offset = 0 ;

    double *col_cost ;

    if((col_cost = malloc(sizeof(double)*numCol)) == NULL)
    {
        perror("Error in allocating costs vector. Exiting...") ;
        exit(1) ;
    }

    double *colLower ;

    if((colLower = malloc(sizeof(double)*numCol)) == NULL)
    {
        perror("Error in allocating costs vector. Exiting...") ;
        exit(1) ;
    }

    double *colUpper ;

    if((colUpper = malloc(sizeof(double)*numCol)) == NULL)
    {
        perror("Error in allocating costs vector. Exiting...") ;
        exit(1) ;
    }

    double *row_lower ;

    if((row_lower = malloc(sizeof(double)*numRows)) == NULL)
    {
        perror("Error in allocating costs vector. Exiting...") ;
        exit(1) ;
    }

    double *row_upper ;

    if((row_upper = malloc(sizeof(double)*numRows)) == NULL)
    {
        perror("Error in allocating costs vector. Exiting...") ;
        exit(1) ;
    }

    int *integralities ;

    if((integralities = malloc(sizeof(int) * numCol)) == NULL)
    {
        perror("Error in allocating ''A'' matrix. Exiting...") ;
        exit(1) ;
    }

    const int a_format = kHighsMatrixFormatColwise ;

    int *a_start ;

    if((a_start = malloc(sizeof(int) * numCol)) == NULL)
    {
        perror("Error in allocating ''A'' matrix. Exiting...") ;
        exit(1) ;
    }

    double *a_value ;

    if((a_value = malloc(sizeof(double) * numNz)) == NULL)
    {
        perror("Error in allocating ''A'' matrix. Exiting...") ;
        exit(1) ;
    }

    int *a_index ;

    if((a_index = malloc(sizeof(int) * numNz)) == NULL)
    {
        perror("Error in allocating ''A'' matrix. Exiting...") ;
        exit(1) ;
    }

    int in_col_idx_counter = 0 ;
    unsigned int cursor = 0;
    for (unsigned long i = 0 ; i < instance->nodes ; i++)
    {
        for (unsigned long j = 0 ; j < instance->nodes ; j++) //This double loop is used to compile the 'A' matrix, the cost vector and the integralities
        {
            if(i != j)
            {
                //Setting up cost values and integralities
                colLower[cursor] = 0 ;
                colUpper[cursor] = 1.0 ;
                col_cost[cursor] = get_connection_cost(instance, i, j) ;
                integralities[cursor] = kHighsVarTypeInteger ;

                //To avoid unnecessary extra looping, we piggyback from here row compilation
                if(cursor < (unsigned int) numRows)
                {
                    row_lower[cursor] = 1.0 ;
                    if(relaxed == RELAXED || isPowOfTwo(cursor+1, instance->nodes) || isPowOfTwo(~(cursor+1), instance->nodes))
                        row_upper[cursor] = 1.0 ;
                    else
                        row_upper[cursor] = 1.0e30 ;
                }

                //'A' matrix compilation column wise : for every column we scan all partitions represented as a bitmask q, then we seek
                //if the arc represented by i and j is exiting from the partition, if so it is registered in a_start and a_value
                a_start[cursor] = in_col_idx_counter ;

                if(relaxed == RELAXED)
                {
                    a_index[in_col_idx_counter++] = (int) i ;
                    a_index[in_col_idx_counter++] = (int) (instance->nodes + j) ;
                }
                else
                {
                    for (int q = 1 ; q <= numRows ; q++) {

                        int i_mask = (1 << i) ;
                        int j_mask = (1 << j) ;

                        if((q & i_mask) && !(q & j_mask))
                        {
                            a_index[in_col_idx_counter] = q -1 ;
                            in_col_idx_counter ++ ;
                        }
                    }
                }

                //All the non-zeros in 'A' have value 1, still piggybacking on the main loop
                if(cursor < (unsigned int) numNz)
                {
                    a_value[cursor] = 1 ;
                }

                cursor ++ ;
            }
        }
    }

    //Exhausting the remaining rows and non-zeroes to set
    for (unsigned int i = cursor ; i < (unsigned int) numRows ; i++, cursor++)
    {
        row_lower[i] = 1.0 ;
        if(relaxed == RELAXED || isPowOfTwo(cursor+1, instance->nodes) || isPowOfTwo(~(cursor+1), instance->nodes))
            row_upper[i] = 1.0 ;
        else
            row_upper[i] = 1.0e30 ;

        if(i < (unsigned int)numNz)
        {
            a_value[i] = 1 ;
        }
    }

    //Exhausting the remaining non-zeroes to set
    for (unsigned int i = cursor ; i < (unsigned int) numNz ; i++)
    {
        a_value[i] = 1 ;
    }

    double* col_value ;

    if((col_value = malloc(sizeof(double) * numCol)) == NULL)
    {
        perror("Error in allocating column solution array. Exiting...") ;
        exit(1) ;
    }

    double* row_value ;

    if((row_value = (double*)malloc(sizeof(double) * numRows)) == NULL)
    {
        perror("Error in allocating column solution array. Exiting...") ;
        exit(1) ;
    }

    int model_status;
    int run_status;

    run_status = Highs_mipCall(numCol, numRows, numNz, a_format,
                               sense, offset, col_cost, colLower, colUpper, row_lower, row_upper,
                               a_start, a_index, a_value, integralities,
                               col_value, row_value,
                               &model_status);

    if(run_status != kHighsStatusOk || model_status != kHighsModelStatusOptimal)
    {
        perror("Error in solving MIP model. Exiting...") ;
        exit(1) ;
    }

    cursor = 0 ;
    for (unsigned long i = 0 ; i < instance->nodes ; i++)
    {
        for (unsigned long j = 0; j < instance->nodes; j++)
        {
            if (i != j)
            {
                instance->adjacencies[instance->nodes * i + j] = (unsigned char) col_value[cursor] ;
                cursor++ ;
            }
        }
    }

    free(col_cost) ;
    free(colLower) ;
    free(colUpper) ;
    free(row_lower) ;
    free(row_upper) ;
    free(integralities) ;
    free(a_start) ;
    free(a_value) ;
    free(a_index) ;
    free(col_value) ;
    free(row_value) ;
}