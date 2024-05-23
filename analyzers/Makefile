.PHONY : venv install-deps

venv : ./analyzers/virt_env/bin/activate

./analyzers/virt_env/bin/activate :
	python3 -m venv ./analyzers/virt_env

install-deps :
	pip install scikit-learn
	pip install matplotlib
	pip install PyQt6