#!/usr/bin/env python3
import socket
import threading

P = 23
G = 5

class AliceChat:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.sock = None
        self.shared_key = 0
    
    def mod_pow(self, base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    def dh_handshake(self):
        print("\n🔑 DIFFIE-HELLMAN HANDSHAKE (P=23, G=5)")
        self.a = 6
        self.A = self.mod_pow(G, self.a, P)
        
        print(f"   Alice secret: a={self.a}")
        print(f"   Alice public: A={self.A}")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.sendall(f"PK:{self.A}".encode())
        print(f"📤 Alice → Bob: PK:{self.A}")
        
        data = self.sock.recv(1024).decode()
        _, bob_B = data.split(':')
        bob_B = int(bob_B)
        print(f"📥 Bob → Alice: PK:{bob_B}")
        
        self.shared_key = self.mod_pow(bob_B, self.a, P)
        print(f"🔒 Alice computes shared key: {bob_B}^{self.a} mod 23 = {self.shared_key}")
        print("✅ SHARED KEY SECURELY ESTABLISHED!")
    
    def xor_encrypt(self, message):
        """تم التعديل هنا: نستخدم المفتاح مباشرة كرقم لضمان التوافق مع كود بوب"""
        encrypted = []
        for char in message:
            # استخدام المفتاح الرقمي مباشرة مع الحرف
            encrypted.append(ord(char) ^ self.shared_key)
        return ''.join(chr(c) for c in encrypted)
    
    def xor_decrypt(self, encrypted):
        return self.xor_encrypt(encrypted)
    
    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data or data == "BYE":
                    print("\n👋 Bob disconnected")
                    break
                if data.startswith("MSG:"):
                    message = data[4:]
                    # هنا يتم فك التشفير قبل الطباعة لضمان ظهور النص واضح
                    decrypted = self.xor_decrypt(message)
                    # إضافة flush=True لضمان ظهور الرسالة فوراً في الترمنال
                    print(f"\n👤 Bob: {decrypted}", flush=True)
                    print("👩 Alice> ", end='', flush=True)
            except:
                break
    
    def run(self):
        try:
            self.dh_handshake()
            print("\n" + "="*50)
            print("💬 SECURE CHAT STARTED (XOR encrypted)")
            print("📝 Type messages (or 'quit' to exit)")
            print("="*50)
            
            recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
            recv_thread.start()
            
            while True:
                # الـ prompt يظهر بشكل صحيح مع الـ threading
                message = input("👩 Alice> ")
                if message.lower() in ['quit', 'bye', 'exit']:
                    self.sock.sendall("BYE".encode())
                    break
                
                if message.strip():
                    encrypted = self.xor_encrypt(message)
                    # استخدام sendall لضمان إرسال كامل البيانات فوراً
                    self.sock.sendall(f"MSG:{encrypted}".encode())
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        finally:
            if self.sock: self.sock.close()

if __name__ == "__main__":
    alice = AliceChat()
    alice.run()