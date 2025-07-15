from ucimlrepo import fetch_ucirepo
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

# fetch dataset
iris = fetch_ucirepo(id=53)
X = iris.data.features
y = iris.data.targets
print(iris.metadata)
print(iris.variables)

sepal_length = X['sepal length']
sepal_width = X['sepal width']

# Convert string labels to numerical values
le = LabelEncoder()
y_encoded = le.fit_transform(y['class'])

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(sepal_length, sepal_width, c=y_encoded, cmap='viridis')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.title('The data set of all 3 classes')
plt.colorbar(label='Class')
plt.show()


# Filter for Setosa and Versicolor
setosa_versicolor_indices = y['class'].isin(['Iris-setosa', 'Iris-versicolor'])
X_binary = X[setosa_versicolor_indices]
y_binary = y['class'][setosa_versicolor_indices]


sepal_length = X_binary['sepal length']
sepal_width = X_binary['sepal width']

# Convert string labels to numerical values (0 and 1)
le = LabelEncoder()
y_encoded = le.fit_transform(y_binary)


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_binary[['sepal length', 'sepal width']], y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Create the scatter plot for the binary classification data
plt.figure(figsize=(8, 6))
plt.scatter(X_train['sepal length'], X_train['sepal width'], c=y_train, cmap='viridis')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.title('The data set of the first 2 classes(Setosa & Versicolor)')
plt.colorbar(label='Class')
plt.show()

class Perceptron:
    def __init__(self, learning_rate=0.1, n_iters=100):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        y_ = np.where(y >=1, 1, -1) #Convert to bipolar {-1, 1}
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = np.where(linear_output>=0, 1, -1)
                update = self.lr * (y_[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = np.where(linear_output >= 0, 1, 0) #Convert back to {0,1}
        return y_predicted

# Train the perceptron
perceptron = Perceptron(learning_rate=0.01, n_iters=1000)
perceptron.fit(X_train.values, y_train)

# Make predictions on the test set
y_pred = perceptron.predict(X_test.values)

# Calculate the accuracy
accuracy = np.mean(y_pred == y_test)
print(f"Test Accuracy: {accuracy}")

#Calculate training error
y_train_pred = perceptron.predict(X_train.values)
training_accuracy = np.mean(y_train_pred == y_train)
print(f"Training Accuracy: {training_accuracy}")