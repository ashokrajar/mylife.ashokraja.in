---
title: "Multi Stage Azure Pipeline for Golang"
date: 2020-04-29T00:38:15+04:00
categories:
  - DevOps
  - CI/CD
  - Azure DevOps
tags:
  - Azure Devops
  - DevOps
  - Goland
  - Azure Pipeline
  - Azure Pipeline Template
  - CI/CD Pipeline
keywords:
  - Azure
  - DevOps
  - Azure Devops
  - Goland
  - Azure Pipeline
  - Azure Pipeline Template
  - CI/CD Pipeline
thumbnailImage: "/img/thumbs/azure-multistage.png"
---

I have been playing around with Azure DevOps as part of my experiment with various CI/CD tools. I will be sharing my views and comparison of various CI/CD tools in a separate post.
<!--more-->
For now lets focus on how we can create a templatized Multi Staged Azure Pipeline.

> GitHub Repo : [https://github.com/ashokrajar/mylabs-go](https://github.com/ashokrajar/mylabs-go)
> 	
> Multi Stage Azure Pipeline Demo : [https://dev.azure.com/ashokrajar/testpad](https://dev.azure.com/ashokrajar/testpad)


We will be building a simple Golang cli application for demo purpose.

```bash
shell # ./mylabs-go
Hello Home !!
shell # ./mylabs-go version
0.2.1
shell #
```

Let’s demonstrate how we do Build => Test => Deploy(In our case it willbe Release Binary Artifact) using Azure Multi Stage build.

What all Tests will we be running ?

* Unit Tests
* Code Coverage
* Vulnerability Test (we will be using ShiftLeft)

All these tests will be executed in parallel for multiple versions of Golang.

# Our GOAL

Create a dynamically configurable Azure Pipeline for Golang application for multiple platforms.

> Multi Stage Azure Pipeline Demo : [https://dev.azure.com/ashokrajar/testpad](https://dev.azure.com/ashokrajar/testpad)

### A Multi Stage build which looks like this

![](/img/build-stage-01.png)

![Pipeline View](/img/build-stage-02.png)

### Embedded Test Results
![](/img/embed-test-result01.png)

### Embedded Code Coverage Results
![](/img/embed-code-cover01.png)

### Embedded Vulnerability Scan Reports
![](/img/vulnerability-result01.png)

> Alright enough showing off let’s get our hands dirty.

# Design/Create a Azure Pipeline to achieve our GOAL
### Step 1 : Create folders/files hierarchy
For creating reusable template we need a proper **folders/files hierarchy design**.

![](/img/folder-hierarchy.png)

### Step 2 : Create azure-pipeline.yml
We have designed a pipeline config which will **trigger the builds** for commits to **master, dev & release**/* branches and also or **pull request to master** branch. At the same time it will build will **not be triggered** for changes to non-project files.

```yaml
trigger:
  batch: true  # Ensure batch execution for very active repos
  branches:
    include:
      - master
      - dev
      - release/*
  paths:
    exclude:
      - README.md
      - .gitignore

pr:
  autoCancel: True  # Auto cancel if active pull request updated
  branches:
    include:
      - master
  paths:
    exclude:
        ..... removed for brevity .....
variables:
  GOPATH: '$(Pipeline.Workspace)/gowork'

stages:
# We will be building stages in following steps
```

Before we start creating multiple stages lets create some reusable templates.

### Step 3 : Creating Shared Templates
Azure provides a powerful templating functionality which let you define reusable content, logic, and parameter.

**Template : templates/azure/steps/setupgo.yml**

```yaml
parameters:
  goVersion: '1.14'

steps:
  - task: GoTool@0
    displayName: 'Use Go ${{ parameters.goVersion }}'
    inputs:
      version: ${{ parameters.goVersion }}

  - script: |
      set -e -x
      mkdir -p '$(GOPATH)/bin'
      echo '##vso[task.prependpath]$(GOROOT)/bin'
      echo '##vso[task.prependpath]$(GOPATH)/bin'
    displayName: 'Create Go Workspace'
```

This will setup the Golang workspace with the default version of 1.14. Which can be overridden when calling the template from the pipeline config files.

**Template : templates/azure/steps/buildapp.yml**

```yaml
steps:
  - task: Go@0
    displayName: 'Build Application Binary'
    inputs:
      command: 'build'
      workingDirectory: '$(System.DefaultWorkingDirectory)'
      arguments: '-o $(Build.BinariesDirectory)/mylabs-go'
```

Similarly this template helps build the Golang application.

**Template : templates/azure/jobs/build.yml**

```yaml
parameters:
  name: ''
  pool: ''

jobs:
  - job: ${{ parameters.name }}
    pool: ${{ parameters.pool }}
    steps:
      - template: ../steps/setupgo.yml

      - template: ../steps/buildapp.yml
```

This template will help executing of the build stage of the the Golang application.

But Wait ! What ? More templates inherited inside the template ? YES!, we are just make using the templates we designed in the previous steps

**Template : templates/azure/jobs/test.yml**

```yaml
jobs:
  - job: RunTests
    strategy:
      matrix:
        GoVersion_1_13:
          go.version: '1.13'
        GoVersion_1_14:
          go.version: '1.14'

    pool:
      vmImage: 'ubuntu-18.04'

    steps:
      - template: ../steps/setupgo.yml
        parameters:
          goVersion: '$(go.version)'

      - script: |
          set -e -x
          go version
          go get -u github.com/jstemmer/go-junit-report
          go get github.com/axw/gocov/gocov
          go get github.com/AlekSi/gocov-xml

          curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.24.0
          curl https://cdn.shiftleft.io/download/sl > $(go env GOPATH)/bin/sl && chmod a+rx $(go env GOPATH)/bin/sl
        displayName: 'Install Dependencies'

      - script: |
          set -e -x
          golangci-lint run
        displayName: 'Run Code Quality Checks'

      - script: |
          set -e -x
          go test -v -coverprofile=coverage.txt -covermode count ./... > test_results.txt
          go-junit-report < test_results.txt > report.xml
        displayName: 'Run Unit Tests'

      - task: PublishTestResults@2
        displayName: 'Publish Test Results'
        inputs:
          testRunner: JUnit
          testResultsFiles: $(System.DefaultWorkingDirectory)/**/report.xml

      - script: |
          set -e -x
          gocov convert coverage.txt > coverage.json
          gocov-xml < coverage.json > coverage.xml
        displayName: 'Run Code Coverage Tests'

      - task: PublishCodeCoverageResults@1
        displayName: 'Publish Code Coverage'
        inputs:
          codeCoverageTool: Cobertura
          summaryFileLocation: $(System.DefaultWorkingDirectory)/**/coverage.xml

      - script: |
          curl https://cdn.shiftleft.io/download/sl > $BUILD_SOURCESDIRECTORY/sl && chmod a+rx $BUILD_SOURCESDIRECTORY/sl
          $BUILD_SOURCESDIRECTORY/sl analyze --wait --tag branch=$BUILD_SOURCEBRANCHNAME --tag app.group=MyLabs --tag app.language=go --app MyLabs-G0 --cpg --go ./...
        displayName: 'Run Vulnerability Checks'
        env:
          SHIFTLEFT_ORG_ID: $(SHIFTLEFT_ORG_ID)
          SHIFTLEFT_ACCESS_TOKEN: $(SHIFTLEFT_ACCESS_TOKEN)

      - script: |
          set -e -x
          docker run \
          -v "$(Build.SourcesDirectory):/app:cached" \
          -v "$(Build.ArtifactStagingDirectory):/reports:cached" \
          shiftleft/sast-scan scan --src /app \
          --out_dir /reports/CodeAnalysisLogs
        displayName: "Perform Vulnerability Scan"
        continueOnError: "true"

      - task: PublishBuildArtifacts@1
        displayName: "Publish Vulnerability Scan Results"
        inputs:
          PathtoPublish: "$(Build.ArtifactStagingDirectory)/CodeAnalysisLogs"
          ArtifactName: "CodeAnalysisLogs"
          publishLocation: "Container"
```

This template will perform these actions,

* Setup Golang
* Install Dependencies
* Run Code Quality Checks
* Run Unit Tests
* Publish Test Results into Pipeline
* Publish Coverage Results into Pipeline
* Run ShiftLeft Inspect/anAlyse Vulnerability Scan
* Run ShiftLeft SAST Vulnerability Scan
* Publish ShiftLeft SAST Vulnerability Scan Results into Pipeline

Testing on multiple versions.

```yaml
strategy:
      matrix:
        GoVersion_1_13:
          go.version: '1.13'
        GoVersion_1_14:
          go.version: '1.14'
```

Also note the strategy we have defined, if you want to support wider version of Golang just add more version, here it’s that simple.

**Template : templates/azure/jobs/release.yml**

```yaml
parameters:
  name: ''
  pool: ''

jobs:
  - job: ${{ parameters.name }}
    pool: ${{ parameters.pool }}
    steps:
      - template: ../steps/setupgo.yml

      - template: ../steps/buildapp.yml

      - task: CopyFiles@2
        displayName: 'Copy binary files to Artifact Stage Directory'
        inputs:
          sourceFolder: $(Build.BinariesDirectory)
          targetFolder: $(Build.ArtifactStagingDirectory)

      - task: PublishBuildArtifacts@1
        displayName: 'Publish Build Artifacts'
        inputs:
          artifactName: $(Agent.OS)

      - task: Bash@3
        displayName: 'Get/Set Application/Package Version'
        inputs:
          targetType: 'inline'
          script: |
            set -e -x
            version=`./mylabs-go version`
            echo "##vso[task.setvariable variable=MYLABSCLI_VERSION;]$version"
          workingDirectory: $(Build.BinariesDirectory)
        condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/master'))

      - task: Bash@3
        displayName: 'Get/Set OS Specific Package Feed Name'
        inputs:
          targetType: 'inline'
          script: |
            set -e -x
            OS_NAME=`echo "$(Agent.OS)" | tr "[:upper:]" "[:lower:]"`
            echo "##vso[task.setvariable variable=FEED_NAME;]$OS_NAME"
          workingDirectory: $(Build.BinariesDirectory)
        condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/master'))

      - task: UniversalPackages@0
        displayName: 'Publish Release Artifacts'
        inputs:
          command: 'publish'
          publishDirectory: '$(Build.ArtifactStagingDirectory)'
          feedsToUsePublish: 'internal'
          vstsFeedPublish: '1354bdaa-1b77-41d3-a573-e85080e85d85/90f9f1a3-3b7f-4814-aea6-f06d7842d9af'
          vstsFeedPackagePublish: $(FEED_NAME)
          versionOption: 'custom'
          versionPublish: $(MYLABSCLI_VERSION)
        condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/master'))
```

This template will do these actions,

* Setup Golang
* Build and produce Golang application binary artifact
* Set environment variable for OS specific Azure Artifact Universal Package Feed
* Get/Set Application version to be published in the Azure Artifact Universal Package Feed
* Push the application binary into Azure Artifact Universal Package

Alright now we have created a reusable build template how do we use this in the pipeline ?

### Step 4 : Create Build Stage

**azure-pipeline.yml**

```yaml
stages:
  - stage: Build
    jobs:
      - template: templates/azure/jobs/build.yml   # Linux Build
        parameters:
          name: 'Linux_Build'
          pool:
            vmImage: 'ubuntu-18.04'
      - template: templates/azure/jobs/build.yml   # macOS Build
        parameters:
          name: 'Mac_Build'
          pool:
            vmImage: 'macos-10.14'
```

Now you can see how the parmeterized template helped us to reuse the sample for different build binary based on the Operating System.

### Step 5 : Create Test Stage

**azure-pipeline.yml**

```yaml
stages:
  ..... removed for brevity .....
  - stage: Test
    jobs:
      - template: templates/azure/jobs/test.yml
```

I don’t have to explain here as it’s self explanatory.

### Final Step : Create Release Stage

**azure-pipeline.yml**

```yaml
stages:
  ..... removed for brevity .....
  - stage: Release
    jobs:
      - template: cicd/jobs/release.yml
        parameters:
          name: 'Linux_Release'
          pool:
            vmImage: 'ubuntu-18.04'
      - template: cicd/jobs/release.yml
        parameters:
          name: 'Mac_Release'
          pool:
            vmImage: 'macos-10.14'
```

This stage will create release for multiple Operating System.