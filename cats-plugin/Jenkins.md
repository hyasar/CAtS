### Jenkins Configuration


#### Credential Generation

In Jenkins, select `Manage Jenkins` > `Configure System`.
Add credentials for different plugins.


#### Install Plugin

In Jenkins, select `Manage Jenkins` > `manage plugin`.

Go to `Available’ > `Install Plugin’

Go to `Installed` > select plugins.


#### Configure Web Service Address

In Jenkins, select `Manage Jenkins` > `Configure System`.

```
SonarQube servers
```

TODO

```
SWAMP
```

SWAMP URL: https://www.mir-swamp.org
Add SWAMP Credential.
Choose default project.

```
Build Timestamp
```

Select `Enable BUILD_TIMESTAMP`

```
SSH remote hosts
```

Hostname: ${AWS public DNS}
Port: 22

```
Jenkins Location
```
Jenkins URL: http://${AWS public DNS}:8080/

```
Git Parameter
````
Select `Show 'need to clone' information`

```
Publish over SSH
```
Fill in the `Passphrase``` of Jenkins SSH key.

```
CAtS Plugin
```
CAS Host URL: ${AWS public DNS}
CAS Port: 8000

```
GitHub Pull Request Builder
```
Go to `GitHub Auth`.
GitHub Server API URL: https://api.github.com
Shared secret: 
Credentials: Select admin credential

Go to `Auto-manage webhooks` and select it.
