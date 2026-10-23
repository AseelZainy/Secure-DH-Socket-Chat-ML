import time
import matplotlib.pyplot as plt

# brute force
def brute_dlp(g, y, p):
    for x in range(1, p):
        if pow(g, x, p) == y:
            return x
    return None


#  (key sizes)
test_values = {
    "8-bit": (2, 5, 23),
    "12-bit": (2, 8, 1019),
    "16-bit": (2, 15, 50021),
    "18-bit": (2, 20, 100003),
    "20-bit": (2, 25, 200003)
}

sizes = []
times = []

print("Key Size | Time (seconds) | Found x")
print("-" * 45)

repeats = 500  # تكرار للقيم عشان القياس يكون أدق

for name, (g, x_real, p) in test_values.items():
    y = pow(g, x_real, p)  

    start = time.perf_counter()

    for _ in range(repeats):
        x_found = brute_dlp(g, y, p)

    end = time.perf_counter()

    elapsed = (end - start) / repeats

    print(f"{name} | {elapsed:.6f} sec | x = {x_found}")

    sizes.append(name)
    times.append(elapsed)


# الرسم
plt.figure()
plt.plot(sizes, times, marker='o')
plt.xlabel("Key Size")
plt.ylabel("Time (seconds)")
plt.title("Brute Force Time vs Key Size (Diffie-Hellman)")
plt.grid()

plt.show()



plt.figure()
plt.plot(sizes, times, marker='o')
plt.xlabel("Key Size")
plt.ylabel("Time (seconds)")
plt.title("Brute Force Time vs Key Size (Diffie-Hellman)")
plt.grid()

plt.show()