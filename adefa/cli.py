import boto3

import click

# Device Farm is available only in us-west-2 region for now.
client = boto3.client('devicefarm', 'us-west-2')


def print_api_response(res: list):
    """
    Print API response to console.
    :param res: API response
    """
    try:
        if type(res) == str:
            raise TypeError('Invalid type')

        p = 1
        print('------------------------------------')
        for i in res:
            print('nr: {pos}'.format(pos=p))
            print_item(i)
            print('------------------------------------')
            p += 1
    except TypeError:
        raise


def print_item(item: dict):
    """
    Print Item to console.
    :param item: item
    """
    try:
        for k, v in sorted(item.items()):
            print('{key}: {value}'.format(key=k, value=v))
    except AttributeError:
        raise


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from . import __version__
    click.echo('adefa {}'.format(__version__))
    ctx.exit()


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


@cli.command()
@click.argument('name', type=str)
def create(name):
    """
    Create new project.
    :param name: project name
    """
    res = client.create_project(name=name)
    print(res.get('project').get('arn'))


@cli.command()
@click.argument('type', type=click.Choice(['devices', 'projects', 'uploads', 'groups', 'runs', 'jobs']))
@click.argument('arn', type=str, required=False)
def list(type, arn):
    """
    Get list of data by selected type.
    :param type: devices, projects | uploads | pools | runs | results
    :param arn: project id | run id
    """
    res = None

    if type == 'devices':
        res = client.list_devices().get('devices')
    elif type == 'projects':
        res = client.list_projects().get('projects')
    elif type == 'jobs':
        if not arn:
            arn = click.prompt('Enter run arn', type=str)
        res = client.list_jobs(arn=arn).get('jobs')
    else:
        if not arn:
            arn = click.prompt('Enter project arn', type=str)

        if type == 'groups':
            res = client.list_device_pools(arn=arn).get('devicePools')
        elif type == 'uploads':
            res = client.list_uploads(arn=arn).get('uploads')
        elif type == 'runs':
            res = client.list_runs(arn=arn).get('runs')
    print_api_response(res) if res else print('--no data--')


@cli.command()
@click.argument('type', type=click.Choice(['project', 'upload', 'group', 'run']))
@click.argument('arn', type=str)
def delete(type, arn):
    """
    Delete data by arn.
    :param type: project | upload | group | run
    :param arn: id
    """
    if type == 'project':
        client.delete_project(arn=arn)
    elif type == 'upload':
        client.delete_upload(arn=arn)
    elif type == 'group':
        client.delete_device_pool(arn=arn)
    elif type == 'run':
        client.delete_run(arn=arn)


@cli.command()
@click.option('-n', '--name', required=True, help='Upload name')
@click.option('-p', '--project', required=True, help='Project arn')
@click.option('-t', '--type', required=True, help='Upload type', type=click.Choice([
    'ANDROID_APP', 'IOS_APP, WEB_APP', 'EXTERNAL_DATA', 'APPIUM_JAVA_JUNIT_TEST_PACKAGE',
    'APPIUM_JAVA_TESTNG_TEST_PACKAGE', 'APPIUM_PYTHON_TEST_PACKAGE', 'APPIUM_WEB_JAVA_JUNIT_TEST_PACKAGE',
    'APPIUM_WEB_JAVA_TESTNG_TEST_PACKAGE', 'APPIUM_WEB_PYTHON_TEST_PACKAGE', 'CALABASH_TEST_PACKAGE',
    'INSTRUMENTATION_TEST_PACKAGE', 'UIAUTOMATION_TEST_PACKAGE', 'UIAUTOMATOR_TEST_PACKAGE',
    'XCTEST_TEST_PACKAGE', 'XCTEST_UI_TEST_PACKAGE)']))
@click.option('-f', '--file', required=True, help='File path (.ipa|.apk|.zip)')
def upload(name, project, type, file):
    """
    Upload an app or test script.
    :param name: upload name
    :param arn: project id
    :param file: file that want to be uploaded
    :param type: upload type
    """
    CONTENT_TYPE = 'application/octet-stream'
    res = client.create_upload(projectArn=project, name=name, type=type, contentType=CONTENT_TYPE)
    upload = res.get('upload')

    if upload:
        import requests

        url = upload.get('url')

        if 'http' in file:
            from urllib import request
            with request.urlopen(file) as fp:
                data = fp.read()
                requests.put(url, data=data, headers={'content-type': CONTENT_TYPE})
        else:
            with open(file, 'rb') as fp:
                data = fp.read()
                requests.put(url, data=data, headers={'content-type': CONTENT_TYPE})

        print(upload.get('arn'))


