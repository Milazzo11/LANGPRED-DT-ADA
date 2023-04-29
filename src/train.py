"""
Train new model.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


import build_data
import pickle
import sys
from build_DT import build_DT
from build_ADA import build_ADA


NUM_MODELS = 10
# the number of models to train
# (multiple models can be created using different random partitioning of the
# train_set and test_set, and this allows for a better idea of a model's true
# accuracy when viewing new data) -- the final model will then be trained using
# all available data


DT_MAX_DEPTH = 5
# maximum depth for the DT model type


ADA_NUM_TREES = 6
# number of trees to build for the ADA model type


def build_model(mode: str, data: list):
    """
    Builds a model.
    """
    
    if mode == "dt":
        model = build_DT(data, DT_MAX_DEPTH)
    else:
        model = build_ADA(data, "en", "nl", ADA_NUM_TREES)
        
    return model


def model_eval(data_file: str, mode: str) -> None:
    """
    Generates several models and finds the average accuracy as an evaluation.
    """

    accuracy_total = 0
    
    for x in range(NUM_MODELS):
        print(f"MODEL {x + 1} of {NUM_MODELS}:")
        print("Fetching data...")
        
        data = build_data.build_data(data_file)
        train_set, test_set = build_data.train_test_split(data)
        train_set = build_data.set_default_weights(train_set)
        # builds formatted training/testing data lists
        
        print("Training model...")
        model = build_model(mode, train_set)
            
        print("Evaluating model...")
        accuracy = model.eval(test_set)
        
        print(f"Accuracy: {round(accuracy * 100, 2)}%\n")
        accuracy_total += accuracy

    print(f"Mean accuracy of trained models:")
    print(f"{round((accuracy_total / NUM_MODELS) * 100, 2)}%\n")   
    

def save_model(data_file: str, save_file: str, mode: str) -> None:
    """
    Builds and saves the final model using all available data.
    """
    
    data = build_data.build_data(data_file)
    data = build_data.set_default_weights(data)
    # builds full formatted dataset
    
    print("Generating final model...")
    model = build_model(mode, data)
    
    print("Saving model...")
    model.minimize()

    with open(save_file, "wb") as f:
        pickle.dump(model, f)
        
    print(f'Model "{save_file}" saved.') 


def main(args: list) -> None:
    """
    Program entry point.
    """
    
    model_eval(args[0], args[2])
    save_model(args[0], args[1], args[2])
    

if __name__ == "__main__":
    num_args = 4
    args = sys.argv
    # gets arguments and defines expected argument length
    
    if len(args) == num_args:
        main(args[1:])
        # calls main with command line arguments
        
    else:
        print("usage: py train.py <examples> <hypothesisOut> <learning-type>")