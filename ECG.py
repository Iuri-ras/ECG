import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# Streamlit App Configuration
st.title("ECG Signal Filtering Application")
st.markdown("Upload your **ECG CSV file** to apply Bandpass Filtering (0.5 - 40 Hz)")

# File Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Define Bandpass Filter
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Main Logic
if uploaded_file:
    # Load the data
    st.markdown("### Original Signal")
    df = pd.read_csv(uploaded_file)
    
    # Display DataFrame
    st.write(df.head())

    # Assume the first column is time and the second is ECG
    time = df.iloc[:, 0]
    ecg_signal = df.iloc[:, 1]
    
    # Plot Original Signal
    fig, ax = plt.subplots()
    ax.plot(time, ecg_signal, label='Original Signal')
    ax.set_title("Original ECG Signal")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    plt.legend()
    st.pyplot(fig)
    
    # Apply Bandpass Filter (0.5 to 40 Hz)
    filtered_signal = bandpass_filter(ecg_signal, 0.5, 40, fs=250, order=4)

    # Plot Filtered Signal
    st.markdown("### Filtered Signal")
    fig, ax = plt.subplots()
    ax.plot(time, filtered_signal, color='orange', label='Filtered Signal')
    ax.set_title("Filtered ECG Signal")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    plt.legend()
    st.pyplot(fig)

    # QRS Visibility Comment
    st.markdown("**QRS Visibility Improved:** The high-frequency noise and baseline drift have been filtered out, making the QRS complex more prominent and clearer to analyze.")
