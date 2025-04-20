import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
import configparser
from typing import List
from hammingCode import Hamming
from decoder import Decoder
from bitExtraction import demodulate_from_file



#region Config Parsing
config = configparser.ConfigParser()
config.read('config.ini')
general_config = config['GENERAL']

bitTime = int(general_config['BitTime'])
crcLength = int(general_config['CRCLength'])
crcDivisor = general_config['CRCDivisor']
paddingChar = general_config['PaddingCharacter']
sampleRate = int(float(general_config['SampleRate']))
windowSize = int(general_config['WindowSize'])

#endregion

# windowsPerBit = (bitTime/1000) * sampleRate / windowSize
# windowsPerBit = math.ceil(windowsPerBit)


# # Uses scipy library
# def computeNormalizedXcor(a, b):
#     normalized_a = (a - np.mean(a)) / (np.std(a))
#     normalized_b = (b - np.mean(b)) / (np.std(b))
#     c = signal.correlate(normalized_a, normalized_b,
#                          mode="full") / max(len(a), len(b))
#     center = int(len(c)/2)
#     return (c[center], center, c)

class Demodulator:

    def __init__(self, preambleThres: float = 0.05, bitThres: float = 0.03):
       
        self._preambleThres = preambleThres 
        self._bitThres = bitThres

    
    # def setBitThreshold(self, bitThres: float = 0.03) -> None:
    #     self._bitThres = bitThres

    
    # def setBitThreshold(self, preambleThres: float = 0.05) -> None:
    #     self._preambleThres = preambleThres
    
    
    # def _computeNormalizedXcor(self, a, b):
    #     normalized_a = (a - np.mean(a)) / (np.std(a))
    #     normalized_b = (b - np.mean(b)) / (np.std(b))
    #     c = signal.correlate(normalized_a, normalized_b,
    #                          mode="full") / max(len(a), len(b))
    #     center = int(len(c)/2)
    #     return (c[center], center, c)

    
    def _correctErrors(self, demodulatedFrame: List[int]) -> str:
        frame = demodulatedFrame
        chunk_size = 7
        ham = Hamming()
        dec = ""
        for i in range(0, len(frame), chunk_size):
            chunk = frame[i:i+chunk_size]
            binary_string = str(chunk)
            bit_list = [int(bit) for bit in binary_string] 
            reshaped_array = np.array(bit_list).reshape(-1, 1) 
            corrected = ham.getOriginalMessage(reshaped_array)[0]
            x = ""
            for i in corrected:
                x += str(i)
            dec += x
        return dec

    
    def _decodeFrame(self, correctedFrame: str) -> str:
        decod = Decoder(divisor=crcDivisor, crc_length=crcLength, paddingChar=paddingChar)
        m = decod.decode(correctedFrame)
        return m

    
    def demodulateSignal(self, data: List[int], statusChange=None, decodedFrame=None) -> List[List[int]]:
        payloadLength = 56
        numOfBitsToDecode = payloadLength
        decoded = []
        bitsDecoded = 0
        framesDecoded = 0
        statusChange("Detecting Preamble")
        preamble = "10101010"
        first8bits= data[0:8]
        payloadBits= data[8:]
        print("Demodulated Bits: ",data)
        if(first8bits == preamble):
            #print("Preamble detected")
            corrected = self._correctErrors(payloadBits)
            message = self._decodeFrame(corrected)
            while bitsDecoded >= numOfBitsToDecode:
                  bitsDecoded = 0
                  framesDecoded += 1
                  corrected = self._correctErrors(decoded)
                  message = self._decodeFrame(corrected)
                  decodedFrame(message)
                  statusChange("Detecting Preamble")
                  decoded = []
        statusChange("Decoding Finished")
        return message


def eventHandler(x):
    print(x)

if __name__ == "__main__":
    data = list(np.fromfile(open("/home/sandali/Documents/Encoder/new10bitscollect.bin"), dtype=np.float64))
    demod = Demodulator()
    dec = demod.demodulateSignal(data, eventHandler, eventHandler)
    print(dec)
    # x = ['01110011011010000110000110001010', '01101011011101000110100010110100', '01101001001000000111001101000001',
    #      '01100001011000110110100010011111', '01101001011011100111010010100111', '01101000011000010010110111010100']
    # for c in decodedMessages: print(c, end="")
    # print(x)





