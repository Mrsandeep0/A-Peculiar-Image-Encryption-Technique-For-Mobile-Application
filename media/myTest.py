from cryptosteganography import CryptoSteganography

crypto_steganography = CryptoSteganography('GV7NRBDJ6U')

# Save the encrypted file inside the image
# crypto_steganography.hide('241.jpg', '1_out.png', 'this is Secret Message')

secret = crypto_steganography.retrieve('output/test_23.png')

print(secret)
# My secret message