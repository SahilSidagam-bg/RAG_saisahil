from urllib.parse import quote_plus

username = "saisahil"
password = "RAGpass@1"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

print(f"Encoded Username: {encoded_username}")
print(f"Encoded Password: {encoded_password}")