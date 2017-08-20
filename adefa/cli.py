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
            print('no: {pos}'.format(pos=p))
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


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
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
    print_item(res.get('project'))


@cli.command()
@click.argument('type', type=click.Choice(['projects', 'uploads', 'results', 'runs']))
def list(type):
    """
    Get list of data by selected type.
    :param type: projects | uploads | results | runs
    """
    res = None
    if type == 'projects':
        res = client.list_projects().get('projects')
    elif type == 'uploads':
        print('TODO')
    elif type == 'results':
        print('TODO')
    elif type == 'runs':
        print('TODO')
    else:
        print('Invalid option!')

    print_api_response(res) if res else print('--no data--')


@cli.command()
@click.argument('type', type=click.Choice(['project', 'upload']))
@click.argument('arn', type=str)
def delete(type, arn):
    """
    Delete data of selected type by arn.
    :param type: project | upload
    :param arn: arn
    """
    if type == 'project':
        client.delete_project(arn=arn)
    elif type == 'upload':
        client.delete_upload(arn=arn)
    else:
        print('TODO')


@cli.command()
@click.option('-a', '--arn', required=True, help='Project arn')
@click.option('-f', '--file', required=True, help='File (.ipa|.apk|.zip)')
@click.option('-t', '--type', required=True, help='Upload type', type=click.Choice([
    'ANDROID_APP', 'IOS_APP, WEB_APP', 'EXTERNAL_DATA', 'APPIUM_JAVA_JUNIT_TEST_PACKAGE',
    'APPIUM_JAVA_TESTNG_TEST_PACKAGE', 'APPIUM_PYTHON_TEST_PACKAGE', 'APPIUM_WEB_JAVA_JUNIT_TEST_PACKAGE',
    'APPIUM_WEB_JAVA_TESTNG_TEST_PACKAGE', 'APPIUM_WEB_PYTHON_TEST_PACKAGE', 'CALABASH_TEST_PACKAGE',
    'INSTRUMENTATION_TEST_PACKAGE', 'UIAUTOMATION_TEST_PACKAGE', 'UIAUTOMATOR_TEST_PACKAGE',
    'XCTEST_TEST_PACKAGE', 'XCTEST_UI_TEST_PACKAGE)']))
def upload(arn, file, type):
    """
    Upload an app or test script.
    :param arn: project arn
    :param file: file that want to be uploaded
    :param type: upload type
    :return:
    """
    res = client.create_upload(projectArn=arn, name=file, type=type)
    print_item(res.get('upload'))


@cli.command()
def pool():
    """Create device pool."""
    # TODO
    print('create device pool')


@cli.command()
def schedule():
    """Schedule test to be run."""
    # TODO
    print('Schedule test')


if __name__ == '__main__':
    cli()
