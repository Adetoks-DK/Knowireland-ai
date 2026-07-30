from app.security import hash_password

new_password = "TestPassword123!"

hashed = hash_password(new_password)

print("New password:")
print(new_password)

print("\nHashed password:")
print(hashed)