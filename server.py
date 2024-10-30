# server.py
import socket
import os
import base64

BLOCK_SIZE = 8  # Block size in bytes for CBC

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

# Tabel permutasi
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


def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", str(address))

    key = "mysecretk"  # 8-byte key
    iv = os.urandom(8)  # 8-byte random IV

    # Send the IV to the client
    conn.send(iv)

    while True:
        encrypted_data = conn.recv(1024)
        if not encrypted_data:
            break

        # Decode the received encrypted message to Base64 for display
        encrypted_data_base64 = to_base64(encrypted_data)
        print(f"\n[SERVER] Pesan terenkripsi dari klien: {encrypted_data_base64}")

        # Decrypt and display the received message
        decrypted_message = decrypt_cbc(encrypted_data, key, iv)
        print(f"[SERVER] Pesan setelah didekripsi: {decrypted_message}")

        # Prepare a response
        response = input("Balas pesan -> ")
        encrypted_response = encrypt_cbc(response, key, iv)
        encrypted_response_base64 = to_base64(encrypted_response)
        print(f"[SERVER] Pesan terenkripsi ke klien: {encrypted_response_base64}")
        
        conn.send(encrypted_response)

    conn.close()

if __name__ == '__main__':
    server_program()
