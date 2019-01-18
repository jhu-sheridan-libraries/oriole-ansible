# using ansible to check on okapi
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants' -vv

 # using curl to check on okapi
ansible oriole -m raw -a "curl localhost:9130"

# can also delete tenants
ansible oriole -m uri -a 'method="DELETE" url=http://localhost:9130/_/proxy/tenants/jh-test'
- this does return a failure

# Usefull ansible commands

Create  vagrant and oriale
``` 
time vagrant up && time ansible-playbook main.yml  -v
```
List docker contains
ansible oriole -m raw --become -a "docker ps "

Get tenants, modules, discovery, envs
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/tenants'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/proxy/modules'
ansible oriole --become  -m uri -a 'url=http://localhost:9130/_/discovery'
ansible oriole -m uri -a "url=http://localhost:9130/_/env" 

View docker logs 
ansible oriole -m raw --become -a "docker logs --tail=50  okapi"
ansible oriole -m raw --become -a "docker logs --tail=50  okapi"

Get list of isntances on a docker network
ansible oriole -m raw --become -a "docker network inspect --format={%raw%}'{{range .Containers}}{{println .Name}}{{end}}'{%endraw%} backend"

Get the oriole resources
 curl -D - -w '\n' -H 'X-Okapi-Tenant: diku' http://oriole-dev:9130/oriole-resources
