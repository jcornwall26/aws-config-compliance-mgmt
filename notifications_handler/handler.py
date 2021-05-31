import json
import boto3
import os

S3_BUCKET = os.environ['S3_BUCKET']

def lambda_handler(event, context):

    for sns_record in event['Records']:
        sns_message_id = sns_record['Sns']['MessageId']
        message = json.loads(sns_record['Sns']['Message'])
        detail = message['detail']

        flatten_detail = {
            'configRuleARN': detail['configRuleARN'],
            'resultRecordedTime': detail['newEvaluationResult']['resultRecordedTime'],
            'complianceType': detail['newEvaluationResult']['complianceType'],
            'configRuleName': detail['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['configRuleName'],
            'resourceType': detail['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['resourceType'],
            'resourceId': detail['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['resourceId'],
        }

        print(flatten_detail)

        #push detail as object to s3
        client = boto3.client('s3')
        client.put_object(Bucket=S3_BUCKET, Body=json.dumps(flatten_detail).encode('utf_8'), Key=f'config-notifications/{sns_message_id}')

    return {
        'statusCode': 200,
        'body': json.dumps('Processed event succesfully')
    }
