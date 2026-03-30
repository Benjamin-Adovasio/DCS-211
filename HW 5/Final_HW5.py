# %%
############################
# BLOCK 1:  IMPORTS
############################

# libraries!
import numpy as np      # numpy is Python's "array" library
import pandas as pd     # Pandas is Python's "data" library ("dataframe" == spreadsheet)

# %%


# %%
#############################
# BLOCK 2:  VARIABLES LISTING
#############################

# for reference, as you work throughout, come back and list all the variable names
#   here along with what that variable holds

#   Variable:  Contents
#   -------------------
#   [FILL IN VARS BELOW]
#

# %%
####################################
#from sklearn.datasets import load_iris
#data = load_iris()
#df = pd.DataFrame(data.data, columns=data.feature_names)
#df

# %%
#############################
# BLOCK 3:  READING DATA
#############################

# let's read in our flower data...
#
filename = 'iris.csv'
df = pd.read_csv(filename, header=0)   # encoding="latin1" et al.
print(f"{filename}: file read into a pandas DataFrame.")
df.head()

# %%
#############################
# BLOCK 4:  SETTING OPTIONS
#############################

#
# a dataframe is a "spreadsheet in Python"
#    (this one seems to have an extra column!)
#
pd.set_option('display.max_rows', 8)  # None for no limit; default: 10
pd.set_option('display.min_rows', 8)  # None for no limit; default: 10
# let's view it!
df

# %%
##############################
# BLOCK 5:  USING DF'S .info()
##############################

#
# let's look at our pandas DataFrame's info   (Aargh: that extra column!)
#
df.info()

# %%
#############################
# BLOCK 6:  CLEANING DATA
#############################

#
# let's drop that last column (dropping is usually by _name_):
#
#   if you want a list of the column names use df.columns
#col5name = df.columns[5]  # get column name at index 5

df_clean = df.drop(columns=['junk']) # drop by name is typical, but what else is possible?
df_clean.info()                         # Is the bad last column gone?

# %%
##############################
# BLOCK 7:  FEATURE NAMES DICT
##############################

#
# let's keep our column names in variables, for reference;
#   in machine learning contexts, these are referred to as "features"
#
features = df_clean.columns            # "list" of columns
print(f"FEATURES: {features}\n")
  # It's a "pandas" list, called an Index
  # use it just as a Python list of strings:
print(f"First feature: {features[0]}\n")

# let's create a dictionary to look up any column index by name
feature_name_to_index = {}
for i, name in enumerate(features):
    feature_name_to_index[name] = i  # using the name (as key), assign the value (i)
print(f"feature_name_to_index: {feature_name_to_index}")

# %%
##############################
# BLOCK 8:  INSPECTING DATA
##############################

#
# let's look at our cleaned-up dataframe...
#
df_clean.info()
print('=' * 70)

#
# Notice that the non-null count is _different_ for irisname!
# Why?  Show a table and inspect...
print(df_clean)
print('=' * 70)

# or more to the point, grab that column and inspect:
print(f"Irisname entries: {df_clean['irisname'].unique()}")

# also note how the last two rows in the df have problems, among others...


# %%
df.columns

# %%
##############################
# BLOCK 9:  USING DF'S dropna
##############################

#
# typically, after dropping columns that we don't want,
#   we drop rows with missing data (other approaches are possible, too)
#
df_clean = df_clean.dropna()   # this removes all rows with nan items
df_clean.info()
print('=' * 70)
df_clean

#
# notice that _all_ of the rows now have 144 non-null items
#    also, the first and last rows (among others) aren't valid data...
#    we'll handle that next

# %%
################################
# BLOCK 10:  REMOVING BOGUS DATA
################################

# or more to the point, grab that column and inspect:
print(f"Irisname entries: {df_clean['irisname'].unique()}")
print(df_clean['irisname'] == 'alieniris')  # what does this show?
print(df_clean['irisname'] != 'alieniris')  # what does this show?

# define a final version of the DataFrame by pulling out the
# bad alieniris data (remember that you can pass a boolean
# Series to select data that you want)
df_final = df_clean[df_clean['irisname'] != 'alieniris'].copy()
#          ^^^^  YOU NEED TO WRITE CODE HERE...

print(df_final.shape)
df_final

# %%
##########################################
# BLOCK 11:  CONVERT SPECIES NAME TO INDEX
##########################################

# all of scikit-learn's ML routines need numbers, not strings
#   ... even for categories/classifications (like species!)
#   so, we will convert the flower-species to numbers:

