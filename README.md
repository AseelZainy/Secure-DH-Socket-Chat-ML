# 🔒 Secure Socket Chat with Diffie-Hellman, Cryptanalysis, & ML Traffic Detection

A comprehensive Cybersecurity project demonstrating secure communication, cryptographic attack vectors, and Machine Learning-based network traffic analysis.

## 📌 Project Overview
- **Encrypted Socket Communication (`alice.py` & `bob.py`):** Multi-threaded TCP chat using Diffie-Hellman Key Exchange ($P=23, G=5$) and XOR Encryption.
- **Cryptanalytic Attack (`Eve_Attack.py`):** Brute-force simulation executing a Discrete Logarithm attack to recover secret session keys.
- **Performance Analysis (`brute.py`):** Benchmarking key size resistance against brute-force duration using Matplotlib.
- **AI/ML Traffic Classifier (`DiffieHellman_ML.py`):** Random Forest model distinguishing between encrypted and plaintext payloads via Entropy Analysis.

## 🚀 How to Run
1. Run Bob (Server): `python bob.py`
2. Run Alice (Client): `python alice.py`
3. Execute Brute-Force Attack: `python Eve_Attack.py`
4. Run AI Packet Analyzer: `python DiffieHellman_ML.py`
