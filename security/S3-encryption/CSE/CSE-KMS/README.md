This is the contents of folder CSE-KMS

This is the contents of folder CSE-OpenSSL

The steps to carry out client side encryption (CSE) on an object using AWS KMS CMK and upload the object.

0. source assumerole.sh Role_CSEOperator
1. Create a file with text of your choice
2. aws kms generate-data-key --key-id alias/`<customer amster key alias>`  --key-spec AES_256 --output json > `data_key.json`
3. jq -r .Plaintext `data_key.json` | base64 --decode > `plaintextkey.bin`
4. jq -r .CiphertextBlob data_key.json > `ciphertextkey.b64`
5. openssl enc -aes-256-cbc -salt -pbkdf2 -in `unencrypted.txt` -out encrypted.txt -pass file:./plaintextkey.bin
