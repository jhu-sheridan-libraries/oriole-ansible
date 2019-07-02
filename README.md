# using ansible to check on okapi
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants' -vv

 # using curl to check on okapi
ansible oriole -m raw -a "curl localhost:9130"

# can also delete tenants
ansible oriole -m uri -a 'method="DELETE" url=http://localhost:9130/_/proxy/tenants/jh-test'
- this does return a failure

# Useful ansible commands

## Set up local oriole-dev server

Create vagrant and oriole

```
time vagrant up && time ansible-playbook main.yml  -v
```

## Set up remote oriole-test server

```
ansible-playbook -i inventory/test main.yml -v
```

## Commands to interact with docker containers

List docker containers

```
ansible oriole -m raw --become -a "docker ps "
```

View docker logs

```
ansible oriole -m raw --become -a "docker logs --tail=50  okapi"
ansible oriole -m raw --become -a "docker logs --tail=50  okapi"
```

Get list of instances on a docker network

```
ansible oriole -m raw --become -a "docker network inspect --format={%raw%}'{{range .Containers}}{{println .Name}}{{end}}'{%endraw%} backend"
```

## Other ansible Commands

Get tenants, modules, discovery, envs

```
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/modules'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/discovery'
ansible oriole -m uri -a "url=http://localhost:9130/_/env"
```

# Upgrade mod-oriole

Here's the workflow to upgrade mod-oriole.

## 1. Build mod-oriole, and upload it to docker hub.

Refer to the documentation in the mod-oriole project for how to do this.

## 2. Update these files

In the following file, update the mod-oriole versions

* inventory/group_vars/all/okapi.yml

Rename the mod-oriole module descriptor file with new version

```
git mv playboooks/files/descriptors/mod-oriole-{old-version}.json playboooks/files/descriptors/mod-oriole-{new-version}.json
```

and make necessary changes (such as changes to permissions and module descriptors)

## 3. Remove okapi-modules and database tables

SSH to the server, and remove all okapi modules and database tables.

For example, to upgrade mod-oriole on oriole-test.library.jhu.edu

```
ssh oriole-test.library.jhu.edu
# after login, become sudoer and do the following:
sudo su -
docker stop okapi mod-oriole mod-configuration mod-authtoken mod-permissions mod-login mod-users mod-password-validator mod-notify mod-users-bl mod-login-saml mod-licenses
docker rm okapi mod-oriole mod-configuration mod-authtoken mod-permissions mod-login mod-users mod-password-validator mod-notify mod-users-bl mod-login-saml mod-licenses
runuser -l postgres -c "dropdb okapi; dropdb okapi_modules; dropuser diku_mod_configuration; dropuser diku_mod_login; dropuser diku_mod_oriole; dropuser diku_mod_permissions; dropuser diku_mod_users; dropuser diku_mod_password_validator; dropuser diku_mod_notify;"
docker image rm jhulibraries/mod-oriole:1.0.17
```

If there's a connection error, shutdown postgresql and restart it before drop the databases

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


## To upgrade a module

docker stop module
docker rm module
docker image rm # clean up image

update database
delete row in okapi.public.deployments for mod-oriole
delete row in okapi.public.modules for mod-oriole
