
from utils.security import hash_password, check_password
pw = 'admin123'
h = hash_password(pw)
print(f"HASH:{h}")
print(f"VERIFY:{check_password(h, pw)}")
with open('good_hash.txt', 'w') as f:
    f.write(h)
