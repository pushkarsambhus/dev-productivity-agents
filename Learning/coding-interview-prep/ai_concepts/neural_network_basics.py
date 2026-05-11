# A neural network is loosely inspired by the human brain — it's made of layers of
# "neurons" that pass signals to each other. Each connection has a weight (importance).
# We'll build a tiny one from scratch using only numpy to understand the core idea.

import numpy as np

# =============================================================================
# THE CORE IDEA
# =============================================================================
#
#  Input Layer       Hidden Layer      Output Layer
#  ───────────       ────────────      ────────────
#
#   x1 ──┐                              ┌── y (prediction)
#   x2 ──┼──→ [weights] ──→ [neurons] ──┤
#   x3 ──┘                              └── (sigmoid activation)
#
#  Forward pass: input → multiply by weights → add bias → activation → output
#  Backprop:     compare output to true label → adjust weights to reduce error
#
# An "activation function" decides whether a neuron "fires".
# Sigmoid squashes any number into a value between 0 and 1 — perfect for yes/no problems.

# =============================================================================
# ACTIVATION FUNCTIONS
# =============================================================================

def sigmoid(x):
    """
    Sigmoid: squashes any number to between 0 and 1.
    Used in the output layer for binary classification (yes/no, spam/not spam).
    Graph looks like a stretched S-curve.
    """
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """
    The derivative of sigmoid — needed for backpropagation.
    Tells us how much to adjust weights during training.
    """
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    """
    ReLU (Rectified Linear Unit): output = x if x > 0, else 0.
    Very fast and commonly used in hidden layers of deep networks.
    """
    return np.maximum(0, x)

# =============================================================================
# A SINGLE NEURON (the building block)
# =============================================================================

class Neuron:
    """
    A single artificial neuron.
    It takes inputs, multiplies each by a weight (importance),
    adds a bias (like a threshold), then applies an activation function.

    Think of it like a decision-maker:
      "If the weighted evidence is strong enough, I'll fire!"
    """

    def __init__(self, n_inputs):
        # Initialize weights randomly (small values near 0)
        np.random.seed(42)
        self.weights = np.random.randn(n_inputs) * 0.1   # one weight per input
        self.bias = 0.0                                    # bias starts at zero

    def forward(self, inputs):
        """
        Forward pass: compute the neuron's output.
        z = (w1*x1 + w2*x2 + ... + wn*xn) + bias
        output = sigmoid(z)
        """
        z = np.dot(inputs, self.weights) + self.bias   # weighted sum
        return sigmoid(z)                               # activation

# =============================================================================
# A SIMPLE NEURAL NETWORK (1 hidden layer)
# =============================================================================

class SimpleNeuralNetwork:
    """
    A tiny neural network with:
      - Input layer:  2 inputs
      - Hidden layer: 2 neurons
      - Output layer: 1 neuron (binary prediction: 0 or 1)

    This can solve simple problems like logical AND/OR.
    """

    def __init__(self):
        np.random.seed(42)
        # Layer 1 (hidden): 2 neurons, each with 2 weights + 1 bias
        self.w1 = np.random.randn(2, 2) * 0.1    # shape: (inputs=2, neurons=2)
        self.b1 = np.zeros((1, 2))                # shape: (1, 2)

        # Layer 2 (output): 1 neuron, takes 2 inputs from hidden layer
        self.w2 = np.random.randn(2, 1) * 0.1    # shape: (inputs=2, neurons=1)
        self.b2 = np.zeros((1, 1))                # shape: (1, 1)

    def forward(self, X):
        """
        Forward pass: push data through the network, layer by layer.
        X shape: (n_samples, 2)
        """
        # Hidden layer: linear combination + sigmoid activation
        self.z1 = np.dot(X, self.w1) + self.b1   # weighted sum
        self.a1 = sigmoid(self.z1)                 # activate

        # Output layer: same idea
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = sigmoid(self.z2)                 # final prediction

        return self.a2

    def train(self, X, y, learning_rate=0.5, epochs=1000):
        """
        Train using backpropagation + gradient descent.

        Backprop: start from the error at the output,
                  work BACKWARDS through layers,
                  nudge each weight slightly to reduce the error.

        learning_rate: how big each nudge is (too big = unstable, too small = slow)
        epochs: how many full passes through the training data
        """
        for epoch in range(epochs):
            # --- Forward pass ---
            output = self.forward(X)

            # --- Calculate error ---
            error = y - output    # how wrong are we?

            # --- Backward pass (backpropagation) ---
            # Output layer gradient
            d_output = error * sigmoid_derivative(self.z2)

            # Hidden layer gradient
            d_hidden = np.dot(d_output, self.w2.T) * sigmoid_derivative(self.z1)

            # --- Update weights (gradient descent step) ---
            self.w2 += learning_rate * np.dot(self.a1.T, d_output)
            self.b2 += learning_rate * np.sum(d_output, axis=0, keepdims=True)
            self.w1 += learning_rate * np.dot(X.T, d_hidden)
            self.b1 += learning_rate * np.sum(d_hidden, axis=0, keepdims=True)

            # Print progress every 200 epochs
            if epoch % 200 == 0:
                loss = np.mean(error ** 2)   # Mean Squared Error
                print(f"  Epoch {epoch:4d}: Loss = {loss:.6f}")

    def predict(self, X):
        """Return 0 or 1 based on whether output > 0.5."""
        output = self.forward(X)
        return (output > 0.5).astype(int)

if __name__ == "__main__":
    print("=== Building a Neural Network from Scratch ===\n")

    # --- Demo 1: Single Neuron ---
    print("--- Single Neuron ---")
    neuron = Neuron(n_inputs=3)
    inputs = np.array([0.5, -0.2, 0.8])
    output = neuron.forward(inputs)
    print(f"Inputs: {inputs}")
    print(f"Weights: {neuron.weights.round(3)}")
    print(f"Neuron output (sigmoid): {output:.4f}")

    # --- Demo 2: Neural Network learning OR logic ---
    print("\n--- Neural Network: Learning OR Gate ---")
    print("OR gate: output is 1 if AT LEAST ONE input is 1")
    print()

    # Training data: OR gate truth table
    X_train = np.array([
        [0, 0],   # input: 0 OR 0 = 0
        [0, 1],   # input: 0 OR 1 = 1
        [1, 0],   # input: 1 OR 0 = 1
        [1, 1],   # input: 1 OR 1 = 1
    ])
    y_train = np.array([[0], [1], [1], [1]])   # expected outputs

    nn = SimpleNeuralNetwork()

    print("Training loss over time:")
    nn.train(X_train, y_train, learning_rate=0.5, epochs=1001)

    print("\nResults after training:")
    predictions = nn.predict(X_train)
    print(f"{'Input':>10} | {'Expected':>8} | {'Predicted':>9}")
    print("-" * 34)
    for inp, exp, pred in zip(X_train, y_train, predictions):
        correct = "✓" if pred[0] == exp[0] else "✗"
        print(f"  {str(inp):>8} | {exp[0]:>8} | {pred[0]:>9} {correct}")

    print("\nKey concepts demonstrated:")
    print("  - Forward pass:      data flows input → hidden → output")
    print("  - Sigmoid activation: squashes output to 0–1 range")
    print("  - Loss function:      measures prediction error (MSE)")
    print("  - Backpropagation:    calculates how to adjust each weight")
    print("  - Gradient descent:   nudges weights to reduce loss")
    print("  - Epochs:             training passes through all data")
