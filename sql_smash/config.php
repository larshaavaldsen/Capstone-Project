<?php

/* Attempt to connect to MySQL database */
$link = mysqli_connect(
    '172.28.1.8',
    'php_docker',
    'password',
    'php_docker'
);

// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
