<?php
// download-handler.php

$file_id = get_query_var('assetarc_download_file');
if (!$file_id) {
    status_header(404);
    echo 'File not specified.';
    exit;
}

if (!isset($_COOKIE['access_token'])) {
    status_header(403);
    echo 'Access denied. You must be logged in.';
    exit;
}

$access_token = $_COOKIE['access_token'];
$api_url = 'http://eng-vault/vault/download/' . $file_id;

$response = wp_remote_get($api_url, [
    'timeout' => 60,
    'cookies' => ['access_token' => $access_token]
]);

if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
    status_header(404);
    echo 'File not found or you do not have permission to access it.';
    exit;
}

// Get headers and body from the response
$headers = wp_remote_retrieve_headers($response);
$body = wp_remote_retrieve_body($response);

// Set headers to trigger download
header('Content-Type: ' . $headers['content-type']);
header('Content-Disposition: ' . $headers['content-disposition']);
header('Content-Length: ' . strlen($body));
header('Connection: close');

// Output the file content
echo $body;
exit;
?>
