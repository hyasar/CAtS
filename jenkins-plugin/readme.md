# Jenkins-plug-in

The Jenkins plug-in can get the Sonarqube report and upload the report to the configured CAtS service.

## How to use?

You can refer to https://wiki.jenkins.io/display/JENKINS/Plugin+tutorial.

### Setting up environment

It may be helpful to add the following to your `~/.m2/settings.xml` (Windows users will find them in `%USERPROFILE%\.m2\settings.xml`):

```xml
<settings>
  <pluginGroups>
    <pluginGroup>org.jenkins-ci.tools</pluginGroup>
  </pluginGroups>
 
  <profiles>
    <!-- Give access to Jenkins plugins -->
    <profile>
      <id>jenkins</id>
      <activation>
        <activeByDefault>true</activeByDefault> <!-- change this to false, if you don't like to have it on per default -->
      </activation>
      <repositories>
        <repository>
          <id>repo.jenkins-ci.org</id>
          <url>https://repo.jenkins-ci.org/public/</url>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>repo.jenkins-ci.org</id>
          <url>https://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
      </pluginRepositories>
    </profile>
  </profiles>
  <mirrors>
    <mirror>
      <id>repo.jenkins-ci.org</id>
      <url>https://repo.jenkins-ci.org/public/</url>
      <mirrorOf>m.g.o-public</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

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

Select the generated plugin.