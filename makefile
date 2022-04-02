lint:
	black .
	isort .
	flake8 .
act:
	conda activate crypto-cast