# remote_syslog2
Dockerfile for papertrail/remote_syslog2

This repo has a dodo.py file for providing login, build, publish commands.

src: https://pydoit.org/

`pip3 install doit` will install the required python3 commandline tool.

## doit list

This command is a built-in with doit and will list every task in the dodo.py
file.  Currently that is everything that is everything listed below.

## doit login

Running this command will login to the AWS ECR Docker repository.  This
presumes that you have the correct credentials in the current shell env.

## doit build

This will invoke a Docker build and tag the image with the appropriate
value.  This defaults to `v0.20` which has been the current value since
2017.  Running `docker images` afterward should show the built|tagged
image.

## doit publish

This is the man point of this automation, to be able to push a Docker
image to the AWS ECR repository.  Keep in mind, there are ECR repositories
per AWS account, so this will push to the account that you have
credentials for in your shell environment.
