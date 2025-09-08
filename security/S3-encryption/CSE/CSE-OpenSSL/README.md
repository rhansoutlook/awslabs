This is the contents of folder CSE-OpenSSL

The steps to carry out client side encryption (CSE) on an object and uploading the object are as follows

0. source assumerole.sh Role_CSEOperator
1. Create a file with text of your choice
2. openssl rand 32 > `<key file name>`
3. openssl enc -aes-256-cbc -salt -pbkdf2 -in `<unencrypted file>`  -out `<encrypted file>` -pass file:./`<key file name>`
4. aws s3api put-object --bucket `<bucket name>` --key `<encrypted file>` --body `<encrypted file>`
5. delete local copies of `<encrypted file>` and `<unencrypted file>`
6. aws s3api get-object --bucket `<bucket name>`  --key `<encrypted file>`  `<encrypted file name>`
7. openssl enc -d -aes-256-cbc -salt -pbkdf2 -in `<encrypted file>` -out `<unencrypted file>` -pass file:./`<key file name>`
