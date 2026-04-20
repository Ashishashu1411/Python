import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, auc

dataset_pairs = [
    ('100D_heart_disease_dataset.csv', '100D_test_dataset.csv'),
    ('300D_heart_disease_dataset.csv', '300D_test_dataset.csv'),
    ('600D_heart_disease_dataset.csv', '600D_test_dataset.csv'),
    ('900D_heart_disease_dataset.csv', '900D_test_dataset.csv'),
]

k_values = [3, 5, 7, 9, 11, 21, 31]

# Store metrics for all datasets
all_accuracy = {}
all_precision = {}
all_recall = {}
all_auc = {}

for train_file, test_file in dataset_pairs:
    
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    X_train = train_df.iloc[:, :-1].values
    y_train = train_df.iloc[:, -1].values
    X_test = test_df.iloc[:, :-1].values
    y_test = test_df.iloc[:, -1].values

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    accuracy_scores_k = []
    precision_scores_k = []
    recall_scores_k = []
    auc_scores_k = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        y_pred = knn.predict(X_test_scaled)
        y_pred_proba = knn.predict_proba(X_test_scaled)[:, 1]

        accuracy_scores_k.append(accuracy_score(y_test, y_pred))
        precision_scores_k.append(precision_score(y_test, y_pred, zero_division=0))
        recall_scores_k.append(recall_score(y_test, y_pred, zero_division=0))
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_scores_k.append(auc(fpr, tpr))

    label = train_file.split('_')[0] + 'D'
    all_accuracy[label] = accuracy_scores_k
    all_precision[label] = precision_scores_k
    all_recall[label] = recall_scores_k
    all_auc[label] = auc_scores_k

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for label in all_accuracy:
    axes[0, 0].plot(k_values, all_accuracy[label], marker='o', label=label)
    axes[0, 1].plot(k_values, all_precision[label], marker='o', label=label)
    axes[1, 0].plot(k_values, all_recall[label], marker='o', label=label)
    axes[1, 1].plot(k_values, all_auc[label], marker='o', label=label)

axes[0, 0].set_title('Accuracy vs. K value')
axes[0, 0].set_xlabel('K')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].legend()

axes[0, 1].set_title('Precision vs. K value')
axes[0, 1].set_xlabel('K')
axes[0, 1].set_ylabel('Precision')
axes[0, 1].legend()

axes[1, 0].set_title('Recall vs. K value')
axes[1, 0].set_xlabel('K')
axes[1, 0].set_ylabel('Recall')
axes[1, 0].legend()

axes[1, 1].set_title('AUC vs. K value')
axes[1, 1].set_xlabel('K')
axes[1, 1].set_ylabel('AUC')
axes[1, 1].legend()

plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 8))
for train_file, test_file in dataset_pairs:
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    X_train = train_df.iloc[:, :-1].values
    y_train = train_df.iloc[:, -1].values
    X_test = test_df.iloc[:, :-1].values
    y_test = test_df.iloc[:, -1].values

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Use best K (e.g., K=5) or loop for each K if you want
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    y_pred_proba = knn.predict_proba(X_test_scaled)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    label = train_file.split('_')[0] + 'D'
    plt.plot(fpr, tpr, label=f'{label} (AUC={roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid(True)
plt.show()
