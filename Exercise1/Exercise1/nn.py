import numpy as np
import time

class TwoLayerNet(object):
    """
    A two-layer neural network with the architecture:
    
    input - fully connected layer - activation function (ReLU) - fully connected layer - softmax 
    
    The neural network performes a classification over C classes. The output is a score of the classes.
    A softmax loss function and a L2 regularization are used when training the network.
    """

    def __init__(self, input_dim, hidden_dim, output_dim, std=1e-4):
        """
        Inputs:
        
        - input_dim: Dimension of the input
        - hidden_dim: Neurons in hidden layer
        - output_dim: Classes
        
        Variables (stored in a dictionary self.params):
        
        W1: First layer weights with shape (L, M)
        b1: First layer biases with shape (M,)
        W2: Second layer weights with shape (M, N)
        b2: Second layer biases with shape (N,)
        """
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_dim, hidden_dim)
        self.params['b1'] = np.zeros(hidden_dim)
        self.params['W2'] = std * np.random.randn(hidden_dim, output_dim)
        self.params['b2'] = np.zeros(output_dim)

    def loss_grad(self, X, y=None, reg=0.0):
        """
        Compute the loss and gradients.

        Inputs:
        
        X: Input data of shape (N, D). Each X[i] is a training sample.
        y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
           an integer in the range 0 <= y[i] < C. This parameter is optional; if it
           is not passed then we only return scores, and if it is passed then we
           instead return the loss and gradients.
        reg: Regularization strength.

        Returns:
        
        - If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
          the score for class c on input X[i].
        - If y is not None, return a tuple of:
          - loss: Loss (data loss and regularization loss) for this batch of training
            samples.
          - grads: Dictionary mapping parameter names to gradients of those parameters
            with respect to the loss function; has the same keys as self.params.
        """
        # Unpack variables from the params dictionary
        W1 = self.params['W1']
        b1 = self.params['b1']
        W2 = self.params['W2'] 
        b2 = self.params['b2']
        N, D = X.shape

        #--------------------------------------- forward propagation ---------------------------------------                     
        
        scores = None
        loops = False
        
        if loops == True:
            
            # 1.1 Task:
            # Compute the class scores for the input.
            # Use the weights and biases to perform a forward propagation and store the results
            # in the scores variable, which should be an array of shape (N, C).
            # Start with a naive implementation with at least 2 loops.

            ######################################## START OF YOUR CODE ########################################
            M, C = W2.shape
            # first fully connected layer
            z1 = np.zeros([N, M])
            for i in range(N):  # loop over samples
                for j in range(M):  # loop over hidden layer
                    for k in range(D):  # loop over input layer
                        z1[i][j] += X[i][k]*W1[k][j]
                    z1[i][j] += b1[j]  # add bias
            # ReLU
            z1 = np.maximum(0, z1)
            # second fully connected layer
            z2 = np.zeros([N, C])
            for i in range(N):  # loop over samples
                for j in range(C):  # loop over output layer
                    for k in range(M):  # loop over hidden layer
                        z2[i][j] += z1[i][k]*W2[k, j]
                    z2[i][j] += b2[j]  # add bias
            # output
            scores = z2
            ######################################## END OF YOUR CODE ##########################################

        else:
            
            # Task 1.2:
            # Now implement the same forward propagation as you did above using no loops.
            # If you are done set the parameter loops to False to test your code.

            ######################################## START OF YOUR CODE ########################################

            # create output after first weights, separately for each sample
            x1 = np.zeros([W1.shape[1], N])

            x1[:, 0] = W1.T.dot(X[0].T) + b1
            x1[:, 1] = W1.T.dot(X[1].T) + b1
            x1[:, 2] = W1.T.dot(X[2].T) + b1
            x1[:, 3] = W1.T.dot(X[3].T) + b1
            x1[:, 4] = W1.T.dot(X[4].T) + b1

            # apply ReLU
            relu = lambda x: np.max([0, x])
            vectorized_ReLU = np.vectorize(relu)
            x1 = vectorized_ReLU(x1)

            # calculate network output (scores), separately for each sample
            out = np.zeros([W2.shape[1], N])

            out[:, 0] = W2.T.dot(x1[:, 0]) + b2
            out[:, 1] = W2.T.dot(x1[:, 1]) + b2
            out[:, 2] = W2.T.dot(x1[:, 2]) + b2
            out[:, 3] = W2.T.dot(x1[:, 3]) + b2
            out[:, 4] = W2.T.dot(x1[:, 4]) + b2

            scores = out.T

        ######################################## END OF YOUR CODE ##########################################

        # Jump out if y is not given.
        if y is None:
            return scores

        #--------------------------------------- loss function ---------------------------------------------
        
        loss = None
        
        # Task 2:
        # Compute the loss with softmax and store it in the variable loss. Include L2 regularization for W1 and W2.
        # Make sure to handle numerical instabilities.

        ######################################## START OF YOUR CODE ########################################

        # TODO: @All: - see lecture 4 from slide 40
        #       - see: https://deepnotes.io/softmax-crossentropy

        # function to calculate a stable softmax of a given array (handle numerical instabilities)
        def softmax_stable(x):
            e_res = np.exp(x - np.max(x))
            return e_res / np.sum(e_res)

        # function to calculate normal softmax of a given array
        def softmax(x):
            e_res = np.exp(x)
            return e_res / np.sum(e_res)

        # number of classes
        C = b2.size

        # calculate softmax of class scores
        sm_results = np.zeros([N, C])
        for i in range(N):
            sm_results[i] = softmax_stable(scores[i])

        # calculate L2-Norm for both weight matrices
        l2_w1 = sum(sum(np.square(W1)))
        l2_w2 = sum(sum(np.square(W2)))

        # slow loss calculation (just for see what fast loss is doing)
        losses = np.zeros(N)
        for i in range(N):
            losses[i] = - np.log(sm_results[i, y[i]])
        loss_slow = 1/N * sum(losses) + reg * (l2_w1 + l2_w2)

        # fast loss calculation
        log_likelihood = -np.log(sm_results[range(N), y])
        loss = 1 / N * sum(log_likelihood) + reg * (l2_w1 + l2_w2)

        ######################################## END OF YOUR CODE ##########################################

        #--------------------------------------- back propagation -------------------------------------------
        
        grads = {}

        # Task 3:
        # Compute the derivatives of the weights and biases (back propagation).
        # Store the results in the grads dictionary, where 'W1' referes to the gradient of W1 etc.
        
        ######################################## START OF YOUR CODE ########################################

        sm_scores = softmax_stable(scores)
        #  upstream gradient dloss/dscores
        dL_dsm_scores = -1 / 5 * 1 / sm_scores[range(N), y]
        # local gradient dsm_scores/dscores
        dsm_scores_dscores = np.zeros([N, N, C])
        for n in range(N):
            for i in range(N):
                for j in range(C):
                    if n == i:
                        if j == y[n]:
                            dsm_scores_dscores[n][i][j] = (np.exp(scores[n][j]) * np.sum(np.exp(scores[n])) - np.square(
                                np.exp(scores[n][j]))) / np.square(np.sum(np.exp(scores[n])))
                        else:
                            dsm_scores_dscores[n][i][j] = -np.exp(scores[n][y[n]]) * np.exp(scores[n][j]) / np.square(
                                np.sum(np.exp(scores[n])))
                    else:
                        dsm_scores_dscores[n][i][j] = 0
        # upstream gradient dL_dscores
        dL_dscores = np.zeros([N, C])
        for n in range(N):
            for i in range(N):
                for j in range(C):
                    dL_dscores[i][j] += dL_dsm_scores[n] * dsm_scores_dscores[n][i][j]
        # local dscores/dW2
        dscores_dW2 = np.zeros([N, C, M, C])
        for n in range(N):
            for i in range(C):
                for j in range(M):
                    for l in range(C):
                        if i == l:
                            dscores_dW2[n][i][j][l] = z2[n][j]
        # upstream gradient dL/dW2
        dL_dW2 = np.zeros([M, C])
        for i in range(M):
            for j in range(C):
                for k in range(N):
                    for l in range(C):
                        dL_dW2[i][j] += dL_dscores[k][l] * dscores_dW2[k][l][i][j]
        # local gradient dscors/db2
        # dscors_db2 = np.zeros(N, C, C)
        # upstream gradient dL/db2
        dL_db2 = np.zeros(C)
        for i in range(C):
            dL_db2[i] = np.sum(dL_dscores[range(N), i])
        # local gradient dscores/dz2
        dscores_dz2 = np.zeros([N, C, M])
        for n in range(N):
            for i in range(C):
                for j in range(M):
                    dscores_dz2[n][i][j] = W2[j][i]
        # upstream gradient dL/dz2
        dL_dz2 = np.zeros([N, M])
        for n in range(N):
            for k in range(C):
                dL_dz2[n] = dL_dscores[n][k] * dscores_dz2[n][k]
        # local gradient dz2/dz1
        dz2_dz1 = np.zeros([N, M, M])
        for n in range(N):
            for i in range(M):
                for j in range(M):
                    if z1[n][j] > 0:
                        dz2_dz1[n][i][j] = 1
        # upstream gradient dL/dz1
        dL_dz1 = np.zeros([N, M])
        for n in range(N):
            for k in range(M):
                dL_dz1[n] += dL_dz2[n][k] * dz2_dz1[n][k]
        # local gradient dz1/dW1
        dz1_dW1 = np.zeros([N, M, D, M])
        for n in range(N):
            for i in range(M):
                for j in range(D):
                    for l in range(M):
                        if i == l:
                            dz1_dW1[n][i][j][l] = X[n][j]
        # upstram gradient dL/dW1
        dL_dW1 = np.zeros([N, D, M])
        for n in range(N):
            for k in range(M):
                dL_dW1[n] += dL_dz1[n][k] * dz1_dW1[n][k]
        # upstream gradient dL/db1
        dL_db1 = dL_dz1

        grads = {'W1': dL_dW1, 'b1': dL_db1, 'W2': dL_dW2, 'b2': dL_db2}

        ######################################## END OF YOUR CODE ##########################################

        return loss, grads

    def train(self, X, y, X_val, y_val,
              learning_rate=1e-3, learning_rate_decay=0.95,
              reg=5e-6, num_iters=100,
              batch_size=200, verbose=False):
        """
        Train this neural network using stochastic gradient descent.

        Inputs:
        
        - X: A numpy array of shape (N, D) giving training data.
        - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
          X[i] has label c, where 0 <= c < C.
        - X_val: A numpy array of shape (N_val, D) giving validation data.
        - y_val: A numpy array of shape (N_val,) giving validation labels.
        - learning_rate: Scalar giving learning rate for optimization.
        - learning_rate_decay: Scalar giving factor used to decay the learning rate
          after each epoch.
        - reg: Scalar giving regularization strength.
        - num_iters: Number of steps to take when optimizing.
        - batch_size: Number of training examples to use per step.
        - verbose: boolean; if true print progress during optimization.
        """
        num_train = X.shape[0]
        iterations_per_epoch = max(num_train / batch_size, 1)

        # Use SGD to optimize the parameters in self.model
        loss_history = []
        train_acc_history = []
        val_acc_history = []

        for it in range(num_iters):
            X_batch = None
            y_batch = None

            # Task 4.1: 
            # Create a random minibatch of training data X and labels y, and stor
            # them in X_batch and y_batch.
            ######################################## START OF YOUR CODE ########################################

            pass  # to be replaced by your code

            ######################################## END OF YOUR CODE ##########################################

            # Compute loss and gradients using the current minibatch
            loss, grads = self.loss_grad(X_batch, y=y_batch, reg=reg)
            loss_history.append(loss)

            # Task 4.2:
            # Update the parameters of the network (in self.params) by using stochastic gradient descent. 
            # You will need to use the gradients in the grads dictionary.
            ######################################## START OF YOUR CODE ########################################

            pass  # to be replaced by your code

            ######################################## END OF YOUR CODE ##########################################

            if verbose and it % 100 == 0:
                print('iteration %d / %d: loss %f' % (it, num_iters, loss))

            # Every epoch, check train and val accuracy and decay learning rate.
            if it % iterations_per_epoch == 0:
                # Check accuracy
                train_acc = (self.predict(X_batch) == y_batch).mean()
                val_acc = (self.predict(X_val) == y_val).mean()
                train_acc_history.append(train_acc)
                val_acc_history.append(val_acc)

                # Decay learning rate
                learning_rate *= learning_rate_decay

        return {
          'loss_history': loss_history,
          'train_acc_history': train_acc_history,
          'val_acc_history': val_acc_history,
        }

    def predict(self, X):
        """
        Use the trained network to predict labels for the data points. 
        For each data point we predict scores for each of the C classes, 
        and assign each data point to the class with the highest score.

        Inputs:
        
        X: A numpy array of shape (N, D) giving N D-dimensional data points to
          classify.

        Returns:
        
        y_pred: A numpy array of shape (N,) giving predicted labels for each of
          the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
          to have class c.
        """
        y_pred = None

        # Task 4.3: 
        # Implement this function to predict labels for the data points.
        ######################################## START OF YOUR CODE ########################################

        pass  # to be replaced by your code

        ######################################## END OF YOUR CODE ##########################################

        return y_pred