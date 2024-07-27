aws apigateway create-rest-api --name ContactFormAPI

$API_ID = (aws apigateway get-rest-apis --query "items[?name=='ContactFormAPI'].id" --output text)
$RESOURCE_ID = (aws apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/'].id" --output text)

aws apigateway create-resource --rest-api-id $API_ID --parent-id $RESOURCE_ID --path-part "submit"

$SUBMIT_RESOURCE_ID = (aws apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/submit'].id" --output text)

aws apigateway put-method --rest-api-id $API_ID --resource-id $SUBMIT_RESOURCE_ID --http-method POST --authorization-type NONE

$LAMBDA_ARN = (aws lambda get-function --function-name ContactFormProcessor --query "Configuration.FunctionArn" --output text)

aws apigateway put-integration --rest-api-id $API_ID --resource-id $SUBMIT_RESOURCE_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod

$API_ENDPOINT = "https://$API_ID.execute-api.us-east-1.amazonaws.com/prod/submit"