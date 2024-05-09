<?php
    include("config.php");
?>
<!DOCTYPE html>
<lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SQL Smash</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div id="form">
            <h1>Sign In</h1>
            <form name="form" action="login.php" onsubmit="return isvalid()" method="POST">
                <label>Username: </label>
                <input type="text" id="user" name="user"><br><br>
                <label>Password: </label>
                <input type="password" id="pass" name="pass"><br><br>
                <input type="submit" id="btn" value="Login" name="submit">
            </form>
        </div>
        <script>
            function isvalid() {
                var user = document.form.user.value;
                var pass = document.form.pass.value;
                if(user.length == "" && pass.length == "") {
                    alert("Please enter a username and password.")
                    return false
                }
                else {
                    if(user.length == "") {
                        alert("Please enter a username.");
                        return false
                    }
                    if(pass.length == "") {
                        alert("Please enter a password.")
                        return false
                    }
                }
            }
        </script>
    </body>
</html>