### 1. get_data deploy하기
````shell
gcloud functions deploy get_data --entry-point get_data --runtime python37 --trigger-http --allow-unauthenticated --region=asia-northeast3 --timeout=180 --memory=1024 --service-account=service-developer-660@vlcc-304007.iam.gserviceaccount.com  --env-vars-file config.yaml
````

### 1. ship_cost deploy하기
````shell
gcloud functions deploy ship_cost --entry-point calculate_cost --runtime python37 --trigger-http --allow-unauthenticated  --region=asia-northeast3 --timeout=180 --memory=1024 --service-account=service-developer-660@vlcc-304007.iam.gserviceaccount.com  --env-vars-file config.yaml
````