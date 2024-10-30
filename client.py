# client_combined.py
import socket
import os
import base64

# Konstanta dan fungsi dari encryption_utils.py
BLOCK_SIZE = 8  # Ukuran blok dalam byte untuk CBC

def pad(data):
    padding_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + chr(padding_len) * padding_len

def unpad(data):
    padding_len = ord(data[-1])
    return data[:-padding_len]

def xor_bytes(data1, data2):
    return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])

def to_base64(data):
    return base64.b64encode(data).decode('utf-8')

# Tabel permutasi yang sama dengan server
PERMUTATION_TABLE = [2, 0, 3, 1, 6, 4, 7, 5]

def permute_block_with_table(block):
    """Permutasi blok menggunakan tabel permutasi"""
    return bytes(block[PERMUTATION_TABLE[i]] for i in range(len(block)))

def inverse_permute_block_with_table(block):
    """Permutasi terbalik menggunakan tabel permutasi"""
    inverse_table = [0] * len(PERMUTATION_TABLE)
    for i, pos in enumerate(PERMUTATION_TABLE):
        inverse_table[pos] = i
    return bytes(block[inverse_table[i]] for i in range(len(block)))

def encrypt_cbc(plaintext, key, iv):
    plaintext = pad(plaintext)
    ciphertext = b''
    prev_block = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE].encode()
        block = xor_bytes(permute_block_with_table(block), prev_block)  # Permutasi + XOR dengan blok sebelumnya
        encrypted_block = xor_bytes(block, key.encode())  # XOR dengan kunci
        ciphertext += encrypted_block
        prev_block = encrypted_block

    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    plaintext = b''
    prev_block = iv

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted_block = xor_bytes(block, key.encode())
        plaintext_block = inverse_permute_block_with_table(xor_bytes(decrypted_block, prev_block))  # Permutasi terbalik + XOR dengan blok sebelumnya
        plaintext += plaintext_block
        prev_block = block

    return unpad(plaintext.decode())

# Fungsi client dari client.py
def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    key = "mysecretk"  # 8-byte key
    iv = client_socket.recv(8)  # Menerima IV dari server

    while True:
        message = input("Kirim pesan -> ")
        if message.lower().strip() == 'bye':
            break

        # Enkripsi pesan dan kirim ke server
        encrypted_message = encrypt_cbc(message, key, iv)
        encrypted_message_base64 = to_base64(encrypted_message)
        print(f"[CLIENT] Pesan terenkripsi ke server: {encrypted_message_base64}")
        client_socket.send(encrypted_message)

        # Terima dan dekripsi respons dari server
        encrypted_response = client_socket.recv(1024)
        encrypted_response_base64 = to_base64(encrypted_response)
        print(f"[CLIENT] Pesan terenkripsi dari server: {encrypted_response_base64}")
        
        decrypted_response = decrypt_cbc(encrypted_response, key, iv)
        print(f"[CLIENT] Pesan setelah didekripsi: {decrypted_response}")

    client_socket.close()

if __name__ == '__main__':
    client_program()
