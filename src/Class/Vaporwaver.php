<?php

require ('lang.php');

class Vaporwaver {


    private $data;
    private $font;
    public  $res;


    public function __construct($data)
    {
        $this->font = dirname(__FILE__) . "\..\MPLUSRounded1c.ttf";
        $this->data = $data;
        $this->purpleOverlay = \imagecreate(600, 600);
        $colorOverlay = \imagecolorallocate($this->purpleOverlay, 250, 109, 255);
    }

    private function translate($string, $alp)
    {
        for ($i=0; $i < count(LANG); $i++) {
            $string = str_replace(LANG[$i][0], LANG[$i][$alp], $string);
        }
        return $string;
    }

    private function createColorOverlay($r, $g, $b)
    {
        $ov = \imagecreate(600, 600);
        $co = \imagecolorallocate($ov, $r, $g, $b);
        return $ov;
    }

    private function RGBtoHSV($r, $g, $b)
    {
        $r = $r/255;
        $g = $g/255;
        $b = $b/255;
        $cols = array("r" => $r, "g" => $g, "b" => $b);
        asort($cols, SORT_NUMERIC);
        $min = key(array_slice($cols, 1));
        $max = key(array_slice($cols, -1));
        if($cols[$min] == $cols[$max]) {
            $h = 0;
        } else {
            if ($max == "r") {
                $h = 60 * ( 0 + ( ($cols["g"]-$cols["b"]) / ($cols[$max]-$cols[$min]) ) );
            } else if ($max == "g") {
                $h = 60 * ( 2 + ( ($cols["b"]-$cols["r"]) / ($cols[$max]-$cols[$min]) ) );
            } else if ($max == "b") {
                $h = 60 * ( 4 + ( ($cols["r"]-$cols["g"]) / ($cols[$max]-$cols[$min]) ) );
            }
            if ($h < 0) {
                $h += 360;
            }
        }
        if($cols[$max] == 0) {
            $s = 0;
        } else {
            $s = ( ($cols[$max]-$cols[$min])/$cols[$max] );
            $s = $s * 255;
        }
        $v = $cols[$max];
        $v = $v * 255;
        return(array($h, $s, $v));
    }
    
    private function posterizeImg($im, $w = 600, $h = 600, $g, $b)
    {
        for($hi=0; $hi < $h; $hi++) {
            for($wi=0; $wi < $w; $wi++) {
                $rgb = imagecolorat($im, $wi, $hi);
                $r = ($rgb >> 16) & 0xFF;
                $g = ($rgb >> 8) & 0xFF;
                $b = $rgb & 0xFF;
                $hsv = $this->RGBtoHSV($r, $g, $b);
                if($hi < $h-1) {
                    $brgb = imagecolorat($im, $wi, $hi+1);
                    $br = ($brgb >> 16) & 0xFF;
                    $bg = ($brgb >> 8) & 0xFF;
                    $bb = $brgb & 0xFF;
                    $bhsv = $this->RGBtoHSV($br, $bg, $bb);
                    if($bhsv[2]-$hsv[2] > 20) {
                        for($i=-2;$i<1;$i++)
                            imagesetpixel($im, $wi + $i, $hi, imagecolorallocate($im, 0, $g, $b));
                    } else {
                        imagesetpixel($im, $wi, $hi, imagecolorallocate($im, 255, 255, 255));
                    }
                }
            }
        }
    }

    private function imagecopymerge_alpha($dst_im, $src_im, $dst_x, $dst_y, $src_x, $src_y, $src_w, $src_h, $pct)
    {
        $cut = imagecreatetruecolor($src_w, $src_h);
        imagecopy($cut, $dst_im, 0, 0, $dst_x, $dst_y, $src_w, $src_h);
        imagecopy($cut, $src_im, 0, 0, $src_x, $src_y, $src_w, $src_h);
        imagecopymerge($dst_im, $cut, $dst_x, $dst_y, 0, 0, $src_w, $src_h, $pct);
    }

    private function createNoiseImg()
    {
        $x = 600;
        $y = 600;
        $im = imagecreatetruecolor($x,$y);
        for($i = 0; $i < $x; $i++) {
            for($j = 0; $j < $y; $j++) {
                $color = imagecolorallocate($im, rand(0,255), rand(0,255), rand(0,255));
                imagesetpixel($im, $i, $j, $color);
            }
        }    
        imagefilter($im, IMG_FILTER_GRAYSCALE);
        return ($im);
    }

    private function cropCharacter(&$character)
    {
        $character = imagescale($character, 700);
        $character = imagecrop($character, ['x' => 0, 'y' => 0, 'width' => 600, 'height' => 600]);
    }

