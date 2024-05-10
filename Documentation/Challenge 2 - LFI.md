## Machines on network:

172\.28.1.3 - **Target webserver**

172\.28.1.5 - **Kali Linux container**

## Overview of Challenge:

**LFI**, or local file inclusion is a common vulnerability where sensitive local files are unintentionally leaked through abusing the functionality of a web application. In this challenge we will use an LFI vulnerability to find the logic for creating cookies on a web application, and use it to get past a login page. 

Walkthrough:


## 1) Reconnaissance
Firstly, let's go to the website. We are greeted with the index.html page with a login form, and a link to the help center. Upon closer inspection of the form by viewing the source code in the browser (right click, view page source), we can see that the input from the form is sent to the login.php file. Let's remember this and check out the help center.
 
In the help center, we see three links, each to a different page in the help center. If we click the first one, we see that "admin" is the default username. This could be useful for the future so we will remember this. 

If we inspect the url of the login help page -

```
http://172.28.1.3/helpdisplay.php?help=login.txt
```


We can see the url is passing the variable named ‘help’ to the page, and the value of that variable is ‘login.txt’. We can interpret this to be the website displaying the contents of a file called ‘login.txt’. Maybe there is some way we could display other files that could help us hack this website?

## 2) Exploiting the LFI and Setting the cookie
 If we swap ‘login.txt’ for ‘login.php’ (the page we determined to be handling the logins earlier), we get some funky output, but if we view the source of the page, we see:

```php
<?php
include 'secure/passcheck.php';
$uname = htmlspecialchars($_GET["uname"]);
$passwd = htmlspecialchars($_GET["passwd"]);
if($uname == 'admin' & passcheck($passwd)) {
    $cookie_name = 'user';
    $cookie_value = base64_encode($uname);
    setcookie($cookie_name, $cookie_value, time() + (86400 * 30), "/"); // 86400 = 1 day
    print('Logged in. <a href="home.php">Click Here</a>');
}
// I've just base64 encoded the username for the cookie, no one will see this anyways so it shouldn't matter ¯\_(ツ)_/¯
else{
    header('Location: ' . $_SERVER['HTTP_REFERER']);
}
```
It seems that whatever lazy developer made this website only decided to use the username encoded as base64 to manage logins. Also note that this page, once properly logged in links 172\.28.1.3 to a page known as home.php. If we look at that page we can see that we don’t have access to it. So let's set a cookie with the name ‘user’, and the value as ‘admin’ base64 encoded (YWRtaW4=) using the inspect element storage tool in Firefox. After we set the cookie, if we try and access the home.php page, we can see that we have completed the challenge. Good work!

### Extra challenge
There are a few other ways to exploit this webapp that I have not outlined in this walkthrough. Take a look at the code again and see if you can get the admin password!