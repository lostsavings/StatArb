# Setup
1. Setup a virtualenvironment in the root directory and install requirements.
2. Create a file `configs/psql.yaml` containing the postgresql db configuration. Here's a template (you will need to replace some of these values - probably host and password):
```yaml
host: 127.0.0.1
username: finance
password: password_here
database: stat_arb
```