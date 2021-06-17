import json, os

f = 'bs_servers.json'

a = {
	'OMEGA PRIVATE TEAMS': {
        "dc_owner": 747836507527708692,
        "chnl": 853992555233411114,
        "ip": "13.232.158.250",
        "key": "E:\\NK2\\bot\\BlackPearl#7788\\bp\\bs_servers\\OMEGA PRIVATE TEAMS\\Omega16New.pem",
        "build": "custom",
        "ls": "/home/ubuntu/oteams/dist/ba_root/mods/stats/ls.json"
	}
}
print(a)
f = open(f, 'w')
f.write(json.dumps(a, indent=4))
f.close()

print('done')