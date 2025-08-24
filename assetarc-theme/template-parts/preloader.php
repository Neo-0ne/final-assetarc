<?php
// preloader.php - Optional loading screen
?>
<style>
#preloader {
    position: fixed;
    left: 0; top: 0;
    width: 100%; height: 100%;
    background: black;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.loader {
    border: 4px solid #FFD700;
    border-top: 4px solid transparent;
    border-radius: 50%;
    width: 40px; height: 40px;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
<div id="preloader">
    <div class="loader"></div>
</div>
<script>
    window.addEventListener('load', function () {
        document.getElementById('preloader').style.display = 'none';
    });
</script>
