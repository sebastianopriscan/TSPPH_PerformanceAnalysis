if(WIN32)
        find_path(HIGHS_INCLUDE_DIR Highs.h
                PATHS
                ${HIGHS_SOURCE_DIR}/HiGHS/src
        )

        find_library(HIGHS_LIBRARIES NAMES highs
                PATHS
                ${HIGHS_SOURCE_DIR}/HiGHS/build/RELEASE/bin
        )
else(WIN32)
        find_path(HIGHS_INCLUDE_DIR Highs.h
                PATHS
                /usr/local/include/highs
                ${HIGHS_INSTALL_DIR}/include/highs
                ${HIGHS_SOURCE_DIR}/HiGHS/src
        )

        find_library(HIGHS_LIBRARIES NAMES highs
                PATHS
                /usr/local/lib
                ${HIGHS_INSTALL_DIR}/include/highs/interfaces
                ${HIGHS_SOURCE_DIR}/HiGHS/build/lib
        )
endif(WIN32)