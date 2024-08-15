<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [AWS HPCWatch](#aws-hpcwatch)
    - [Requirements](#requirements)
    - [Examples](#examples)
    - [Recommended](#recommended)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# AWS HPCWatch #

To work with the example applications in this repository, first ensure that you've installed and configured the requirements listed below. Then follow the instructions in the README files in the application/language subdirectories.

### Requirements ##

* An AWS account
* The AWS Command Line Interface (AWS CLI)
* Docker
* SAM Local
* An Amazon S3 bucket
* (Optional) Maven

To install the AWS CLI, follow the instructions at [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).

To install Docker and SAM Local, follow the instructions at [Requirements for Using SAM Local](http://docs.aws.amazon.com/lambda/latest/dg/test-sam-local.html#sam-cli-requirements).

To create an Amazon S3 bucket, follow the instructions at [Create a Bucket](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html).

To run the Java examples, you'll need to install Maven. For more information, see [Creating a .jar Deployment Package Using Maven without any IDE (Java) ](http://docs.aws.amazon.com/lambda/latest/dg/java-create-jar-pkg-maven-no-ide.html).

### Examples

- [./samples_1](./samples_1) - split examples from https://github.com/awslabs/aws-sam-local/tree/develop/samples
- [./samples_2](./samples_2) - split examples from https://github.com/awslabs/serverless-application-model/tree/develop/examples/apps
- [./samples_3](./samples_3) - split examples from https://github.com/awslabs/serverless-application-model/tree/develop/examples/2016-10-31

### Recommended ##

* [Postman](https://www.getpostman.com/)

You can use Postman to test API Gateway.
test