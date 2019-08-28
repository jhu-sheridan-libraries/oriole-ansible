# Oriole-ansible Quick Start

## Set up local testing server

### Install prequisites

* Ansible
* Virtual Box and Vagrant

Install vagrant-hostsupdater plugin

```
vagrant plugin install vagrant-hostsupdater
```

### Check out this repo

```
git clone git@github.com:jhu-sheridan-libraries/oriole-ansible.git
```

### Create ini file

Edit playbooks `playbooks/create-ini.yml`

### Provision a vagrant box for the first time

First create a file in ~/.ssh/oriole-ansible/vault_password_file. The password is in lastpass. Save the value in the file.

Make sure there is a file `~/.ssh/config`, and it's mask is 600. 

```
vagrant up --provision
```

After this step, there will be a record in ~/.ssh/config for oriole-dev.test

You may want to add an alias for 'oriole-dev' in the config file.

### Set up SSH

Next set up SSH keywordless for the deploy user.

The passphrase is stored in `inventory/group_vars/dev/vault.yml`. See the passphrase

```
ansible-vault view inventory/group_vars/dev/vault.yml | cat
```

Try

```
ssh oriole-dev
```

Enter the passphrase to login.

Add the key to keychain on MacOS:

```
ssh-add -K ~/.ssh/oriole-ansible/oriole-ansible_dev
```

Note the `-K` option is not necessary on linux like Centos. 

### Run ansible-playbook

```
ansible-playbook -i inventory/dev main.yml -v
```

## Set up oriole-test

First make sure that you have passwordless login set up on oriole-test. 

Then Modify the file ansible.cfg

Set remote_user to your jhed_id. 

Then run 

```
ansible-playbook setup.yml -i inventory/test -v -K
```

This will create the ssh keys. 

Revert changes to ansible.cfg

```
git checkout ansible.cfg
```

# Upgrade mod-oriole

Here's the workflow to upgrade mod-oriole.

## 1. Build mod-oriole, and upload it to docker hub.

In `mod-oriole` directory, run 

```
mvn clean install -DskipTests
```

It will automatically build the docker image. Push it to docker hub. 

Refer to the documentation in the mod-oriole project for details. 

## 2. Update these files

In the following file, update the mod-oriole versions

* inventory/group_vars/all/okapi.yml

Rename the mod-oriole module descriptor file with new version

```
git mv playboooks/files/descriptors/mod-oriole-{old-version}.json playboooks/files/descriptors/mod-oriole-{new-version}.json
```

and make necessary changes (such as changes to permissions and module descriptors)

## 3. Remove okapi-modules and database tables

SSH to oriole-test.library.jhu.edu

```
sudo su -
docker stop mod-oriole 
# If the following step fails, try stop all modules: 
# docker stop okapi mod-oriole mod-configuration mod-authtoken mod-permissions mod-login mod-users mod-password-validator mod-notify mod-users-bl mod-login-saml mod-licenses
docker rm mod-oriole
docker image rm jhulibraries/mod-oriole:{version}
```

Next you need to update the database, and remove the rows for `mod-oriole` in the following tables (TODO: Script this step):

* delete row in okapi.public.deployments for mod-oriole
* delete row in okapi.public.modules for mod-oriole

## 4. On local dev machine, use ansible to deploy again

```
ansible-playbook -i inventory/test main.yml -v
```

## Note: Redhat networking docker issues

Redhat/Centos: NetworkManager has issues managing the docker network/s
https://success.docker.com/article/should-you-use-networkmanager

The following has been ansiblized.
Ensure we have stopped network manager, and trust docekr networks  
systemctl stop NetworkManager.service
systemctl disable NetworkManager.service
firewall-cmd --permanent --zone=trusted --change-interface=docker0
firewall-cmd --permanent --zone=trusted --add-interface=dockernet


## Some useful commands

### using ansible to check on okapi
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants' -vv

### using curl to check on okapi
ansible oriole -m raw -a "curl localhost:9130"

### can also delete tenants
ansible oriole -m uri -a 'method="DELETE" url=http://localhost:9130/_/proxy/tenants/jh-test'
- this does return a failure

### Other ansible Commands

Get tenants, modules, discovery, envs

```
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/modules'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/discovery'
ansible oriole -m uri -a "url=http://localhost:9130/_/env"
```
