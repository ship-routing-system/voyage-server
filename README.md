# 항로 탐색 서비스(Voyage Navigation Service)

## Objective

출발지에서 도착지까지 가는 최빈 경로를 탐색하는 유조선 항로 탐색 서비스. 

## 환경구성

### 1. Worker Server을 위한 Set-Up

항로 탐색 서비스 중 Voyage Cost을 생성하는 **Worker Server**는 GCP에서 제공하고 있는 서버리스 컴퓨팅 환경인 
[Google Cloud Function](https://cloud.google.com/functions?hl=ko)을 활용하여 구현되어 있습니다. 
Google Cloud Fuction을 동작시키기 위해서는 함수 배포 권한, 빅쿼리 접근 권한 등을 받아야 합니다.

1. **프로젝트 관리자에게 권한을 가진 json 형식의 키 파일을 받기**
    > 프로젝트을 수행하기 위해서는, Google BigQuery | Google Storage | Google Cloud Function | Google Logging 등에 대한 접근 및 수정 권한을 받아야 합니다. 
    * 관리의 용이성을 위해 `/credentials` 폴더에 저장해 주세요.
2. [Google Cloud Sdk](https://cloud.google.com/sdk/docs/quickstarts?hl=ko) 설치하기
    > Google Cloud Function을 배포하기 위해서는 gcloud의 설치가    

3. [서비스 계정으로 승인](https://cloud.google.com/sdk/docs/authorizing?hl=ko)
    ````shell
    gcloud auth activate-service-account [ACCOUNT] --key-file=[KEY_FILE]
    ````

## 서버 구성

### 1. Worker Server

출발지에서 도착지까지 가는 최빈 경로를 탐색하는 서비스

#### (1) `ship_cost` 함수 배포하기

````shell
gcloud functions deploy ship_cost --entry-point calculate_cost --runtime python37 --trigger-http --allow-unauthenticated  --region=asia-northeast3 --timeout=180 --memory=1024 --service-account=service-developer-660@vlcc-304007.iam.gserviceaccount.com  --env-vars-file config.yaml
```` 

#### (2) `ship_cost` 함수 호출하기

- **Terminal에서 호출 테스트**
    ````shell
    curl -d '{"imo_no": 6758466}' -H "Content-Type: application/json" -X POST https://asia-northeast3-vlcc-304007.cloudfunctions.net/ship_cost
    ````
  
- **Python에서 호출 테스트**
    ````python
    import requests
    res = requests.post("https://asia-northeast3-vlcc-304007.cloudfunctions.net/ship_cost",
                         json={"imo_no":6758466})
    ````