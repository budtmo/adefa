[![Build Status](https://travis-ci.org/butomo1989/adefa.svg?branch=master)](https://travis-ci.org/butomo1989/adefa)
[![codecov](https://codecov.io/gh/butomo1989/adefa/branch/master/graph/badge.svg)](https://codecov.io/gh/butomo1989/adefa)

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
pip3 install -e git+https://github.com/butomo1989/adefa.git#egg=adefa
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
   export APP_ID=$(adefa upload --name sample.apk --project $PROJECT_ID --type ANDROID_APP --file https://github.com/butomo1989/adefa/blob/master/test-app/sample_apk_debug.apk?raw=true)
   ```

3. Upload test scripts

   ```bash
   export TEST_ID=$(adefa upload --name myTestScript --project $PROJECT_ID --type APPIUM_PYTHON_TEST_PACKAGE --file https://github.com/butomo1989/adefa/blob/master/test-app/appium-python/test_bundle.zip?raw=true)
   ```

4. Create device group

   For example we want to create device group from following devices:
   1. Samsung Galaxy S7 Edge - arn:aws:devicefarm:us-west-2::device:270E0E7C4512409A81CF7F8CE48B814B
   2. HTC One M8 (AT&T) - arn:aws:devicefarm:us-west-2::device:784D54EA42DF4030B669587FC2B5184E
   3. LG Nexus 5 - arn:aws:devicefarm:us-west-2::device:DAFD5E60762748C98D662E0320E3FE66

   ```bash
   export GROUP_ID=$(adefa group --name myDeviceGroup --project $PROJECT_ID --device arn:aws:devicefarm:us-west-2::device:270E0E7C4512409A81CF7F8CE48B814B --device arn:aws:devicefarm:us-west-2::device:784D54EA42DF4030B669587FC2B5184E --device arn:aws:devicefarm:us-west-2::device:DAFD5E60762748C98D662E0320E3FE66)
   ```

5. Run test

   ```bash
   adefa run --name firstRun --project $PROJECT_ID --app $APP_ID --type APPIUM_PYTHON --test $TEST_ID --group $GROUP_ID
   ```

6. Get test result

   //TODO


Unit tests
----------

Run the unit tests with this command:

```bash
nosetests -v
```
