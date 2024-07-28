# Create the API
$api_id = aws apigateway create-rest-api --name ContactFormAPI --query 'id' --output text

# Get the root resource ID
$root_resource_id = aws apigateway get-resources --rest-api-id $api_id --query 'items[0].id' --output text

# Create a resource
$resource_id = aws apigateway create-resource --rest-api-id $api_id --parent-id $root_resource_id --path-part submit --query 'id' --output text

# Create a POST method
aws apigateway put-method --rest-api-id $api_id --resource-id $resource_id --http-method POST --authorization-type NONE

# Set up the integration with Lambda
aws apigateway put-integration `
    --rest-api-id $api_id `
    --resource-id $resource_id `
    --http-method POST `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:824116678613:function:ContactFormProcessor/invocations

# Deploy the API
aws apigateway create-deployment --rest-api-id $api_id --stage-name prod

echo $api_id