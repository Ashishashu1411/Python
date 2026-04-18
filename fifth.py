import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, auc
import matplotlib.pyplot as plt

def eval_model(m, X, y):
    p = m.predict(X); prob = m.predict_proba(X)[:,1]
    fpr, tpr, _ = roc_curve(y, prob)
    return accuracy_score(y,p), precision_score(y,p), recall_score(y,p), fpr, tpr, auc(fpr,tpr)

def load_scaled(path, X_test):
    df = pd.read_csv(path)
    X, y = df.drop("target", axis=1), df["target"]
    sc = StandardScaler()
    return sc.fit_transform(X), y, sc.transform(X_test)

def plot_all(x, A, P, R, ROC, title, xlabel):
    fig, ax = plt.subplots(2, 2, figsize=(14,10))
    for i,(name,data,mark) in enumerate(zip(["Acc","Prec","Rec"],[A,P,R],['o','s','^'])):
        ax[i//2,i%2].plot(x,data,marker=mark); ax[i//2,i%2].set_title(name); ax[i//2,i%2].set_xlabel(xlabel)
    ax[1,1].plot([0,1],[0,1],'k--')
    for lbl,d in ROC.items(): ax[1,1].plot(d["fpr"],d["tpr"],label=f"{lbl} (AUC={d['auc']:.2f})")
    ax[1,1].legend(); fig.suptitle(title); plt.tight_layout(); plt.show()

# -------- Load Test Set --------
df_test = pd.read_csv("100D_test_dataset.csv")
X_test, y_test = df_test.drop("target", axis=1), df_test["target"]

# -------- PART 1: Dataset Size vs Performance --------
files = {
    100:"100D_heart_disease_dataset.csv",
    300:"300D_heart_disease_dataset.csv",
    600:"600D_heart_disease_dataset.csv",
    900:"900D_heart_disease_dataset.csv"
}

A=[]; P=[]; R=[]; ROC={}
for size,path in files.items():
    Xs, yt, Xts = load_scaled(path, X_test)
    acc, pr, rc, fpr, tpr, auc_ = eval_model(KNeighborsClassifier(5).fit(Xs,yt), Xts, y_test)
    A.append(acc); P.append(pr); R.append(rc); ROC[size]={"fpr":fpr,"tpr":tpr,"auc":auc_}

plot_all(list(files.keys()), A, P, R, ROC, "KNN (k=5) vs Dataset Size", "Dataset Size")

# -------- PART 2: K Value vs Performance --------
Xs, yt, Xts = load_scaled(files[900], X_test)
k_vals = [1,3,5,7,9,11,21,31]

A=[]; P=[]; R=[]; ROC={}
for k in k_vals:
    acc, pr, rc, fpr, tpr, auc_ = eval_model(KNeighborsClassifier(k).fit(Xs,yt), Xts, y_test)
    A.append(acc); P.append(pr); R.append(rc); ROC[k]={"fpr":fpr,"tpr":tpr,"auc":auc_}

plot_all(k_vals, A, P, R, ROC, "KNN vs K Value (900D Dataset)", "K Value")
