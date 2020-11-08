gitlab_commands = [
    'project',
    'pipeline',
    'variable'
]

gitlab_project_sub_commands = [
    'list',
    'search'
]

gitlab_pipeline_sub_commands = [
    'list',
    'variable',
    'run'
]

gitlab_variable_sub_commands = [
    'list'
]

gitlab_sub_commands = {
    'project': gitlab_project_sub_commands,
    'pipeline': gitlab_pipeline_sub_commands,
    'variable': gitlab_variable_sub_commands
}
