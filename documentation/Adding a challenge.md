# Adding a challenge 

## Step 1 - adding container to docker compose

All files needed for building your challenge container should be stored in a directory in the root of the repository, i.e. the lfi-challenge folder contains all code and the necessary docker file. After putting your container files into the repository, you can add it to the docker compose.

```
lfi-challenge:
    build: ./lfi-challenge
    networks:
      webnet:
        ipv4_address: 172.28.1.3
        aliases:
          - lfi-challenge
```

Make sure you assign the container a static IP that isn't already taken, and include any volumes/configuration that isn't in the dockerfile.

## Step 2 - adding the webhook endpoint

All endpoints are stored in [db.json](../Webhook%20Container/db.json). To add an endpoint just follow this template:

```
    {
      "name": "challenge_endpoint",
      "points": 100,
      "completed": false
    }
```

Be sure to set completed to false, and don't push with any challenges set to true.

## Step 3 - integrate the webhook, so the challenge can be completed

How to integrate this step will depend on the challenge. All that needs to happen for a challenge to be "completed" is the webhook endpoint being requested via http. The endpoint will follow this format (including the static IP) - http://172.28.1.6:3000/{endpoint name}

In the LFI challenge, this is integrated as follows - 
[home.php](../lfi-challenge/webapp/home.php)

```
<?php
include 'secure/cookiecheck.php';
if (checkKook()){
    print('Congratulations, you have compromised this site. Good work!');
    get_headers("http://172.28.1.6:3000/lfi-challenge");
}
else{
    $bruh = "(ง'̀-'́)ง";
    print('<h1> You do not have access to this page! BEGONE!! ');
    print($bruh);
}
?>
```

Assuming the challenge is complete, and the checkKook function returns true, the webapp will query the endpoint. In this case the request is done on the backend using the get_headers() function (It literally does not matter what function you use it just needs to send the http request to the server). If it isn't technically feasible to have the backend send the http request, we can also provide the user with a link to the endpoint that they can click to trigger the challenge completion.