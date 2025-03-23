# Mimir

Mimir is a data extractor for git (primarily GitHub) repositories.

Mimir looks through all the code (currently only Java) files. It extracts information
on the code files such as packages, classes, annotations, methods, etc.

After it extracts this information using `tree-sitter` it leverages `PyDriller` to extract
git information for the code files, iterating over every commit for the project.

Finally, Mimir saves this extracted information in a JSON file for future use and analysis.

## Installation

Dependencies:
- `python 3.13+`
- `git`

Clone the repository:

`git clone https://github.com/consulthunter/mimir`

Create a python 3.13+ virtual environment:

`python -m venv venv`

Activate the virtual environment and install the requirements:

`source venv/bin/activate`

`pip install -r requirements.txt`

Create the config:

`python main.py create-config --config config\default-config.json`

Run the example:

`python main.py collect-info --config config\default_config.json`

Check the `/output/` directory for the `data.json`

