<?php
/**
 * Nextcloud Primary Object Storage Configuration for AWS S3 & SSE-KMS
 * 
 * SecureVault Phase 2: Zero-Trust Storage Tiering & KMS Integration
 * This file is automatically loaded by Nextcloud from /var/www/html/config/
 */

$s3Bucket = getenv('OBJECTSTORE_S3_BUCKET') ?: getenv('S3_BUCKET_NAME');

if (!empty($s3Bucket)) {
    $s3Key = getenv('OBJECTSTORE_S3_KEY') ?: getenv('AWS_ACCESS_KEY_ID') ?: '';
    $s3Secret = getenv('OBJECTSTORE_S3_SECRET') ?: getenv('AWS_SECRET_ACCESS_KEY') ?: '';
    $s3Region = getenv('OBJECTSTORE_S3_REGION') ?: getenv('AWS_REGION') ?: 'us-east-1';
    $useSse = getenv('OBJECTSTORE_S3_USE_SSE');
    $s3Host = getenv('OBJECTSTORE_S3_HOST');
    $s3Port = getenv('OBJECTSTORE_S3_PORT');
    $pathStyle = getenv('OBJECTSTORE_S3_PATH_STYLE');
    $useSsl = getenv('OBJECTSTORE_S3_SSL');

    $s3Arguments = [
        'bucket'         => $s3Bucket,
        'autocreate'     => false,
        'key'            => $s3Key,
        'secret'         => $s3Secret,
        'region'         => $s3Region,
        'use_ssl'        => ($useSsl !== 'false'),
        'use_path_style' => ($pathStyle === 'true'),
    ];

    // Enable Server-Side Encryption (SSE-KMS / SSE-S3)
    if ($useSse === 'true' || $useSse === '1' || strtolower((string)$useSse) === 'kms' || strtolower((string)$useSse) === 'aes256') {
        $s3Arguments['use_sse'] = true;
    }

    // Custom hostname/port (for MinIO or local mock S3)
    if (!empty($s3Host)) {
        $s3Arguments['hostname'] = $s3Host;
        if (!empty($s3Port)) {
            $s3Arguments['port'] = (int)$s3Port;
        }
    }

    $CONFIG = [
        'objectstore' => [
            'class'     => '\\OC\\Files\\ObjectStore\\S3',
            'arguments' => $s3Arguments,
        ],
    ];
}
