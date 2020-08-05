# CSCW Data Analysis, Mark II
Looking at the data from the CSCW paper, taking into account tweaks to processing scripts, the models and so forth.

**Last Update: 2020-08-05**

## Requirements
Run scripts using Python 3.7, and create a virtual environment with the packages listed in `requirements.txt`.

## Log Processor
The directory contains updated code for the log processor. Code is an update from the `cscw-markov` initial exploration. In this update, we take the processing script one step further, splitting the codebase out into separate modules, and introducing command-line arguments to make running different permutations easier.

To processor parses over the MongoDB log instance (for CSCW), and spits out a CSV file of counts for different search sessions. These counts vary depending on the configuration you pass via the command line.

From the `cscw-mk2` directory, launch the processor with the command

`python -m log_processor <config_file>`

Where `<config_file>` points to a configuration file. The script outputs to `stdout`, so you can pipe the output of the script to a file if you wish.