species_names = df_final['irisname'].unique()
species_name_to_index = { species_names[i]:i for i in range(len(species_names))}
print(species_name_to_index)
print(type(species_name_to_index))

def convertSpecies(species_name: str) -> int:
    ''' return the species index (a unique integer/category) '''
    #print(f"converting {species_name}...")
    return species_name_to_index[species_name]

# Let's try it out...
for name in species_names:
    print(f"{name} maps to {convertSpecies(name)}")

# %%
##########################################
# BLOCK 12:  USING DF'S .apply
##########################################

#
# we can "apply" our new convertSpecies function to a whole column
#
# (The following will issue a "SettingWithCopyWarning" here...)
# see https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#
# >>> ADD CODE HERE TO KEEP THE WARNING FROM HAPPENING <<<

df_final.loc[:, 'irisname'] = df_final['irisname'].apply(convertSpecies)
#df_final.loc[:, 'irisname'] = df_final['irisname'].apply(convertSpecies)
# Don't run this twice!   Why?!  What's "KeyError: 0"?
#   (of course, you can always go back and re-establish definitions of df_final)



# %%
##########################################
# BLOCK 13:  CONFIRMING FINAL DATAFRAME
##########################################

#
# let's see it!  (this is safe to run many times...)
#
df_final         # print(df_final.tostring())  # for _all_ rows...

# %%
##########################################
# BLOCK 14:  CONVERTING TO NUMPY FORMAT
##########################################

#
# let's convert our dataframe to a numpy array, named A
#    Our ML library, scikit-learn operates entirely on numpy arrays.
#
#A = df_final.values
A = df_final.to_numpy()  # better -- self-documenting!

print(f"type of A: {type(A)}")
print(df_final.head())
print(f"A[0] = {A[0]}")

# %%
##################################################
# BLOCK 15:  CONVERTING NUMPY ARRAY TO ALL FLOATS
##################################################

#
# let's convert to make sure it's all floating-point, so we can multiply and divide
#
A = A.astype('float64')  # so many:  www.tutorialspoint.com/numpy/numpy_data_types.htm
A

# %%
##########################################
# BLOCK 16:  USING NUMPY'S .shape
##########################################

#
# nice to have num_rows and num_cols variables handy...
#
num_rows, num_cols = A.shape
print(f"\nThe dataset has {num_rows} rows and {num_cols} cols")
print(A)

# %%
##########################################
# BLOCK 17:  PRINTING FLOWER INFO
##########################################

# let's use all of our previously-defined variables, to reinforce names...

# choose a row index (particular flower) arbitrarily:
flower = 132
print(f"flower #{flower} data is {A[flower]}")

for i in range(len(features)):
    col_name = features[i]
    if col_name != 'irisname':
        print(f"  Its {col_name} is {A[flower][i]}")
    else:
        species_num  = int(A[flower][i])
        species_name = species_names[species_num]
        print(f"  Its {col_name} is {species_name} ({species_num})")

# %%
##########################################
# BLOCK 18:  WRITING OUR OWN 1-NN FUNCTION
##########################################

#
# We don't have to use scikit-learn to implement NN!
#

#
# data-driven predictive model (1-nearest-neighbor)
#

# Python functions are first-class objects!
dist = np.linalg.norm  # built in to numpy... but what does norm do?

num_rows, num_cols = A.shape  # data size

def predictiveModel( features: list[float] ) -> str:
    """ input: a list of four features
                [ sepallen, sepalwid, petallen, petalwid ]
        output: the predicted species of iris, from
                  setosa (0), versicolor (1), virginica (2)
    """
    our_features = np.asarray(features)   # make a numpy array

    closest_flower   = A[0]
    closest_features = A[0,0:4]
    closest_distance = dist(our_features - closest_features)

    for i in range(1, num_rows, 1):
        current_flower   = A[i]
        current_features = A[i,0:4]
        current_distance = dist(our_features - current_features)

        if current_distance < closest_distance:
            closest_distance = current_distance  # remember closest!
            closest_flower   = current_flower

    # done comparing with every flower in the dataset
    predicted_species = int(round(closest_flower[4]))   # what type is closest_flower?
    name = species_names[predicted_species]
    return f"{name} ({predicted_species})"

#
# Try it!
#
# features = eval(input("Enter new features: "))
#
features = [ 4.6, 3.6, 3.0, 1.2 ]
result = predictiveModel( features )
print(f"I predict {result} from features {features}")

# %%
##########################################
# BLOCK 19:  COMMENTS ON SCIKIT-LEARN kNN
##########################################

