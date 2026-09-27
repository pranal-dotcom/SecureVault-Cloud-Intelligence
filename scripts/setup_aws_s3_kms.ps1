<#
.SYNOPSIS
    SecureVault: AWS S3 & KMS CMK Automation Script (PowerShell)
    Phase 2: Zero-Trust Storage Tiering & KMS Integration

.DESCRIPTION
    Automates the provisioning of:
    1. Zero-Trust Amazon S3 Bucket (Block Public Access enforced)
    2. S3 Bucket Versioning
    3. AWS KMS Customer-Managed Key (CMK)
    4. S3 Default Server-Side Encryption with KMS (SSE-KMS) and S3 Bucket Key

.PARAMETER BucketName
    The name of the S3 bucket to create. Defaults to securevault-primary-storage-<timestamp>.

.PARAMETER Region
    The AWS Region. Defaults to us-east-1 (or $env:AWS_REGION).
#>

[CmdletBinding()]
param (
    [Parameter(Position = 0)]
    [string]$BucketName = "securevault-primary-storage-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())",

    [Parameter(Position = 1)]
    [string]$Region = $(if ($env:AWS_REGION) { $env:AWS_REGION } else { "us-east-1" })
)

$ErrorActionPreference = "Stop"
$KmsAlias = "alias/securevault-storage-key"

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " SecureVault AWS S3 & KMS Automated Provisioning (PowerShell)" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "Target S3 Bucket Name : $BucketName"
Write-Host "Target AWS Region     : $Region"
Write-Host "KMS Key Alias         : $KmsAlias"
Write-Host "------------------------------------------------------------------------------"

# 1. Verify AWS CLI & Authentication
Write-Host "[1/5] Verifying AWS authentication..." -ForegroundColor Yellow
try {
    $callerJson = aws sts get-caller-identity --output json | ConvertFrom-Json
    $accountId = $callerJson.Account
    Write-Host "Authenticated AWS Account: $accountId (ARN: $($callerJson.Arn))" -ForegroundColor Green
} catch {
    Write-Error "Failed to authenticate with AWS CLI. Please ensure 'aws configure' has been run."
    exit 1
}

# 2. Create S3 Bucket
Write-Host "[2/5] Creating S3 bucket '$BucketName' in region '$Region'..." -ForegroundColor Yellow
if ($Region -eq "us-east-1") {
    aws s3api create-bucket --bucket $BucketName --region $Region | Out-Null
} else {
    aws s3api create-bucket --bucket $BucketName --region $Region --create-bucket-configuration LocationConstraint=$Region | Out-Null
}
Write-Host "Bucket created successfully." -ForegroundColor Green

# 3. Enable Strict Block Public Access (Zero-Trust)
Write-Host "[3/5] Enforcing Zero-Trust 'Block Public Access' configuration..." -ForegroundColor Yellow
aws s3api put-public-access-block `
    --bucket $BucketName `
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" | Out-Null
Write-Host "Public Access Block applied." -ForegroundColor Green

# 4. Enable S3 Bucket Versioning
Write-Host "[4/5] Enabling S3 bucket versioning..." -ForegroundColor Yellow
aws s3api put-bucket-versioning `
    --bucket $BucketName `
    --versioning-configuration Status=Enabled | Out-Null
Write-Host "Versioning enabled." -ForegroundColor Green

# 5. Create Customer-Managed Key (CMK) in AWS KMS & Apply SSE-KMS
Write-Host "[5/5] Creating Customer-Managed KMS Key (CMK)..." -ForegroundColor Yellow
$kmsJson = aws kms create-key `
    --description "SecureVault Customer-Managed Key (CMK) for Nextcloud Object Storage" `
    --key-usage ENCRYPT_DECRYPT `
    --origin AWS_KMS `
    --region $Region `
    --output json | ConvertFrom-Json

$kmsKeyId = $kmsJson.KeyMetadata.KeyId
$kmsKeyArn = $kmsJson.KeyMetadata.Arn
Write-Host "Created KMS Key ID : $kmsKeyId" -ForegroundColor Green
Write-Host "Created KMS Key ARN: $kmsKeyArn" -ForegroundColor Green

# Create KMS Alias
try {
    aws kms create-alias --alias-name $KmsAlias --target-key-id $kmsKeyId --region $Region | Out-Null
    Write-Host "Created KMS Alias: $KmsAlias" -ForegroundColor Green
} catch {
    Write-Warning "Alias $KmsAlias could not be created or already exists."
}

# Apply SSE-KMS Default Encryption
Write-Host "Applying SSE-KMS default encryption to bucket..." -ForegroundColor Yellow
$encryptionConfig = @"
{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "$kmsKeyId"
            },
            "BucketKeyEnabled": true
        }
    ]
}
"@

$tempEncFile = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tempEncFile -Value $encryptionConfig
aws s3api put-bucket-encryption --bucket $BucketName --server-side-encryption-configuration file://$tempEncFile | Out-Null
Remove-Item -Path $tempEncFile -Force

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " SUCCESS: AWS S3 & KMS Infrastructure Provisioned!" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "Add the following variables to your .env file:`n" -ForegroundColor White
Write-Host "S3_BUCKET_NAME=$BucketName" -ForegroundColor Yellow
Write-Host "OBJECTSTORE_S3_BUCKET=$BucketName" -ForegroundColor Yellow
Write-Host "OBJECTSTORE_S3_REGION=$Region" -ForegroundColor Yellow
Write-Host "KMS_KEY_ID=$kmsKeyArn" -ForegroundColor Yellow
Write-Host "OBJECTSTORE_S3_USE_SSE=true" -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan
