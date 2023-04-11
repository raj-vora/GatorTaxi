gatorTaxi: gatorTaxi.py $(FILE)
	python3 ./$< ./$< >$@
	chmod +x $@: