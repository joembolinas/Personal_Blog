
from utils.security import check_password
h = '01cf59a639b39f2fefec17fc7a43b9fb$932834a379251955a02870e808d2398'
p = 'admin123'
print(f"Match: {check_password(h, p)}")
