## Inolova task: Simple Coffe store app API
#### Using flask to build a simple API for a Coffe app with two screens. And mongodb Atlas cloud (free tier) to host the data

### Simple API reference
##### PATH: /api/COFFEE_MACHINES - METHOD: GET
##### Get a list of coffee machines filtered based on url parameters
##### URL PARAMETERS:
- product_type: ```COFFEE_MACHINE_LARGE | COFFEE_MACHINE_SMALL | ESPRESSO_MACHINE```
- water_line_compatible:```True | False```
--------------------------------------------------------
##### PATH: /api/COFFEE_PDS - METHOD: GET
##### Get a list of coffee pods filtered based on url parameters
##### URL PARAMETERS:
- product_type: ```COFFEE_POD_LARGE | COFFEE_POD_SMALL | ESPRESSO_POD```
- coffee_flavor: ```COFFEE_FLAVOR_VANILLA | COFFEE_FLAVOR_CARAMEL | COFFEE_FLAVOR_PSL | COFFEE_FLAVOR_MOCHA | COFFEE_FLAVOR_HAZELNUT```
- pack_size: ```1 | 3 | 5 | 7```

### Sample requests and responses
#### All espresso machines: 
```GET api/COFFEE_MACHINES?product_type=ESPRESSO_MACHINE```

RESPONSE: 
```
{
   "count":3,
   "payload":[
      {
         "SKU":"EM001",
         "product_type":"ESPRESSO_MACHINE",
         "water_line_compatible":false
      },
      {
         "SKU":"EM002",
         "product_type":"ESPRESSO_MACHINE",
         "water_line_compatible":false
      },
      {
         "SKU":"EM003",
         "product_type":"ESPRESSO_MACHINE",
         "water_line_compatible":true
      }
   ],
   "success":true
}
```
#### All small pods: 
```GET api/COFFEE_PODS?product_type=COFFEE_POD_SMALL```

RESPONSE: 
```
{
   "count":10,
   "payload":[
      {
         "SKU":"CP001",
         "coffee_flavor":"COFFEE_FLAVOR_VANILLA",
         "pack_size":1,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP003",
         "coffee_flavor":"COFFEE_FLAVOR_VANILLA",
         "pack_size":3,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP011",
         "coffee_flavor":"COFFEE_FLAVOR_CARAMEL",
         "pack_size":1,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP013",
         "coffee_flavor":"COFFEE_FLAVOR_CARAMEL",
         "pack_size":3,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP021",
         "coffee_flavor":"COFFEE_FLAVOR_PSL",
         "pack_size":1,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP023",
         "coffee_flavor":"COFFEE_FLAVOR_PSL",
         "pack_size":3,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP031",
         "coffee_flavor":"COFFEE_FLAVOR_MOCHA",
         "pack_size":1,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP033",
         "coffee_flavor":"COFFEE_FLAVOR_MOCHA",
         "pack_size":3,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP041",
         "coffee_flavor":"COFFEE_FLAVOR_HAZELNUT",
         "pack_size":1,
         "product_type":"COFFEE_POD_SMALL"
      },
      {
         "SKU":"CP043",
         "coffee_flavor":"COFFEE_FLAVOR_HAZELNUT",
         "pack_size":3,
         "product_type":"COFFEE_POD_SMALL"
      }
   ],
   "success":true
}
```
#### All pods sold in 7 dozen packs
GET api/COFFEE_PODS?pack_size=7

RESPONSE: 
```
{
   "count":2,
   "payload":[
      {
         "SKU":"EP007",
         "coffee_flavor":"COFFEE_FLAVOR_VANILLA",
         "pack_size":7,
         "product_type":"ESPRESSO_POD"
      },
      {
         "SKU":"EP017",
         "coffee_flavor":"COFFEE_FLAVOR_CARAMEL",
         "pack_size":7,
         "product_type":"ESPRESSO_POD"
      }
   ],
   "success":true
}
```
