## Install Side Runner

To run the selenium test, install the `selenium-side-runner` at first:

``` 
sudo apt-get install npm
sudo npm install -g selenium-side-runner
```

IF run locally, install the web driver (Chrome and Firefox):

```
sudo npm install -g chromedriver
sudo npm install -g geckodriver
```

Use the following command to run `selenium-side-runner` :

```
selenium-side-runner --server http://ec2-54-162-139-224.compute-1.amazonaws.com:4444/wd/hub -c "browserName='chrome'" cas_chrome.side
```

```
selenium-side-runner --server http://ec2-54-162-139-224.compute-1.amazonaws.com:4444/wd/hub -c "browserName='firefox'" cas.side
```