#
# but, we don't have to write our own ... because
#
#     we want knn for any k (not just k=1 as above)
#     we want an already-debugged algorithm!
#     we want to ask iris-related questions instead of implementation ones...
#

# %%
################################################
# BLOCK 20:  DEFINIING FEATURES & LABELS FOR kNN
################################################

print("+++ Start of data definitions +++\n")

X_all = A[:,0:4]  # X (features) ... is all rows, columns 0, 1, 2, 3
y_all = A[:,4]    # y (labels) ... is all rows, column 4 only
                  # (look back at slide 20)
print(f"X_all (just features) is \n {X_all}")
print(f"y_all (just labels)   is \n {y_all}")

# %%
################################################
# BLOCK 21:  REWEIGHTING FEATURES
################################################

#
# we can re-weight different features here...
#

col_weights = {              # could be called feature weight...
    'sepallen':1.0,
    'sepalwid':1.0,
    'petallen':1.0,
    'petalwid':1.0,
}

for col_name in col_weights:
    i = feature_name_to_index[col_name]    # get the column index, i, of the column name
    weight = col_weights[col_name]  # from the dictionary above
    print(f"Weighting {col_name} by {weight}")
    # weighting == "multiplying"
    X_all[:,i] *= weight   # multiply by the weight to give this column ("feature")

# %%
################################################
# BLOCK 22:  PERMUTING THE DATA
################################################

#
#
# we scramble the data, to give a different TRAIN/TEST split each time...
#
indices = np.random.permutation(len(y_all))  # indices is a permutation-list

# we scramble both X and y, necessarily with the same permutation
X_labeled = X_all[indices]              # we apply the _same_ permutation to each!
y_labeled = y_all[indices]              # again...
print(X_labeled)  # note that X_labeled and y_labeled are permuted identically
print(y_labeled)

# %%
################################################
# BLOCK 23:  DEFINING TRAIN VS TEST SETS
################################################

#
# We next separate into test data and training data ...
#    + We will train on the training data...
#    + We will _not_ look at the testing data when building the model
#
# Then, afterward, we will test on the testing data -- and see how well we do!
#

#
# a common convention:  train on 80%, test on 20%    Let's define the TEST_PERCENT
#
num_rows = X_labeled.shape[0]     # the number of labeled rows
test_percent = 0.20
test_size = int(test_percent * num_rows)   # no harm in rounding down

X_test = X_labeled[:test_size]    # first section are for testing
y_test = y_labeled[:test_size]

X_train = X_labeled[test_size:]   # all the rest are for training
y_train = y_labeled[test_size:]

num_train_rows = len(y_train)
num_test_rows  = len(y_test)
print(f"total rows: {num_rows};  training with {num_train_rows} rows;  testing with {num_test_rows} rows" )
print(f"\t(sanity check:  {num_train_rows} + {num_test_rows} = {num_train_rows + num_test_rows})")

# %%
#######################################################
# BLOCK 24:  FIRST ATTEMPT TO BUILD & TRAIN A kNN MODEL
#######################################################

#
# +++ This is the "Model-building and Model-training Cell"
#
# Create a kNN model and train it!
#
from sklearn.neighbors import KNeighborsClassifier

k = 84   # we don't know what k to use, so we guess for now!  (this will _not_ be a good value)
knn_model = KNeighborsClassifier(n_neighbors = k)       # here, k is the "k" in kNN

# we train the model (it's one line!)
knn_model.fit(X_train, y_train)                              # yay!  trained!
print("Created and trained a knn classifier with k =", k)

# %%
################################################
# BLOCK 25:  TEST THE kNN MODEL
################################################

#
# +++ This is the "Model-testing Cell"
#
# Now, let's see how well we did on our "held-out data" (the testing data)
#

# We run our test set!
predicted_labels = knn_model.predict(X_test)
actual_labels = y_test

# Let's print them so we can compare...
print("Predicted labels:", predicted_labels)
print("Actual  labels  :", actual_labels)

# And, some overall results
num_correct = sum(predicted_labels == actual_labels)
total = len(actual_labels)
print(f"\nResults on test set:  {num_correct} correct out of {total} total.")

# %%
################################################
# BLOCK 26:  PRETTY-PRINT PREDICTED LABELS
################################################

#
# Let's print these more helpfully, in a vertical table
#

