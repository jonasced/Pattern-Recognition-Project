from classifier import *


def hmm_test(HMM_Models, test_data, test_labels, useprint=True):
    """
    Inputs:
        1) List of Class Models
        2) test data [k] [r] > collection of test data containing features, k = number of class r= number of sample per class:
        classlist[ samplelist[ features in np.array format ] ]
        3) list of class labels of test classes in test data
    Output:
        1) array of classification accuracy for each test class
        2) list of label lists that each lists contains the result labels of a specific test class that classifier labeled as
        for example:
            first class has 10 samples
            each sample is labeled with classifier
            first list in results_labels_list will contain the labels that classifier decided on the samples of that test class


    """
    # Vary function depending on if list of model or single model is being evaluated
    if str(type(HMM_Models)) == "<class 'PattRecClasses.HMM_TA.HMM'>":
        num_class = 1
    elif str(type(HMM_Models)) == "<class 'list'>":
        num_class = len(HMM_Models)
    else:
        raise Exception("Invalid input model type: ", type(HMM_Models), ", should be either list or HMM.")

    accuracies = np.zeros(num_class)
    result_labels_list = []

    if useprint:
        print("************* CLASSIFICATION RESULTS ************* ")

    for char in range(num_class):
        
        result_labels = []
        samples = test_data[char]
        num_samples = len(samples)
        truth_label = test_labels[char]
        correct_count = 0
        # for each sample I am calculating the classification result label and compare it with its true label. If they
        # are equal, it is classified correctly
        for sample in samples:
            # Input into classifier
            result_label = classifier(HMM_Models,test_labels, sample)
            result_labels.append(result_label)
            if result_label == truth_label:
                correct_count += 1
                
        accuracies[char] = correct_count / num_samples
        result_labels_list.append(result_labels)

        if useprint:
            print("Classification accuracy of test samples of character " + str(test_labels[char])  + " is: " + str(accuracies[char]*100) + "%")
        
    return accuracies, result_labels_list


def main():
    from dataprep import dataprep
    import pandas as pd

    db_name = "database_inc_sampchar"
    train_data, test_data, data_labels = dataprep(db_name, nr_test=5)

    hmm_learn = pd.read_pickle(r'legit_hmm')

    accuracies, result_labels_list = hmm_test(hmm_learn, test_data, data_labels)


if __name__ == "__main__":
    main()
