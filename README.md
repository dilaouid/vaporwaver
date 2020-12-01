# vaporwaver
Create your own vaporwaved profil picture with this PHP script ! *Made without framework, or any third party library.*
You can test it live here: [Vaporwaver](https://vaporwaver.dilaouid.xyz "dilaouid.xyz")
![preview](https://i.ibb.co/WD8bjQq/presentation.png)

## How to use
**This script can be deployed online and offline !**
First, make sure you have PHP installed in your machine.
Clone this repo in your '*www*' folder of wamp or '*htdocs*' in xampp. Then access to the project by navigating through `localhost/vaporwaver`.

## How does it works
The script takes an image, with or without transparency (though, please use an image with transparency for a better result!), and with many overlapping, with effects, noises, and background, and a glitch effects, give you a special vaporwaved picture like this! (The picture will have a size of 600x600)

![preview](https://i.ibb.co/2qcmBGw/before-after.png)

You can add a background or a filter though the folders `src/res/bg` and `src/res/filters`. **Remember it should have a size of, at least, 600x600 !**
The noise isn't a stock picture, it's a picture created in PHP.

It uses a latin -> hiragana / katakana convertor. If you know some kanjis, you can complete the dictionary in `src/lang.php`. Feel free to ask for a PR anytime !
You can change the used font in the constructor of the Vaporwaver Class (`src/Class/Vaporwaver.php`).

## TODO
+ A completly independant Vaporwaver Class, so you could use it in your own PHP project without any kind of adaptations !
+ Place the imported image right in the center (according to the size, it goes somewhere else atm)
+ Some debugging

## Contribution
The backgrounds from this repo are made by the very talented artists [aestheticshi7](https://www.instagram.com/aestheticshi7 "instagram") and [Maxime DES TOUCHES](https://www.behance.net/elreviae/ "behance"). Please go take a look at their great artworks !