def compareLabels(predicted_labels: np.ndarray, actual_labels: np.ndarray) -> int:
    ''' a more neatly formatted comparison, returning the number correct '''
    num_labels = len(predicted_labels)
    num_correct = 0

    for i in range(num_labels):
        predicted = int(round(predicted_labels[i]))  # round-to-int protects from float imprecision
        actual    = int(round(actual_labels[i]))
        result = "incorrect"
        if predicted == actual:  # if they match,
            result = ""       # no longer incorrect
            num_correct += 1  # and we count a match!

        # note the justification formatting:
        #       :>3d right justifies integers (d) to width 3
        #       :<12s left justifies strings (s) to width 12
        print(f"row {i:>3d} : ", end = "")
        print(f"{species_names[predicted]:>12s} ", end = "")
        print(f"{species_names[actual]:<12s}   {result}")

    print()
    print(f"Correct: {num_correct} out of {num_labels}")
    return num_correct

#
# let's try it out!
#

compareLabels(predicted_labels,actual_labels)

# %%
################################################
# BLOCK 27:  USE THE FIRST-ATTEMPT kNN MODEL
################################################

#
# Ok!  We have our knn model, we could just use it...
#

#
# data-driven predictive model (k-nearest-neighbor), using scikit-learn
#

def predictiveModel( features: list[float] ) -> str:
    ''' input: a list of four features
                [ sepallen, sepalwid, petallen, petalwid ]
        output: the predicted species of iris, from
                  setosa (0), versicolor (1), virginica (2)
    '''
    our_features = np.asarray([features])                 # extra brackets needed
    predicted_species = knn_model.predict(our_features)
    print(f"predicted_species = {predicted_species}")

    predicted_species = int(round(predicted_species[0]))  # unpack one element
    name = species_names[predicted_species]
    return f"{name} ({predicted_species})"

#
# Try it!
#
# features = eval(input("Enter new features: "))
#
features = [6.7,3.3,5.7,2.1]  # [5.8,2.7,4.1,1.0] [4.6,3.6,3.0,2.2] [6.7,3.3,5.7,2.1]
result = predictiveModel( features )
print(f"I predict {result} from features {features}")

# %%
################################################
# BLOCK 28:  COMMENTS ON CHOICE OF BEST k
################################################

#
# Except, we didn't really explore whether this was the BEST model we could build!
#
#
# We used k = 84  (a neighborhood size of 84 flowers)
# In a dataset of only 140ish flowers, with three species, this seems like a bad idea!
#
# Perhaps we should try ALL the neighborhood sizes in their own TRAIN/TEST split
# and see which neighborhood size works the best, for irises, at least...
#

# %%
################################################
# BLOCK 29:  USING CROSS VALIDATION
################################################

#
# to do this, we use "cross validation"
# (see slide 45)
#

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

#
# cross-validation splits the training set into two pieces:
#   + model-building and model-validation. We'll use "build" and "validate"
#

max_k = 85
all_accuracies = []
best_k = 1
best_accuracy = -1

for k in range(1, max_k, 1):
    knn_cv_model = KNeighborsClassifier(n_neighbors=k)
    cv_scores = cross_val_score(knn_cv_model, X_train, y_train, cv=5)
    this_cv_accuracy = cv_scores.mean()
    print(f"k: {k:2d}  cv accuracy: {this_cv_accuracy:7.4f}")
    all_accuracies.append(this_cv_accuracy)
    if this_cv_accuracy > best_accuracy:
        best_accuracy = this_cv_accuracy
        best_k = k
# assign best value of k to best_k
#best_k = k      # *** AT THE MOMENT THIS IS INCORRECT ***
# you'll need to modify the loop above to find and remember the real best_k

print(f"best_k = {best_k}   yields the highest average cv accuracy.")  # print the best one

plt.figure(figsize=(10, 6))
sns.lineplot(x=range(1,len(all_accuracies)+1), y=all_accuracies)
plt.xlabel("k value (index)")
plt.ylabel("Cross-validated accuracy")
plt.title("kNN Accuracy vs k Value")
plt.show()

# %%
################################################
# BLOCK 30:  RE-BUILD & RE-TRAIN USING BEST k
################################################

#
# Now, we re-create and re-run the  "Model-building and -training Cell"
#
# Now, using best_k instead of the original, randomly-guessed value    How does it do?!
#
from sklearn.neighbors import KNeighborsClassifier
knn_model_tuned = KNeighborsClassifier(n_neighbors = best_k)   # here, we use the best_k

# we train the model (one line!)
knn_model_tuned.fit(X_train, y_train)                              # yay!  trained!
print(f"Created + trained a knn classifier, now tuned with a (best) k of {best_k}")

