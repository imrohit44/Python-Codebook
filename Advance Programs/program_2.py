'''
# **Machine Learning Classifier with Scikit-Learn**

This program trains a Random Forest classifier, a popular machine learning model, on the famous Iris dataset. It then evaluates the model's accuracy and shows a classification report.

**Concepts:** 

Supervised learning, model training, feature engineering, evaluation metrics.

**How to Run**

**1. Install libraries:**

```
pip install pandas scikit-learn
```

**2. Save the code and execute it:**

```
python program_2.py
```
'''

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings

# Suppress a specific future warning from scikit-learn
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")


def train_and_evaluate_iris_classifier():
    """Loads the Iris dataset, trains a Random Forest classifier, and evaluates it."""
    # 1. Load Dataset
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)

    print("Iris Dataset Features (First 5 rows):")
    print(X.head())
    print("\n")

    # 2. Split Data into Training and Testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"Training set size: {len(X_train)} samples")
    print(f"Testing set size: {len(X_test)} samples\n")

    # 3. Initialize and Train the Model
    print("Training the Random Forest Classifier...")
    # n_estimators is the number of trees in the forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Training complete.\n")

    # 4. Make Predictions on the Test Set
    y_pred = model.predict(X_test)

    # 5. Evaluate the Model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}\n")
    
    print("Classification Report:")
    report = classification_report(y_test, y_pred, target_names=iris.target_names)
    print(report)

if __name__ == "__main__":
    train_and_evaluate_iris_classifier()