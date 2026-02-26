import json

with open('c:/Users/dania/PP2_Practice/W3Schools/Practice4/Exercises/JSON/sample-data.json', 'r') as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':6}")
print("-" * 50, "-" * 20, "-" * 7, "-" * 6)
for item in data['imdata']:
    attrs = item['l1PhysIf']['attributes']
    if attrs['id'] in ['eth1/33', 'eth1/34', 'eth1/35']:
        print(f"{attrs['dn']:50} {attrs.get('descr', ''):20} {attrs['speed']:7} {attrs['mtu']:6}")