# %%
################################################
# BLOCK 31:  RE-TEST THE BEST-k MODEL
################################################

#
# Re-create and re-run the  "Model-testing Cell"     How does it do with best_k?!
#
predicted_labels = knn_model_tuned.predict(X_test)
actual_labels = y_test

# Let's print them so we can compare...
print("Predicted labels:", predicted_labels)
print("Actual labels:", actual_labels)
print()
# and, we'll print our nicer table...
compareLabels(predicted_labels,actual_labels)

# %%
################################################
# BLOCK 32:  TRYING DIFFERENT PERMUTATIONS
################################################

#
# Before moving on, go back and choose a new permutation to give
# new testing and training sets, and go back through the steps
# for identifying the "best" k (starting at Block 22 and re-doing
# up through Block 31).
#
# Repeat this several times.
# Do you get the same value for k each time?  Why or why not?
#

# %%
####################################################
# BLOCK 33:  REBUILD & TRAIN USING BEST k & ALL DATA
####################################################

# Ok!  Now we have tuned knn to use the "best" value of k...
#
# And, we should really use ALL available data to train our final predictive model
# (not split into test and train as before)
#

knn_model_final = KNeighborsClassifier(n_neighbors=best_k)   # here, we use the best_k
knn_model_final.fit(X_all, y_all)                            # yay!  trained!
print(f"Created + trained a 'final' knn classifier, with a (best) k of {best_k}")

# %%
####################################################
# BLOCK 34:  TRYING FINAL MODEL "IN THE WILD"
####################################################

#
# final predictive model (k-nearest-neighbor), with tuned k + ALL data incorporated
#

def predictiveModel( features: list[float] ) -> str:
    ''' input: a list of four features
                [ sepallen, sepalwid, petallen, petalwid ]
        output: the predicted species of iris, from
                  setosa (0), versicolor (1), virginica (2)
    '''
    our_features = np.asarray([features])                 # extra brackets needed
    predicted_species = knn_model_final.predict(our_features)

    predicted_species = int(round(predicted_species[0]))  # unpack one element
    name = species_names[predicted_species]
    return f"{name} ({predicted_species})"

#
# Try it on several!
#
# features = eval(input("Enter new features: "))
#
features = [6.7,3.3,5.7,2.1]  # [5.8,2.7,4.1,1.0] [4.6,3.6,3.0,2.2] [6.7,3.3,5.7,2.1]
result = predictiveModel( features )
print(f"I predict {result} from features {features}")

# %%
################################################################
# BLOCK 35a:  HOW DOES THE MODEL PERFORM ON MEAN OF EACH FLOWER?
################################################################

# let's recall the species names and their order in the list
print(species_names)
print('=' * 70)

# and let's recall what the final DataFrame looks like, noting that
# the irisname was converted to the corresponding index in species_names
print(df_final)

# %%
################################################################
# BLOCK 35b:  HOW DOES THE MODEL PERFORM ON MEAN OF EACH FLOWER?
################################################################

# let's grab the data from df_final corresponding to versicolor
versicolor_data = df_final[ df_final['irisname'] == convertSpecies('versicolor') ]
print(versicolor_data)
print('=' * 70)

# let's print the mean of each column
print(versicolor_data.mean())
print('=' * 70)

# and let's grab the features means only (don't need the label) for versicolor
versicolor_features_means = np.asarray(versicolor_data.mean()[:-1])
print(versicolor_features_means)

# now run the predictive model (see Block 34 above) and print a corresponding
# message

# >>> YOU ADD CODE HERE
result = predictiveModel(versicolor_features_means)
print(f"Mean versicolor features {versicolor_features_means} -> {result}")

# %%
################################################################
# BLOCK 35c:  HOW DOES THE MODEL PERFORM ON MEAN OF EACH FLOWER?
################################################################

# Automate the process used in Block 35b, across all species:
#
# Loop across species names, and for each species,
#   (a) pull that corresponding data from df_final
#   (b) compute the means of the features, storing as a numpy array
#   (c) call the predictive model using those features
#   (d) print a corresponding message

# >> YOU ADD CODE HERE -- YOU SHOULD NEED NO MORE THAN 5 LINES OF CODE
for name in species_names:
    species_data = df_final[df_final['irisname'] == convertSpecies(name)]
    species_features_means = np.asarray(species_data.mean()[:-1])
    result = predictiveModel(species_features_means)
    print(f"Mean {name} features {species_features_means} -> {result}")


