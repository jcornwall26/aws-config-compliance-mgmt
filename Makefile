BUCKET_NAME=ct-config-compliance-mgmt-mwap-npd
REGION=us-east-1

create-s3-bucket:
	aws s3api create-bucket --bucket $(BUCKET_NAME) --region $(REGION)

create-lambda-role:
	aws iam create-role --role-name ct-config-compliance-mgmt-notifications-handler-role --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
	aws iam attach-role-policy --role-name ct-config-compliance-mgmt-notifications-handler-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

create-notifications-handler-lambda-package:
	cd ./notifications_handler && zip ./handler.zip ./handler.py

update-notifications-handler:create-notifications-handler-lambda-package
	aws lambda update-function-configuration --function-name ct-config-compliance-mgmt-notifications-handler --environment Variables={S3_BUCKET=$(BUCKET_NAME)} --region $(REGION)
	aws lambda update-function-code --function-name ct-config-compliance-mgmt-notifications-handler --zip-file fileb://notifications-handler/handler.zip --region $(REGION)

create-notifications-handler:create-notifications-handler-lambda-package
	aws lambda create-function --function-name ct-config-compliance-mgmt-notifications-handler --zip-file fileb://notifications_handler/handler.zip --handler handler.lambda_handler --runtime python3.8 --role arn:aws:iam::277754835857:role/ct-config-compliance-mgmt-notifications-handler-role --region us-east-1 --environment Variables={S3_BUCKET=$(BUCKET_NAME)}

run-tests:
	python -m pytest -c tests/test_config.ini