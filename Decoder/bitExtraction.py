import numpy as np
from scipy.signal import welch
import warnings
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def read_binary_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    return bits

def calc_welch(segment, fs=20000000, nperseg=1024):
    # Calculate Power Spectral Density using Welch's method
    normalized_segment = (segment - np.min(segment)) / (np.max(segment) - np.min(segment))
    f, Pxx = welch(normalized_segment, fs=fs, nperseg=nperseg)
    return np.mean(Pxx)  # Return mean PSD value for simplicity

def demodulate_bits(psd_values,bitSample, bitTime, higherThreshold, lowerThreshold):

    middlePoint = bitTime // 2
    firstHalf = bitSample[0:middlePoint]
    secondHalf = bitSample[middlePoint:bitTime]

    #calculate PSD mean for both half of sample
    firstPSD = calc_welch(firstHalf)
    secondPSD = calc_welch(secondHalf)
    
    # psd_values.append(firstPSD)
    # psd_values.append(secondPSD)
    

    #compare PSD means with thresholds
    if firstPSD > higherThreshold and secondPSD < lowerThreshold:
        return 0
    elif firstPSD < lowerThreshold and secondPSD > higherThreshold:
        return 1
    else:
        return 1


def demodulate_from_file(file_path, bitTime=2000000, higherThreshold=2e-10, lowerThreshold=1.8e-10):

    # Read bits from the binary file
    bits = list(np.fromfile(open(file_path, "rb"), dtype=np.float64))
    
    # Demodulate bits in segments
    demodulated_bits = []
    psd_values = []
    for i in range(0, len(bits), bitTime):
        if i + bitTime <= len(bits): 
            bitSegment = bits[i:i + bitTime]
            demodulated_bit = demodulate_bits(psd_values, bitSegment, bitTime, higherThreshold, lowerThreshold)
            demodulated_bits.append(demodulated_bit)
            #warnings.filterwarnings("ignore")

    # plt.figure(figsize=(10, 5))
    # plt.plot(psd_values, label="First Half PSD Mean", marker='o', linestyle='-')
    # plt.xlabel("Segment Index")
    # plt.ylabel("PSD Mean Value")
    # plt.title("First & Second Half PSD Mean Values")
    # plt.legend()
    # plt.grid()
    # plt.show()
    return demodulated_bits

if __name__ == "__main__":
    file_path = './data/10bps/2cm/signal.bin'
    result = demodulate_from_file(file_path)
    print(len(result))
    print("Demodulated Bits:", result)




