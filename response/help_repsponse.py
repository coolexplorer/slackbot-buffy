from response.base_response import BaseResponse


class HelpResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)

    def get_help_response(self, responses):
        return self.get_response(responses)

    def get_help_template(self, type, commands, sub_commands):
        usage = f"{type} <command> <sub command> <params>\n"
        command_help = ""

        for command in commands:
            command_help += self._get_command(command, sub_commands.get(command, []))

        return [f'''
Usage : {usage}
Command : 
{command_help}
''']

    def _get_command(self, command, sub_commands):
        response = ""
        response += f"\t- {command}\n"

        if len(sub_commands) > 0:
            response += "\t\tSub Commands : \n"
            for sub_command in sub_commands:
                response += f"\t\t\t- {sub_command}\n"

        return response
