import sys
import argparse
from usorchestrator.manager import UsOrchestratorManager
from usorchestrator.exceptions import UsOrchestratorConfigError, ActionError, RemoteCmdError
from usorchestrator.info import __app_name__, __version__, __description__, __author__, __author_email__, __author_url__, __license__

def main():
   # get args from command line
   parser = argparse.ArgumentParser(description=__description__)

   parser.add_argument('--log', dest='log_file', help='Log file', default=None)
   parser.add_argument('--log-level', dest='log_level', help='Log level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
   parser.add_argument('--version', action='version', version=f'{__app_name__} {__version__}')

   subparsers = parser.add_subparsers(title="Commands", dest="command")

   configtest_parser = subparsers.add_parser('configtest', help='Test configuration file')

   show_parser = subparsers.add_parser('show', help='Show informations regarding different action types')
   show_parser.add_argument('--type', help='Show informations regarding different action types', choices=['hosts_groups', 'tests', 'routines'], required=True)

   orchestrate_parser = subparsers.add_parser('orchestrate', help='Orchestrate actions')
   orchestrate_parser.add_argument('--host', dest='hosts', help='Target host', action='append')
   orchestrate_parser.add_argument('--hosts-group', dest='hosts_groups', help='Target hosts group', action='append')
   orchestrate_parser.add_argument('--command', dest='commands', help='Command to be executed on target hosts', action='append')
   orchestrate_parser.add_argument('--routine', dest='routines', help='Routine to be executed on target hosts', action='append')
   orchestrate_parser.add_argument('--test', dest='tests', help='Test to be executed against target hosts', action='append')
   orchestrate_parser.add_argument('--transfer', dest='transfers', help='Transfer to be executed on target hosts (<local-path>:<remote-path>)', action='append')
    
   args = parser.parse_args()

   if args.command is None:
      parser.print_help()
      sys.exit()

   options = {}

   options['log_file'] = args.log_file
   options['log_level'] = args.log_level

   try:
      usorchestrator = UsOrchestratorManager(options)
   except UsOrchestratorConfigError as e:
      print(f"Config error: {e}\nCheck documentation for more information on how to configure UsOrchestrator hosts or actions")
      sys.exit(2)

   if args.command == 'configtest':
      print("Config OK")
   elif args.command == 'show':
      usorchestrator.show(args.type)
   elif args.command == 'orchestrate':
      options = {}

      options['hosts'] = args.hosts
      options['hosts_groups'] = args.hosts_groups
      options['commands'] = args.commands
      options['routines'] = args.routines
      options['tests'] = args.tests
      options['transfers'] = args.transfers

      usorchestrator.orchestrate(options)