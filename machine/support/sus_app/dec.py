import base64

# Base64 encoded password
enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"

# ASCII encoded key
key = "armando".encode("ascii")


def get_password():
    # Decode the base64 encoded password
    array = base64.b64decode(enc_password)

    # Create a new byte array for the decoded password
    array2 = bytearray(len(array))

    # XOR each byte with the key and 0xDF
    for i in range(len(array)):
        array2[i] = array[i] ^ key[i % len(key)] ^ 0xDF

    # Convert the resulting byte array back to a string
    return array2.decode()


# Get and print the decoded password
password = get_password()
print(password)
