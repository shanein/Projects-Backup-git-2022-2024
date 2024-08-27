## PREREQUESITES
Use "ansible_user=<YOUR_USER>" in the inventory for the first run

You may need to change the username value in the playbook vars

## NEXT RUNS
Use "ansible_user=ansibleadmin" in the inventory for all next runs

## RUN 
````
ansible-playbook -i inventory.ini playbook.yml --private-key=./private.key --ask-vault-pass --ask-become-pass
````
