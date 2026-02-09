import jwt
import datetime

# 1. secret key 설정 (대칭키)
SECRET_KEY = 'myservice_api-myservice_api_secret_key'

# 2. JWT 생성(서명 포함)
def create_jwt():
    payload = {
        "user_id": 1,
        "user_uid": "18d4e9b9-c149-467e-885d-a12352e52810",
        "name": "kkh",
        "iat": datetime.datetime.now(datetime.UTC), # 발급시간
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1) # 만료시간 1시간
    }

    # JWT 생성(HS256)
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# 3. JWT 검증
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "- token expired"
    except jwt.InvalidTokenError:
        return "- invalid token"

# 실행 예제
if __name__ == "__main__":
    token = create_jwt()
    print(f"Generated Token:{token}")

    decoded_data = verify_jwt(token)
    print(f"Verified Payload:{decoded_data}")

