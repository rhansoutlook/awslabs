This is the contents of folder CSE-KMS

This is the contents of folder CSE-OpenSSL

The steps to carry out client side encryption (CSE) on an object using AWS KMS CMK and upload the object.

Step 0 - Grant Privileges to Default User based on Least Privilege
source assumerole.sh Role_CSEOperator

Step 1 - Create the File to Encrypt
Create a file with text of your choice

Step 2 – Generate A Data Key from CMK
aws kms generate-data-key --key-id alias/`<customer amster key alias>`  --key-spec AES_256 --output json > `data_key.json`

Step 3 – Extract Plain text key
jq -r .Plaintext `data_key.json` | base64 --decode > `plaintextkey.bin`

Step 4  - Extract Cipher Text key
jq -r .CiphertextBlob `data_key.json` > `ciphertextkey.b64`

Step 5  - Use Plaintext key to Encrypt our file
openssl enc -aes-256-cbc -salt -pbkdf2 -in `unencrypted.txt` -out `encrypted.txt` -pass file:./`plaintextkey.bin`

Step 6 - Delete the plaintext key
rm `plaintextkey.bin`

Step 7 – Upload the encrypted object to our bucket
aws s3api put-object --bucket `<bucket name>` --key `encryptedusimgkms.txt`  --body `encrypted.txt` --metadata encryptedkey=`"$cat ciphertextkey.b64)"`

Step 8 – Delete the cipher text key
rm  `ciphertextkey.b64`

Step 9 – Retrieve the object from our bucket
aws s3api get-object  --bucket `<bucket name>`  --key `encryptedusimgkms.txt` `encrypted.txt`  --query Metadata.encryptedkey  --output text > `ciphertextkey.b64`

Step 10 -Convert from base64 to binary
base64 --decode `ciphertextkey.b64` > `downloaded_key.bin`

Step 11 - converting the cipher data key (which was stored in metadata and later retrieved) back into its plaintext form
aws kms decrypt --ciphertext-blob fileb://`downloaded_key.bin`  --output json | jq -r .Plaintext | base64 --decode > `plaintextkey.bin`

Step 12 - Use the plaintext key to decrypt the encrypted file
openssl enc -d -aes-256-cbc -salt -pbkdf2 -in `encrypted.txt` -out `unencrypted.txt` -pass file:./`plaintextkey.bin`
