import os
from collections import namedtuple
from pathlib import Path
from importlib import resources

import click
from jinja2 import Template
from lxml import etree


with resources.open_text('idea', 'module_tpl.xml') as fid:
    MODULE_TPL = Template(fid.read())


Directory = click.Path(file_okay=False, exists=True, resolve_path=True)


@click.group()
def cli():
    """IntelliJ IDEA helper utility"""
    pass


def get_project_root():
    path = Path(os.getcwd())
    while path.parent:
        if (path / '.idea').exists():
            return path
        path = path.parent
    raise click.BadParameter("Doesn't look like you're inside an IDEA project")


def read_xml(xml_path: Path) -> etree.ElementTree:
    if not xml_path.exists():
        raise click.BadParameter(f'File "{str(xml_path)}" does not exist')
    return etree.fromstring(xml_path.read_bytes())


Module = namedtuple('Module', ['iml', 'root'])


@cli.command(name='list')
def list_modules():
    """List project's modules"""
    project = get_project_root()
    xml_path = project / '.idea' / 'modules.xml'
    xml_node = read_xml(xml_path).find('component/modules')

    root = str(project.absolute())

    def get_module_root(module_path: Path) -> Path:
        module_xml = read_xml(module_path)
        module_root = module_xml.find('component/content').attrib['url']
        return Path(module_root.replace('file://$MODULE_DIR$', root))

    configs = [Path(m.attrib['filepath'].replace('$PROJECT_DIR$', root))
               for m in xml_node.iterchildren()]
    modules = [Module(config, get_module_root(config)) for config in configs]
    for module in modules:
        print(f'{str(module.iml)}: {str(module.root)}')


@cli.command(name='scan')
def scan_modules():
    """List project's modules"""
    project_dir = get_project_root()
    for path in project_dir.glob('**/pom.xml'):
        if 'node_modules' not in path.parents:
            print(path.parent.relative_to(project_dir))


@cli.command()
@click.argument('path', type=Directory)
@click.option('-n', '--name', help='Custom module name')
def add(path: str, name=None, project=os.getcwd()):
    """Add a module to the project"""
    module_root = Path(path)
    name = module_root.name if not name else name

    project_dir = get_project_root()
    idea_dir = project_dir / '.idea'
    iml_path = idea_dir / f'{name}.iml'
    if iml_path.exists():
        raise click.BadParameter(f'Module "{str(iml_path)}" already exists')
    xml_path = idea_dir / 'modules.xml'
    if not xml_path.exists():
        raise click.BadParameter(f'File "{str(xml_path)}" does not exist')

    def rel(glob):
        return [p.relative_to(project_dir) for p in module_root.glob(glob)]

    module_iml = MODULE_TPL.render(
        module_root=module_root.relative_to(project_dir),
        source_folders=rel('src'),
        test_folders=rel('test*'),
        exclude_folders=rel('dist'),
        exclude_patterns=[
            '.cache',
            '.vscode',
            'node_modules'
        ]
    )
    click.echo(f'Writing {iml_path.relative_to(project_dir)}')
    iml_path.write_text(module_iml)

    xml = read_xml(xml_path)
    xml.find('component/modules').append(etree.Element('module', {
        'fileurl': f'file://$PROJECT_DIR$/.idea/{name}.iml',
        'filepath': f'$PROJECT_DIR$/.idea/{name}.iml'
    }))
    click.echo(f'Updating {xml_path.relative_to(project_dir)}')
    xml_path.write_bytes(etree.tostring(xml, method='xml'))
