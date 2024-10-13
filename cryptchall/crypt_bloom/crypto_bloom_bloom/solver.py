#!/usr/bin/env python3

from ast import literal_eval
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
from hashlib import sha256
from re import *
from sage.all import GF, PolynomialRing


    
output,cipher_hex = open('output.txt', 'r').read().splitlines()

all_enc_messages = literal_eval(output)

ct = bytes.fromhex(cipher_hex)
already_decrypted = []

for enc_messages in all_enc_messages:
    for iv,msg in enc_messages:
        for i in range(2):
            try:
                key = f"{i}"*256
                keyhex = sha256(key.encode()).digest()
                decipher = unpad(AES.new(keyhex, AES.MODE_CBC, bytes.fromhex(iv)).decrypt(bytes.fromhex(msg)), AES.block_size)
                if decipher not in already_decrypted:
                    already_decrypted.append(decipher)
                    
                    # print(decipher.decode())
                    break
                
            except:
                continue
            
shares = []
for msg in already_decrypted:
    msg = msg.decode()
    if (share_match := search(r'Share#\d+?#: \((\d+?), (\d+?)\)', msg)):
        shares.append((int(share_match.group(1)), int(share_match.group(2))))

    if (gf_match := search(r'GF\((\d+?)\)', msg)):
        Fp = GF(int(gf_match.group(1)))
        
P = PolynomialRing(Fp, 'x')
polynomial = P.lagrange_polynomial(shares)
key = long_to_bytes(int(polynomial(0)))


print(unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), AES.block_size).decode())