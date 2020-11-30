<?php

header('Content-Type: application/json');

require ('Class/Vaporwaver.php');
require ('func.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $post   = $_POST;
    $checkEntries = checkEntries($post);
    if ($checkEntries !== true) printerror(json_encode($checkEntries));
    $post['img'] = base64_decode($post['img']);
    $post['txt'] = htmlspecialchars($post['txt']);
    $vwaver = new  \Vaporwaver($post);
    $vwaver->Create();
    print_r(json_encode($vwaver->res));
}