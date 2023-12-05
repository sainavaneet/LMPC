# Parameters

## Introduction

For assessing the performances of LMPC sampled data control and H2 optimal control, we compared the quadratic costs of them. The constraints for the cost function include:

### Parameters
- Total Time (\(T\)): \(T = 10\) s
- State Weight Matrix (\(Q\)): \(Q = \text{diag}([1, 1, 1])\)
- Control Weight Matrix (\(R\)): \(R = \text{diag}([0.1, 0.1])\)
- Sampling Time (\(\gamma\)): \(\gamma = 0.1\) s
- LMPC Control Input Limits:
  - \(v_{\text{max}} = 0.3\), \(v_{\text{min}} = 0.0\)
  - \(\omega_{\text{max}} = \frac{\pi}{4}\), \(\omega_{\text{min}} = -\frac{\pi}{4}\)
- Gain Matrix (\(k\)): 

  \[
  k = \begin{bmatrix}
    0.4662 & 0.2978 & 0.2067 \\
    0.8341 & 1.2165 & 1.3492
  \end{bmatrix}
  \]

### Quadratic Cost Function

The quadratic cost function for a single timestep is given by:

\[
J_{\text{total}} = \sum_{k=1}^{N} (\mathbf{x}_k^T \mathbf{Q} \mathbf{x}_k + \mathbf{u}_k^T \mathbf{R} \mathbf{u}_k)
\]

Where \(N = 2\).

## Results
Total Cost Value for LMPC (\(J=10\)): 8.98516268901749 \\
Total Cost Value for H2: 18.775862036811883
