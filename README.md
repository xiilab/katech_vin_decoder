# VIN Decoder API

KADaP (Korea Automotive Data Platform) - 차량 식별 번호(VIN) 디코더 API

## 개요

VIN(Vehicle Identification Number)을 입력하면 제조국, 제조사, 차종 등의 정보를 JSON 형태로 제공하는 REST API입니다.

## 기능

- VIN 번호 해석 및 정보 제공
- Swagger UI를 통한 API 문서 제공
- 리버스 프록시 환경 지원

## 기술 스택

- Python 3.11
- Flask 3.x
- Flask-RESTX 1.3.x
- Werkzeug (ProxyFix, DispatcherMiddleware)

## 설치 및 실행

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python app.py
```

애플리케이션이 `http://localhost:5555`에서 실행됩니다.

### Docker 실행

#### 이미지 빌드
```bash
docker build -t vin-decoder .
```

#### 기본 모드로 실행
```bash
docker run -p 5555:5555 vin-decoder
```

#### 리버스 프록시 모드로 실행 (SUBFOLDER 설정)
```bash
docker run -p 5555:5555 -e SUBFOLDER=/api vin-decoder
```

## 환경 변수

| 환경 변수 | 설명 | 기본값 | 예시 |
|-----------|------|--------|------|
| `SUBFOLDER` | 서브폴더 경로 (리버스 프록시용) | 없음 | `/api`, `/v1` |

### SUBFOLDER 설정 효과

`SUBFOLDER` 환경 변수를 설정하면:
- 자동으로 ProxyFix 미들웨어가 적용됩니다
- 모든 API가 지정된 서브폴더 경로에 마운트됩니다
- X-Forwarded-* 헤더를 올바르게 처리합니다
- `/health` 엔드포인트는 SUBFOLDER 외부에서도 접근 가능 (Kubernetes/Knative readinessProbe용)

## API 엔드포인트

### SUBFOLDER 미설정 시

- **Root**: `http://localhost:5000/` → `/doc`로 리다이렉트
- **Health Check**: `http://localhost:5000/health`
- **Swagger UI**: `http://localhost:5000/doc`
- **VIN Decoder**: `GET http://localhost:5000/APIs/vin-decoder?VIN={vin_number}`

### SUBFOLDER=/api 설정 시

- **Root**: `http://localhost:5000/` → `/api/doc`로 리다이렉트
- **Health Check**: `http://localhost:5000/health` (SUBFOLDER 외부에서도 접근 가능)
- **Swagger UI**: `http://localhost:5000/api/doc`
- **VIN Decoder**: `GET http://localhost:5000/api/APIs/vin-decoder?VIN={vin_number}`

## 사용 예시

### API 요청

```bash
# 기본 모드
curl "http://localhost:5555/APIs/vin-decoder?VIN=KMHEM44CPLU123456"

# SUBFOLDER 모드
curl "http://localhost:5555/api/APIs/vin-decoder?VIN=KMHEM44CPLU123456"
```

### 응답 예시

```json
{
  "제조국": "Korea",
  "제조사": "Hyundai",
  "차량구분": "Sedan",
  "차종": "Mid-size",
  "세부차종": "Advanced",
  "차체형상": "Number of doors",
  "안전장치": "Airbag",
  "배기량": "2500cc",
  "보안코드": "LHD(Left Hand Drive)",
  "제작연도": "2020",
  "생산공장": "Ulsan, Korea",
  "일련번호": "123456"
}
```

## 리버스 프록시 설정

### Nginx 설정 예시

```nginx
location /api/ {
    proxy_pass http://localhost:5555/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Prefix /api;
}
```

애플리케이션 실행 시:
```bash
SUBFOLDER=/api python app.py
```

또는 Docker:
```bash
docker run -p 5555:5555 -e SUBFOLDER=/api vin-decoder
```

## Knative/Kubernetes 배포

### Knative Service YAML

`knative-service.yaml` 파일을 참고하여 배포하세요.

주요 설정:
- `SUBFOLDER` 환경 변수: 프록시 경로 설정
- `readinessProbe`: `/health` 엔드포인트 사용
- `livenessProbe`: `/health` 엔드포인트 사용

```bash
kubectl apply -f knative-service.yaml
```

### 주의사항

Knative에서 긴 프록시 경로를 사용할 때:
- SUBFOLDER는 끝에 슬래시(`/`)를 포함하지 마세요
- 예: `/api/proxy/apps/kadap-saas-dev/marketplace-299` (올바름)
- 예: `/api/proxy/apps/kadap-saas-dev/marketplace-299/` (틀림)

## 프로젝트 구조

```
vin_decoder/
├── app.py                  # Flask 애플리케이션 메인
├── decoder.py              # VIN 디코딩 로직
├── flask_vin.py            # API 엔드포인트 정의
├── requirements.txt        # Python 의존성
├── Dockerfile              # Docker 이미지 빌드 파일
├── .dockerignore           # Docker 빌드 제외 파일
├── .gitignore              # Git 제외 파일
├── knative-service.yaml    # Knative Service 배포 YAML
└── README.md               # 프로젝트 문서
```

## 개발 내용

### v0.0.6
- 리버스 프록시 지원 추가 (`SUBFOLDER` 환경 변수)
- ProxyFix 미들웨어 자동 적용
- DispatcherMiddleware를 통한 서브폴더 마운팅
- Swagger UI 경로 자동 조정
- Docker 지원 추가

### 주요 기능
- **VIN Decoder**: 차량 식별 번호 해석
- **Swagger UI**: API 문서 자동 생성
- **리버스 프록시**: nginx/Apache 등과 연동 가능
- **경로 격리**: SUBFOLDER 설정 시 기본 경로 차단

## 라이선스

이 프로젝트는 KADaP (Korea Automotive Data Platform)의 일부입니다.

## 문의

버그 리포트나 기능 요청은 이슈 트래커를 통해 제출해주세요.

