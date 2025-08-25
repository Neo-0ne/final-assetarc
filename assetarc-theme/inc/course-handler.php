<?php
/**
 * Handles the business logic for the course pages.
 */

// Define the base URL for the lifecycle service
define('LIFECYCLE_API_URL', 'http://localhost:5005');

/**
 * Safely gets the user's access token from cookies.
 *
 * @return string|null The access token or null if not found.
 */
function get_current_user_token() {
    return isset($_COOKIE['access_token']) ? sanitize_text_field($_COOKIE['access_token']) : null;
}

/**
 * Checks if a user is enrolled in a specific course.
 *
 * @param string $token The user's access token.
 * @param int $course_id The ID of the course.
 * @return bool True if enrolled, false otherwise.
 */
function is_user_enrolled_in_course($token, $course_id) {
    if (!$token) {
        return false;
    }

    $api_url = LIFECYCLE_API_URL . '/lifecycle/course/' . intval($course_id) . '/progress';
    $response = wp_remote_get($api_url, [
        'headers' => [
            'Cookie' => 'access_token=' . $token
        ],
        'timeout' => 10,
    ]);

    // If we get a 200 OK, they are enrolled. A 403 Forbidden means not enrolled.
    return wp_remote_retrieve_response_code($response) === 200;
}

/**
 * Fetches the full structure of a course.
 *
 * @param int $course_id The ID of the course.
 * @return array|null The course data or null on error.
 */
function get_course_data($course_id) {
    $api_url = LIFECYCLE_API_URL . '/lifecycle/course/' . intval($course_id);
    $response = wp_remote_get($api_url, ['timeout' => 10]);

    if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
        error_log('Failed to fetch course data for course_id: ' . $course_id);
        return null;
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    return (isset($data['ok']) && $data['ok']) ? $data['course'] : null;
}

/**
 * Fetches the user's progress for a specific course.
 *
 * @param string $token The user's access token.
 * @param int $course_id The ID of the course.
 * @return array A list of completed lesson IDs.
 */
function get_user_progress_data($token, $course_id) {
    if (!$token) {
        return [];
    }

    $api_url = LIFECYCLE_API_URL . '/lifecycle/course/' . intval($course_id) . '/progress';
    $response = wp_remote_get($api_url, [
        'headers' => [
            'Cookie' => 'access_token=' . $token
        ],
        'timeout' => 10,
    ]);

    if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
        return [];
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    return (isset($data['ok']) && $data['ok']) ? $data['completed_lessons'] : [];
}

/**
 * Fetches all data for a single lesson page.
 *
 * @param string $token The user's access token.
 * @param int $lesson_id The ID of the lesson.
 * @return array|null The lesson data or null on error.
 */
function get_lesson_data($token, $lesson_id) {
    if (!$token) {
        return null;
    }

    $api_url = LIFECYCLE_API_URL . '/lifecycle/lesson/' . intval($lesson_id);
    $response = wp_remote_get($api_url, [
        'headers' => ['Cookie' => 'access_token=' . $token],
        'timeout' => 10,
    ]);

    if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
        error_log('Failed to fetch lesson data for lesson_id: ' . $lesson_id);
        return null;
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    // For now, we are not fetching next/prev lesson IDs from the backend.
    // This can be added as a future enhancement.
    if (isset($data['ok']) && $data['ok']) {
        $lesson_data = $data['lesson'];
        $lesson_data['prev_lesson_id'] = null; // Placeholder
        $lesson_data['next_lesson_id'] = null; // Placeholder
        return $lesson_data;
    }

    return null;
}
