# About

Container for adding/tracking challenges in our environment. When deploying with our docker compose, be sure to mount /usr/src/app to a volume to ensure persistence of challenge completion statuses

# Adding challenges -

You can use this template for adding challenges into db.json -

```
    {
      "name": "challenge_endpoint",
      "points": 100,
      "completed": false
    }
```

The endpoint name is everything found after the /, i.e. http://container-ip/{NAME}

# NOTE - do not push to repo with challenges set to true in db.json please:)
