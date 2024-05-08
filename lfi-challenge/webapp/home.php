<?php
include 'secure/cookiecheck.php';
if (checkKook()){
    print('Congratulations, you have compromised this site. Good work!');
    get_headers("http://172.28.1.2/LFI-Challenge");
}
else{
    $bruh = "(ง'̀-'́)ง";
    print('<h1> You do not have access to this page! BEGONE!! ');
    print($bruh);
}