#!/usr/bin/env python3
"""
Bob - Simple Chat Server with Basic Diffie-Hellman (P=23, G=5)
Waits for Alice's public key first, sends his, derives shared key, then chats XOR encrypted.
"""

import socket
import threading

# Diffie-Hellman parameters (shared publicly)
P = 23  # Prime modulus
G = 5    # Generator

class BobChat:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.sock = None
        self.client_sock = None
        self.shared_key = 0
    
    def mod_pow(self, base, exp, mod):
        """Simple modular exponentiation: base^exp mod mod"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    def dh_handshake(self):
        """1. Receive Alice's public key first, 2. send Bob's, 3. derive shared key"""
        print("\n🔑 DIFFIE-HELLMAN HANDSHAKE (P=23, G=5)")
        
        # Create server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        
        print("Step 1: Bob picks secret 'b' and computes B = G^b mod P")
        print("👂 Waiting for Alice...")
        
        # Bob's secret
        self.b = 15  # Bob picks secret number b (1 < b < P)
        self.B = self.mod_pow(G, self.b, P)  # B = 5^15 mod 23 = 19
        
        print(f"   Bob secret: b={self.b}")
        print(f"   Bob public: B={self.B}")
        
        # Accept connection and receive Alice's public key FIRST
        self.client_sock, addr = self.sock.accept()
        print(f"🔗 Alice connected from {addr}")
        
        data = self.client_sock.recv(1024).decode()
        _, alice_A = data.split(':')
        alice_A = int(alice_A)
        print(f"📥 Alice → Bob: PK:{alice_A}")
        
        # Send Bob's public key
        self.client_sock.sendall(f"PK:{self.B}".encode())
        print(f"📤 Bob → Alice: PK:{self.B}")
        
        # Derive shared key: K = A^b mod P
        self.shared_key = self.mod_pow(alice_A, self.b, P)
        print(f"🔒 Bob computes shared key: {alice_A}^{self.b} mod 23 = {self.shared_key}")
        print("✅ SHARED KEY SECURELY ESTABLISHED!")
        print(f"🔍 Both have same key: {self.shared_key}")
    
    def xor_encrypt(self, message):
        """Simple XOR encryption with shared key (byte by byte)"""
        # تم تعديل هذا الجزء ليتعامل مع المفتاح الرقمي مباشرة لتجنب التشفير الخاطئ
        encrypted = []
        for char in message:
            encrypted.append(ord(char) ^ self.shared_key)
        return ''.join(chr(c) for c in encrypted)
    
    def xor_decrypt(self, encrypted):
        """XOR decryption (same as encryption)"""
        return self.xor_encrypt(encrypted)
    
    def receive_messages(self):
        """Receive and decrypt messages"""
        while True:
            try:
                data = self.client_sock.recv(1024).decode()
                if not data or data == "BYE":
                    print("\n👋 Alice disconnected")
                    break
                if data.startswith("MSG:"):
                    message = data[4:]
                    decrypted = self.xor_decrypt(message)
                    # أضفنا flush=True لضمان ظهور الرسالة فوراً
                    print(f"\n👩 Alice: {decrypted}", flush=True)
                    print("👤 Bob> ", end='', flush=True)
            except:
                break
    
    def run(self):
        """Main chat loop"""
        try:
            self.dh_handshake()
            
            print("\n" + "="*50)
            print("💬 SECURE CHAT STARTED (XOR encrypted)")
            print("📝 Type messages (or 'quit' to exit)")
            print("="*50)
            
            # Start receiver thread
            recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
            recv_thread.start()
            
            # Send messages
            while True:
                # الـ prompt يظهر بشكل نظيف بفضل الـ threading
                message = input("👤 Bob> ")
                if message.lower() in ['quit', 'bye', 'exit']:
                    self.client_sock.sendall("BYE".encode())
                    break
                
                if message.strip():
                    encrypted = self.xor_encrypt(message)
                    # نرسل الرسالة فوراً ونستخدم sendall لضمان وصولها
                    self.client_sock.sendall(f"MSG:{encrypted}".encode())
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        finally:
            if self.client_sock:
                self.client_sock.close()
            if self.sock:
                self.sock.close()

if __name__ == "__main__":
    bob = BobChat()
    bob.run()