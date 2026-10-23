import time
import math

def mod_pow(base, exp, mod):
    """Efficient modular exponentiation (Binary Exponentiation)Computes: base^exp mod mod"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1  # exp //= 2
        base = (base * base) % mod
    return result

def brute_force_dlog(P, G, A):
    """ Solve Discrete Logarithm Problem using Brute Force Find 'a' such that: G^a (mod P) = A"""
    print(f"Starting brute force search for secret 'a'...")
    print(f"P = {P}, G = {G}, A = {A}")
    
    # Check trivial cases
    if mod_pow(G, 1, P) == A:
        return 1
    
    # Brute force search from 2 to P-2
    for a in range(2, P):
        if mod_pow(G, a, P) == A:
            print(f"Secret 'a' found: a = {a}!")
            return a
    
    print("No solution found!")
    return None

def main():
    print("=== Eve's Diffie-Hellman Attack Tool ===")
    print("P = 23, G = 5")
    
    # Get public keys from user
    try:
        A = int(input("Enter Alice's public key (A): "))
        B = int(input("Enter Bob's public key (B): "))
    except ValueError:
        print("Error: Please enter valid integers!")
        return
    
    P = 23
    G = 5
    
    # Measure attack time
    start_time = time.time()
    
    # Find Alice's secret (a)
    a_found = brute_force_dlog(P, G, A)
    
    if a_found is None:
        print("Attack failed!")
        return
    
    # Calculate shared session key (K = B^a mod P)
    K = mod_pow(B, a_found, P)
    end_time = time.time()
    
    # Print results
    print("\n" + "="*40)
    print("Attack Results:")
    print(f"Alice's secret (a) = {a_found}")
    print(f"Shared Session Key (K) = {K}")
    print(f"Attack time: {end_time - start_time:.4f} seconds")
    print("="*40)
    
    print("\n🎉 Diffie-Hellman cracked successfully!")
    print("Eve can now decrypt all messages!")

if __name__ == "__main__":
    main()