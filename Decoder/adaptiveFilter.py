import numpy as np
import matplotlib.pyplot as plt

def lms_filter(reference_signal, target_signal, mu=0.05, filter_order=256):
    # Initialize variables
    n_samples = len(target_signal)
    weights = np.zeros(filter_order)  # Adaptive filter weights
    output_signal = np.zeros(n_samples)
    error_signal = np.zeros(n_samples)

    # Pad reference signal to match filter order
    padded_ref = np.pad(reference_signal, (filter_order - 1, 0), mode='reflect')

    for n in range(n_samples):
        # Get current input vector (last 'filter_order' samples)
        x_n = padded_ref[n:n + filter_order][::-1]

        # Compute filter output
        output_signal[n] = np.dot(weights, x_n)

        # Compute error signal
        error_signal[n] = target_signal[n] - output_signal[n]

        # Update weights using LMS rule
        weights += mu * error_signal[n] * x_n
        
    return output_signal, error_signal

# Load binary signal data
ref_file_path = "./data/10bps/8cm/signal.bin"
target_file_path = "./data/10bps/8cm/noise.bin"
reference_noise = np.fromfile(ref_file_path, dtype=np.float64)
target_signal = np.fromfile(target_file_path, dtype=np.float64)

# Ensure both signals have the same length
min_length = min(len(reference_noise), len(target_signal))
reference_noise = reference_noise[:min_length]
target_signal = target_signal[:min_length]

# Apply LMS filter
filtered_output, filtered_error = lms_filter(reference_noise, target_signal)

# Save filtered signal
output_file_path = "./data/10bps/8cm/filtered_signal.bin"
np.array(filtered_output, dtype=np.float64).tofile(output_file_path)

# Plot Results
plt.figure(figsize=(12, 6))

# Plot PSD for target and filtered signal
plt.subplot(2, 1, 1)
plt.title("Power Spectral Density (PSD)")
plt.psd(target_signal, NFFT=1024, label="Target Signal PSD", color="orange")
plt.psd(filtered_output, NFFT=1024, label="Filtered Signal PSD", color="green")
plt.legend()

# Plot error signal to check performance
plt.subplot(2, 1, 2)
plt.title("Error Signal (Target - Filtered Output)")
plt.plot(filtered_error, color="red")
plt.xlabel("Sample Index")
plt.ylabel("Error Amplitude")

plt.tight_layout()
plt.show()
