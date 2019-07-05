[![Build Status](https://travis-ci.org/budtmo/adefa.svg?branch=master)](https://travis-ci.org/budtmo/adefa)
[![Build Status](https://dev.azure.com/budtmoos/budtmoos/_apis/build/status/budtmo.adefa?branchName=master)](https://dev.azure.com/budtmoos/budtmoos/_build/latest?definitionId=2&branchName=master)
[![codecov](https://codecov.io/gh/budtmo/adefa/branch/master/graph/badge.svg)](https://codecov.io/gh/budtmo/adefa)

ADEFA
=====

ADEFA stands for AWS Device Farm which is a CLI to help test developer running UI tests on AWS Device Farm.

Requirement
-----------

1. AWS Credentials

   ```bash
   export AWS_ACCESS_KEY_ID=<id>
   export AWS_SECRET_ACCESS_KEY=<secret>
   ```

2. Python 3

Installation
------------

```bash
pip3 install -e git+https://github.com/budtmo/adefa.git#egg=adefa
```

Usage
-----

```bash
adefa -h
```

Quick Start
-----------
1. Create project

   ```bash
   export PROJECT_ID=$(adefa create myFirstProject)
   ```

2. Upload app

   ```bash
   export APP_ID=$(adefa upload --name sample.apk --project $PROJECT_ID --type ANDROID_APP --file https://github.com/budtmo/adefa/blob/master/test-app/sample_apk_debug.apk?raw=true)
   ```

3. Upload test scripts

   ```bash
   export TEST_ID=$(adefa upload --name myTestScript --project $PROJECT_ID --type APPIUM_PYTHON_TEST_PACKAGE --file https://github.com/budtmo/adefa/blob/master/test-app/appium-python/test_scripts_app.zip?raw=true)
   ```

4. Create device group

   For example we want to create device group from following devices:
   - Samsung Galaxy S7 Edge - arn:aws:devicefarm:us-west-2::device:270E0E7C4512409A81CF7F8CE48B814B
   - HTC One M8 (AT&T) - arn:aws:devicefarm:us-west-2::device:784D54EA42DF4030B669587FC2B5184E
   - LG Nexus 5 - arn:aws:devicefarm:us-west-2::device:DAFD5E60762748C98D662E0320E3FE66

   ```bash
   export GROUP_ID=$(adefa group --name myDeviceGroup --project $PROJECT_ID --device arn:aws:devicefarm:us-west-2::device:270E0E7C4512409A81CF7F8CE48B814B --device arn:aws:devicefarm:us-west-2::device:784D54EA42DF4030B669587FC2B5184E --device arn:aws:devicefarm:us-west-2::device:DAFD5E60762748C98D662E0320E3FE66)
   ```

5. Run test

   ```bash
   export RUN_ID=$(adefa run --name firstRun --project $PROJECT_ID --app $APP_ID --type APPIUM_PYTHON --test $TEST_ID --group $GROUP_ID)
   ```

6. Get test result

   ```bash
   adefa result $RUN_ID --total-attempts 15 --delay 30 --json-output
   ```

Unit tests
----------

Run the unit tests with this command:

```bash
nosetests -v
```
