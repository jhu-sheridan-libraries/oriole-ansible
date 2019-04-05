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
docker stop okapi mod-oriole mod-configuration mod-authtoken mod-permissions mod-login mod-users
docker rm okapi mod-oriole mod-configuration mod-authtoken mod-permissions mod-login mod-users
runuser -l postgres -c "dropdb okapi; dropdb okapi_modules; dropuser diku_mod_configuration; dropuser diku_mod_login; dropuser diku_mod_oriole; dropuser diku_mod_permissions; dropuser diku_mod_users;"
```

## 4. On local dev machine, use ansible to deploy again

```
ansible-playbook -i inventory/test main.yml -v
```
