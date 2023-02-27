#!/bin/bash


kubectl cp -n jenkins ../jcasc-plugin-config/baseline.yaml jenkins-0:/tmp -c jenkins
