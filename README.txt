<< SEE "WRITEUP.txt" FOR WRITEUP >>

This program trains a decision tree or boosted ensemble model for the purpose
of predicting if a 15 word line of text is from the Dutch or English language.

The source code containing the "train.py" and "predict.py" modules is located
in the "src" folder, and the conglomeration of Wikipedia articles, the training
dataset, and the code used to construct the training dataset from the articles
is in the "data" folder.  The training dataset — "data.txt" — is also copied in
the "src" folder.

To use the training module, enter the command:
py train.py <examples> <hypothesisOut> <learning-type>

To use the predict module, enter the command:
py predict.py <hypothesis> <file>

The model files are stored using Python's pickle object serialization module,
and so it is recommended that these files be stored with the ".pkl" extension;
although this is not stricly necessary.

Because training a new model is a quick process, the program, by default, trains
10 test models for each run of the "train.py" module.  This can be easily
changed by assigning a new value to the "NUM_MODELS" global constant at the top
of the "train.py" module.  Training more models allows for a better prediction
of model accuracy when evaluating unseen data.  The final model is then trained
using all available data.

Also included are the "dt.pkl" "ada.pkl" and "test.txt" files — the ".pkl"
files are models that have been previously trained on the dataset and can be
used for prediction, and the "test.txt" file is a test prediction file
containing 15 word English and Dutch lines of text that can be fed into
"predict.py" to test a model.