    private function glitch(&$character, &$dest)
    {
        $colorChoice = rand(0, 1);
        if ($colorChoice == 0) $this->posterizeImg($character, 600, 600, 255, 0);
        else $this->posterizeImg($character, 600, 600, 0, 255);
        $moved_picture = \imagecreatetruecolor(600, 600);
        \imagecopy($moved_picture, $character, rand(-3, -5), 0, 0, 0, 600, 600);
        $white = imagecolorallocate($moved_picture, 255, 255, 255);
        imagecolortransparent($moved_picture, $white);
        $this->fuseimage($moved_picture, $dest, 60);
    }

    private function fuseimage($source, $dest, $opacity = 100)
    {
        $this->imagecopymerge_alpha($dest, $source, 0, 0, 0, 0, 600, 600, $opacity);
    }

    private function applyEffect(&$im, $effect, $pct)
    {
        imagecopymerge($im, $effect, 0, 0, 0, 0, 600, 600, $pct);
    }

    private function hextorgb($hex)
    {
        if( preg_match( "~^#?[abcdef0-9]{3}$~ui", $hex )) {
            $hex = trim( $hex, "#" );
            list( $hexR, $hexG, $hexB ) = str_split( $hex );
            $hexR .= $hexR;
            $hexG .= $hexG;
            $hexB .= $hexB;
        } else {
            $hex = trim( $hex, "#" );
            list( $hexR, $hexG, $hexB ) = str_split( $hex, 2 );
        }
        $rgb = [hexdec($hexR), hexdec($hexG), hexdec($hexB)];
        return $rgb;
    }

    function randompic($dir)
    {
        $files  = glob($dir . '/*.*');
        $file   = array_rand($files);
        return $files[$file];
    }

    private function createTxt()
    {
        putenv('GDFONTPATH=' . realpath('.'));
        if ($this->data['format'] == 'latin') $txt = $this->data['text'];
        elseif($this->data['format'] == 'hiragana') $txt = $this->translate($this->data['text'], 1);
        elseif($this->data['format'] == 'katakana') $txt = $this->translate($this->data['text'], 2);
        $this->data['color'] = trim(str_replace('#', '', $this->data['color']));
        $color = '#' . $this->data['color'];
        $fontsize = $this->data['font'];
        $im = \imagecreatetruecolor(600, 600);
        imagesavealpha($im, true);
        imagealphablending($im, false);
        $white = imagecolorallocatealpha($im, 255, 255, 255, 127);
        imagefill($im, 0, 0, $white);
        $rgb = $this->hextorgb($color);
        $txtcolor = imagecolorallocate($im, $rgb[0], $rgb[1], $rgb[2]);
        $pos = $this->data['position'];

        $bound = imageftbbox($fontsize, 0, $this->font, $txt);

        $text_width =  $bound[2] - $bound[0];
        $text_height = $bound[3] - $bound[5];
        
        $posparts = explode('-', $pos);
        if ($posparts[0]        == 'top')       { $h = $text_height + 20; }
        elseif ($posparts[0]    == 'middle')    { $h = (600 - $text_height) / 2; }
        elseif ($posparts[0]    == 'bottom')    { $h = (600 - $text_height); }

        if ($posparts[1]        == 'left')      { $w = 20; }
        elseif ($posparts[1]    == 'center')    { $w = (600 - $text_width) / 2; }
        elseif ($posparts[1]    == 'right')     { $w = (600 - $text_width) - 20; }

        imagettftext($im, $fontsize, 0, $w, $h, $txtcolor, $this->font, $txt);
        return $im;
    }

    public function Create()
    {
        $output                 = \imagecreatetruecolor(600, 600);
        $character_background   = \imagecreatetruecolor(600, 600);
        $character              = \imagecreatefromstring($this->data['img']);
        $background             = \imagecreatefromjpeg( $this->randompic("./res/bg/") );
        $effect                 = \imagecreatefromjpeg( $this->randompic("./res/filters/") );
        $overlay                = $this->createColorOverlay(rand(200, 250), rand(80, 110), rand(230, 255));
        $noise                  = $this->createNoiseImg();

        $this->cropCharacter($character);
        $this->fuseimage($character, $background);
        imagecopy($character_background, $background, 0, 0, 0, 0, 600, 600);
        $glitchCharacter = $character;
        $this->glitch($glitchCharacter, $character_background);
        imagelayereffect($character_background, IMG_EFFECT_OVERLAY);
        $this->applyEffect($character_background, $noise, 35);
        $this->applyEffect($character_background, $overlay, 60);
        $this->applyEffect($character_background, $effect, 60);

        $txt = $this->createTxt();
        imagelayereffect($character_background, IMG_EFFECT_NORMAL);
        $this->imagecopymerge_alpha($character_background, $txt, 0, 0, 0, 0, 600, 600, 100);

        ob_start();

        imagejpeg($character_background);

        $data = ob_get_contents();
        ob_end_clean();

        imagedestroy($background);
        imagedestroy($glitchCharacter);
        imagedestroy($character_background);
        $this->res = array("success" => 1, "base64" => 'data:image/jpeg;base64,' . base64_encode($data));
    }
}