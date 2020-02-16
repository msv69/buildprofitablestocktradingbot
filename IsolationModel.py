from sklearn.ensemble import IsolationForest
class IsolationModel:
    """
        Simple Isolation Model based on contamination
    """

    def __init__(self, data):
        self.normalized_data = (data - data.mean()) / data.std()
        self.iso = IsolationForest(contamination=.001, behaviour='new')
        self.iso.fit(self.normalized_data)
        self.iso.predict(self.normalized_data)

    def predict_outlier(self, data):
        return self.iso.predict(data)
# Randomness breaks overpopulated alpha