# decision_tree_sklearn_tuning_reduced.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Data
X, y = load_iris(return_X_y=True, as_frame=True)
feature_names = X.columns
class_names = [str(c) for c in np.unique(y)]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Baseline model
baseline_clf = DecisionTreeClassifier(random_state=42)
baseline_clf.fit(X_train, y_train)
print("Baseline accuracy:", accuracy_score(y_test, baseline_clf.predict(X_test)))

# Grid Search
param_grid = {
    "criterion": ["gini", "entropy", "log_loss"],
    "splitter": ["best", "random"],
    "max_depth": [None, 2, 3, 4, 5, 6, 8, 10],
    "min_samples_split": [2, 5, 10, 20],
    "min_samples_leaf": [1, 2, 4, 8],
    "max_features": [None, "sqrt", "log2"],
    "class_weight": [None, "balanced"],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    scoring="accuracy",
    n_jobs=-1,
    cv=cv,
    refit=True
)

grid.fit(X_train, y_train)
best_clf = grid.best_estimator_
print("\nBest CV accuracy:", grid.best_score_)
print("Best params:", grid.best_params_)

# Test evaluation
y_pred = best_clf.predict(X_test)
print("\nTest accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification report:\n", classification_report(y_test, y_pred))

# Feature importance plot
plt.figure(figsize=(8, 4))
order = np.argsort(best_clf.feature_importances_)[::-1]
plt.bar(range(len(order)), best_clf.feature_importances_[order])
plt.xticks(range(len(order)), feature_names[order], rotation=30, ha="right")
plt.title("Feature importances (tuned DecisionTree)")
plt.tight_layout()
plt.show()

# Tree plot
plt.figure(figsize=(12, 8))
plot_tree(best_clf, feature_names=feature_names, class_names=class_names,
          filled=True, rounded=True, fontsize=8)
plt.title("Decision Tree (tuned)")
plt.tight_layout()
plt.show()