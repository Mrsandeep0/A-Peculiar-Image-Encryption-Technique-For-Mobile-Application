from cryptosteganography import CryptoSteganography

message = None
with open('sample.mp3', "rb") as f:
    message = f.read()

crypto_steganography = CryptoSteganography('My secret password key')

# Save the encrypted file inside the image
crypto_steganography.hide('input_image_name.jpg', 'output_image_file.png', message)

# Retrieve the file ( the previous crypto_steganography instance could be used but I instantiate a brand new object
# with the same password key just to demonstrate that can it can be used to decrypt)
crypto_steganography = CryptoSteganography('My secret password key')
decrypted_bin = crypto_steganography.retrieve('output_image_file.png')

# Save the data to a new file
with open('decrypted_sample.mp3', 'wb') as f:
    f.write("secret_bin")