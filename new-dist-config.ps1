$config = aws cloudfront get-distribution-config --id E29RLSOCAU7O4Y | ConvertFrom-Json
$ETag = $config.ETag
$config = $config.DistributionConfig

# Add domain names to Aliases
$config.Aliases = @{
    Quantity = 2
    Items = @("sreenikethaathreya.com", "www.sreenikethaathreya.com")
}

# Ensure ViewerCertificate settings are correct
$config.ViewerCertificate.CloudFrontDefaultCertificate = $false
$config.ViewerCertificate.ACMCertificateArn = "arn:aws:acm:us-east-1:824116678613:certificate/8d37296f-80e4-4388-b0f1-45378783bedd"
$config.ViewerCertificate.SSLSupportMethod = "sni-only"
$config.ViewerCertificate.MinimumProtocolVersion = "TLSv1.2_2021"
$config.ViewerCertificate.Certificate = $config.ViewerCertificate.ACMCertificateArn
$config.ViewerCertificate.CertificateSource = "acm"

# Enable compression
$config.DefaultCacheBehavior.Compress = $true

$config | ConvertTo-Json -Depth 100 | Out-File -Encoding ascii -NoNewline updated-dist-config.json

aws cloudfront update-distribution --id E29RLSOCAU7O4Y --distribution-config file://updated-dist-config.json --if-match $ETag