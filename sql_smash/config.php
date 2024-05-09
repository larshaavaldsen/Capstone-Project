<?php

/* Attempt to connect to MySQL database */
$link = mysqli_connect(
    'db',
    'php_docker',
    'password',
    'php_docker'
);

// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
