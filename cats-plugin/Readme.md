# Jenkins-plug-in

The Jenkins plug-in can get the Sonarqube report and upload the report to the configured CAtS service.

## How to use?

You can refer to https://wiki.jenkins.io/display/JENKINS/Plugin+tutorial and http://maven.apache.org.

### Setting up environment

#### Maven(For Unix-based OS):

Download binary file http://maven.apache.org/download.cgi

Add path to '~/.profile'

```
source ~/.profile
```
```
  export MAVEN_HOME=/users/$username/apache-maven-$version
  export PATH=${MAVEN_HOME}/bin:$PATH
  export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.0.2.jdk/Contents/Home
```

Run mvn -v check if succeeded

#### Jenkins

Run 'brew cask install homebrew/cask-versions/adoptopenjdk8'

Run 'brew install jenkins'

Run 'brew services start jenkins'

Browse to `http://localhost:8080`


### Create Target

Under the `./cats` directory, run

```
mvn package
```

It shall generate a folder named target.

### Building a Plugin

To build a plugin, run `mvn install`. This will create the file `./target/pluginname.hpi` that you can deploy to Jenkins.

```bash
$ mvn install
```

It shall generate a `.hpi ` under the target folder.


### Install Plugin

In Jenkins, select `manage jenkins` >  `manage plugin`.

Go to `advanced` > `Upload Plugin`.

Select the generated plugin(hpi file).


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
Fill in the `Passphrase` of Jenkins SSH key.
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
```
