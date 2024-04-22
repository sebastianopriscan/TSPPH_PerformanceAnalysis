.PHONY : performance_scripts_build

performance_scripts_build :
	cmake -S ./src -B ./src/build -DHIGHS_SOURCE_DIR=${HIGHS_SOURCE_DIR} -DHIGHS_INSTALL_DIR=${HIGHS_INSTALL_DIR}
	cmake --build ./src/build