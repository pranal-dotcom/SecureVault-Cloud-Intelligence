#!/usr/bin/env bash
# ==============================================================================
# SecureVault: AWS S3 & KMS CMK Automation Script
# Phase 2: Zero-Trust Storage Tiering & KMS Integration
# ==============================================================================

set -euo pipefail

BUCKET_NAME="${1:-securevault-primary-storage-$(date +%s)}"
REGION="${2:-${AWS_REGION:-us-east-1}}"
KMS_ALIAS="alias/securevault-storage-key"

echo "=============================================================================="
echo " SecureVault AWS S3 & KMS Automated Provisioning"
echo "=============================================================================="
echo "Target S3 Bucket Name : ${BUCKET_NAME}"
echo "Target AWS Region     : ${REGION}"
echo "KMS Key Alias         : ${KMS_ALIAS}"
echo "------------------------------------------------------------------------------"

# 1. Verify AWS CLI & Authentication
echo "[1/5] Verifying AWS authentication..."
if ! command -v aws &> /dev/null; then
    echo "ERROR: AWS CLI is not installed. Please install and configure AWS CLI first." >&2
    exit 1
fi

CALLER_IDENTITY=$(aws sts get-caller-identity --output json)
ACCOUNT_ID=$(echo "$CALLER_IDENTITY" | grep -o '"Account": "[^"]*' | cut -d'"' -f4)
echo "Authenticated AWS Account: ${ACCOUNT_ID}"

# 2. Create S3 Bucket
echo "[2/5] Creating S3 bucket '${BUCKET_NAME}' in region '${REGION}'..."
if [ "${REGION}" == "us-east-1" ]; then
    aws s3api create-bucket \
        --bucket "${BUCKET_NAME}" \
        --region "${REGION}"
else
    aws s3api create-bucket \
        --bucket "${BUCKET_NAME}" \
        --region "${REGION}" \
        --create-bucket-configuration LocationConstraint="${REGION}"
fi

# 3. Enable Strict Block Public Access (Zero-Trust)
echo "[3/5] Enforcing Zero-Trust 'Block Public Access' configuration..."
aws s3api put-public-access-block \
    --bucket "${BUCKET_NAME}" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# 4. Enable S3 Bucket Versioning
echo "[4/5] Enabling S3 bucket versioning..."
aws s3api put-bucket-versioning \
    --bucket "${BUCKET_NAME}" \
    --versioning-configuration Status=Enabled

# 5. Create Customer-Managed Key (CMK) in AWS KMS & Apply SSE-KMS
echo "[5/5] Creating Customer-Managed KMS Key (CMK)..."
KMS_KEY_ID=$(aws kms create-key \
    --description "SecureVault Customer-Managed Key (CMK) for Nextcloud Object Storage" \
    --key-usage ENCRYPT_DECRYPT \
    --origin AWS_KMS \
    --region "${REGION}" \
    --query "KeyMetadata.KeyId" \
    --output text)

KMS_KEY_ARN="arn:aws:kms:${REGION}:${ACCOUNT_ID}:key/${KMS_KEY_ID}"
echo "Created KMS Key ID : ${KMS_KEY_ID}"
echo "Created KMS Key ARN: ${KMS_KEY_ARN}"

# Assign alias
aws kms create-alias \
    --alias-name "${KMS_ALIAS}" \
    --target-key-id "${KMS_KEY_ID}" \
    --region "${REGION}" || echo "Notice: Alias ${KMS_ALIAS} already exists or was updated."

# Apply SSE-KMS Default Encryption to Bucket
echo "Applying SSE-KMS default encryption with S3 Bucket Keys enabled..."
aws s3api put-bucket-encryption \
    --bucket "${BUCKET_NAME}" \
    --server-side-encryption-configuration '{
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "aws:kms",
                    "KMSMasterKeyID": "'"${KMS_KEY_ID}"'"
                },
                "BucketKeyEnabled": true
            }
        ]
    }'

echo "=============================================================================="
echo " SUCCESS: AWS S3 & KMS Infrastructure Provisioned!"
echo "=============================================================================="
echo "Add the following variables to your .env file:"
echo ""
echo "S3_BUCKET_NAME=${BUCKET_NAME}"
echo "OBJECTSTORE_S3_BUCKET=${BUCKET_NAME}"
echo "OBJECTSTORE_S3_REGION=${REGION}"
echo "KMS_KEY_ID=${KMS_KEY_ARN}"
echo "OBJECTSTORE_S3_USE_SSE=true"
echo "=============================================================================="
