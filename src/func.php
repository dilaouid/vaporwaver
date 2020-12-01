<?php

require ('constant.php');

function array_keys_exists(array $keys, array $arr)
{
    return !array_diff_key(array_flip($keys), $arr);
}

function printerror($msg)
{
    print_r($msg);
    exit();
}

function checkBase64($file)
{
    $data   = base64_decode($file);
    $f      = finfo_open();
    $mime   = finfo_buffer($f, $data, FILEINFO_MIME_TYPE);
    $type   = explode('/', $mime)[0];
    if ($type !== 'image') return false;
    return true;
}

function checkEntries($post)
{
    if (!array_keys_exists(["text", "overlay", "img", "font", "color", "position", "format"], $post)) return INCOMPLETE_KEYS;
    $colorparse = trim(str_replace('#', '', $post['color']));
    $ex = explode('-', $post['position']);
    if (!in_array($post['overlay'], ['purple', 'green', 'blue'])) return INCORRECT_OVERLAY;
    if (count($ex) != 2 || !in_array($ex[0], ['top', 'middle', 'bottom']) || !in_array($ex[1], ['right', 'center', 'left'])) return INCORRECT_POSITION;
    if (empty($colorparse) || strlen($colorparse) < 5) return INCORRECT_COLOR;
    if (!is_numeric($post["font"])) return NUMERIC_FONT;
    if (!in_array($post['format'], ["latin", "hiragana", "katakana"])) return INCORRECT_FORMAT;
    if ($post["font"] < 10 || $post["font"] > 100) return FONT_SIZE_INCORRECT;
    if (checkBase64($post['img']) === false) return INCORRECT_IMAGE;
    return true;
}