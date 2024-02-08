from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib


iris = load_iris()
X, y = iris.data, iris.target

clf = RandomForestClassifier(random_state=42)
clf.fit(X, y)

joblib.dump(clf, 'model.pkl')
