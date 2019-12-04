# Custom imports
import settings as s

if s.from_database:
    dwh_username = "<personal email>"
    dwh_password = "<password>"
else:
    dwh_username = "<username data warehouse>"
    dwh_password = "<password data warehouse>"

dwh_con_string = "<connection for JupyterHub>"