@cli.command()
@click.option('-n', '--name', required=True, help='Pool name')
@click.option('-p', '--project', required=True, help='Project arn')
@click.option('-d', '--device', required=True, multiple=True, help='Device arn')
def group(name, project, device):
    """
    Create a device group / pool.
    :param name: group name
    :param project: project id
    :param device: device id
    """
    device_str = '['
    for pos, item in enumerate(device):
        device_str += '"{item}"'.format(item=item)
        if pos == len(device) - 1:
            device_str += ']'
        else:
            device_str += ', '
    rules = [{'attribute': 'ARN', 'operator': 'IN', 'value': device_str}]
    res = client.create_device_pool(name=name, projectArn=project, rules=rules)
    print(res.get('devicePool').get('arn'))


@cli.command()
@click.option('-n', '--name', required=True, help='Run name')
@click.option('-p', '--project', required=True, help='Project arn')
@click.option('-a', '--app', required=True, help='App arn')
@click.option('-r', '--type', required=True, help='Type of run', type=click.Choice([
    'BUILTIN_FUZZ', 'BUILTIN_EXPLORER, APPIUM_JAVA_JUNIT', 'APPIUM_JAVA_TESTNG', 'APPIUM_PYTHON',
    'APPIUM_WEB_JAVA_JUNIT', 'APPIUM_WEB_JAVA_TESTNG', 'APPIUM_WEB_PYTHON', 'CALABASH', 'INSTRUMENTATION',
    'UIAUTOMATION', 'UIAUTOMATOR', 'XCTEST', 'XCTEST_UI']))
@click.option('-t', '--test', required=True, help='Test arn')
@click.option('-g', '--group', required=True, help='Device group arn')
def run(name, project, app, type, test, group):
    """
    Schedule test to be run.
    :param name: run name
    :param project: project id
    :param app: app id
    :param type: run type
    :param test: test id
    :param group: device group id
    """
    res = client.schedule_run(
        name=name, projectArn=project, appArn=app, test={'type': type, 'testPackageArn': test}, devicePoolArn=group
    )
    print(res.get('run').get('arn'))


@cli.command()
@click.argument('arn', type=str, required=True)
@click.option('-a', '--total-attempts', type=int, default=10, help='Total attempts to check the result.')
@click.option('-d', '--delay', type=float, default=30, help='Delay time between attempt.')
@click.option('-j', '--json-output', is_flag=True, default=False, help='Print result as json format.')
@click.option('-r', '--result-only', is_flag=True, default=False,
              help='Print only the result as soon as run is completed.')
def result(arn, total_attempts, delay, json_output, result_only):
    """
    Get result by run id.
    :param arn: run id
    :param total_attempts: total attempts
    :param delay: delay time between attempt
    :param json_output: print as json format if True
    :param result_only: print only the result as soon as run is completed if True
    """
    # Waiting until run is completed (10 attempts with given sleep interval)
    attempt = 1
    try:
        while attempt <= total_attempts:
            run = client.get_run(arn=arn).get('run')
            status = run.get('status')

            if status:
                from time import sleep
                if status != 'COMPLETED':
                    if not result_only:
                        print('Attempt: {}'.format(attempt))
                        print('Test status: {}'.format(status))
                        sleep(delay)
                        attempt += 1
                        if attempt > total_attempts:
                            print('--TIMEOUT--')
                else:
                    # Get list of jobs by run arn / id
                    jobs = client.list_jobs(arn=arn).get('jobs')

                    # Delete unneeded key
                    for j in jobs:
                        for k in j.copy().keys():
                            if 'arn' not in k and 'name' not in k:
                                j.pop(k, None)

                    # Add XML and Video key
                    items = ['xml', 'video']
                    for j in jobs:
                        artifacts = client.list_artifacts(arn=j.get('arn'), type='FILE').get('artifacts')

                        for a in artifacts:
                            for i in items:
                                if i in a.get('type').lower():
                                    j[i] = a.get('url')

                    if json_output:
                        import json
                        print(json.dumps(jobs))
                    else:
                        print_api_response(jobs)
                    break
            else:
                if not result_only:
                    print('Run status cannot be found!')
                break
    except AttributeError:
        raise
    except TypeError:
        raise


if __name__ == '__main__':
    cli()
