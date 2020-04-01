#!/usr/bin/env python3

import os
import json

from doit.tools import LongRunning
from subprocess import check_output, CalledProcessError

DIR = os.path.abspath(os.path.dirname(__file__))
CWD = os.path.abspath(os.getcwd())
REL = os.path.relpath(DIR, CWD)

DOIT_CONFIG = {
    'default_tasks': ['test'],
    'verbosity': 2,
}

def call(cmd, **kwargs):
    try:
        result = check_output(cmd, shell=kwargs.pop('shell', True), **kwargs).decode('utf-8').strip()
    except CalledProcessError as cpe:
        raise cpe
    return result

def account():
    cmd = 'aws sts get-caller-identity'
    result = call(cmd)
    obj = json.loads(result)
    return obj['Account']

REGION = os.environ.get('REGION', 'us-west-2')
REPONAME = os.environ.get('REPONAME', 'remote_syslog2')
REPOURL = f'{account()}.dkr.ecr.{REGION}.amazonaws.com/{REPONAME}'
REMOTE_SYSLOG2_VERSION = os.environ.get('REMOTE_SYSLOG2_VERSION', 'v0.20')

def envs(sep=' ', **kwargs):
    envs = dict(
        REMOTE_SYSLOG2_VERSION=REMOTE_SYSLOG2_VERSION
    )
    return sep.join(
        [f'{key}={value}' for key, value in sorted(dict(envs, **kwargs).items())]
    )

def task_build():
    cmd = f'env {envs()} docker build . -t {REPOURL}:{REMOTE_SYSLOG2_VERSION}'
    return {
        'actions': [
            cmd,
        ],
    }

def task_login():
    cmd = f'aws ecr get-login-password --region {REGION} | docker login --username AWS --password-stdin {REPOURL}'
    return {
        'actions': [
            cmd,
        ],
    }

def task_publish():
    cmd = f'docker push {REPOURL}:{REMOTE_SYSLOG2_VERSION}'
    return {
        'task_dep': [
            'login',
        ],
        'actions': [
            cmd,
        ],
    }
