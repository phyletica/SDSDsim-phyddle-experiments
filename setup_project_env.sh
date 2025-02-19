#! /bin/bash

set -e

# Get path to directory of this script
project_dir="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

conda_env_path="${project_dir}/env/conda-env.yml"
conda_env_name="SDSD-phyddle"

conda_exe="conda"
if [ -n "$(command -v mamba)" ]
then
    conda_exe="mamba"
fi

echo ""
echo "Creating project conda environment using '$(which $conda_exe)'..."
echo ""
"$conda_exe" env create --name "$conda_env_name" --file "$conda_env_path"


echo ""
echo "Activating project conda environment..."
echo ""
eval "$(conda shell.bash hook)"
conda activate "$conda_env_name"

echo ""
echo "Adding pydot_ng requirement via pip..."
echo ""
python -m pip install pydot_ng

echo ""
echo "Cloning SDSDsim..."
echo ""
git clone git@github.com:phyletica/SDSDsim.git
(
    cd SDSDsim
    git checkout main
    git pull
    echo "Installing SDSDsim within cond env '$conda_env_name' using '$(which python)'"
    python -m pip install -e .
)

echo ""
echo "Cloning phyddle..."
echo ""
git clone git@github.com:mlandis/phyddle.git
(
    cd phyddle
    git checkout main
    git pull
    echo "Installing phyddle within cond env '$conda_env_name' using '$(which python)'"
    python -m pip install -e .
)
