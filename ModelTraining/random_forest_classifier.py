import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class RandomForestModel:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.model = RandomForestClassifier()

    def preprocess_data(self):
        # Assuming the last column is the target variable
        X = self.data.iloc[:, :-1]  # Features
        y = self.data.iloc[:, -1]   # Target
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        predictions = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        report = classification_report(self.y_test, predictions)
        print(f"Accuracy: {accuracy}\n\nClassification Report:\n{report}")


rf_model = RandomForestModel()
rf_model.preprocess_data()
rf_model.train_model()
rf_model.evaluate_model()
