import jwt
import datetime
import hmac
import hashlib
import base64

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

# 3. 수동으로 서명 생성(HMAC-SHA256)
def generate_hmac_signature(header, payload, secret_key):
    # Base64Url 인코딩된 Header, Payload
    message = f"{header}.{payload}"

    # HMAC-SHA256 서명 생성
    signature = hmac.new(secret_key.encode('utf-8'), msg=message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    # Base64Url 인코딩된 서명 반환
    signature_b64url = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return signature_b64url

# 4. JWT 검증
def verify_jwt(token):
    try:
        # JWT를 헤더, 정보, 서명으로 분리
        header_b64, payload_b64, signature_b64 = token.split(".")

        # 수동으로 서명 생성
        except_signature = generate_hmac_signature(header_b64, payload_b64, SECRET_KEY)

        # PyJWT를 사용하여 검증(기본 검증)
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # 서명이 동일한지 확인
        if signature_b64 == except_signature:
            return {"+ 검증 성공": decoded_payload}
        else:
            return {"- 서명 불일치": "변조된 토큰!"}
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

