# python_and_slack

This is a Python application that monitors the Linux file system for file movements, deletions, and additions within a specified directory. Upon detecting these events, the application will send corresponding messages on Slack.

To ensure seamless integration with the system, the application will be designed to run as a SystemD service. In the event of any failure within the SystemD environment, appropriate error messages will be sent to notify the system of the service's failure.
