### Manual tests 

These are manual tests I run to quickly test and code up stuff.

At some point I will fix these to do the following:

1. Auto generate the ts_api.py from swagger doc
2. Write parallelizable Integration test with provision for auto clean up after every test.
3. ~~Integrate with behave and move away from writing even python code.~~ DONE

and all the goodness.

~~But at this point, I feel python is as easy to write for me as writing Gherkin.~~

~~Above all this is my experiment.~~

Moved some scripts to gherkin using behave. adds little. i might change my mind later. 

### How to run feature:

```
behave --junit -Dtarget="https://nebula-anilcxsamltest.thoughtspotdev.cloud" -Dsecret='<>' -Dpasswd='<>' 
features/token_auth_orgs.feature
```

### How to run normal python:

most scripts are run like this:

```
python3 "http://$host:8080" <params>
```
eg:
```
python3 "http://$host:8080" 'tsadmin' 'admin'
```
