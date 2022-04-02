lint:
	black .
	isort .
	flake8 .
act:
	source ~/miniconda3/etc/profile.d/conda.sh
	conda init zsh
	conda activate crypto-cast
update-env:
	conda env export > conda_env.yaml