from textblob.classifiers import NaiveBayesClassifier
from pathlib import Path

def main():
    # Get directory where this script is located
    base_dir = Path(__file__).parent

    # Build paths to data files
    train_path = base_dir / "train.json"
    test_path = base_dir / "test.json"

    # Load training data
    with open(train_path, "r") as train_file:
        classifier = NaiveBayesClassifier(train_file, format="json")

    # Load test data
    with open(test_path, "r") as test_file:
        accuracy = classifier.accuracy(test_file)

    print("Accuracy:", accuracy)

    print("Classifying sentences:")
    print("I love this place ->", classifier.classify("I love this place"))
    print("I hate this job ->", classifier.classify("I hate this job"))

    print("\nMost Informative Features:")
    classifier.show_informative_features(5)


if __name__ == "__main__":
    main()