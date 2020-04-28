# ISpindle Service

## Usage

All responses will have the form

```json
{
    "message": "Description of what happened",
    "data": "Mixed type holding the content of the response"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all spindles

#### Definition

`GET /spindles`

#### Response

- `200 OK` on success

```json
[
    "Spindle01",
    "Spindle02"
]
```

## Lookup Spindle details

`GET /device/<identifier>`

### Response

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "identifier": "spindle01",
    "name": "DieSpindel01",
    "ID":3746707,
    "token":"A1E-IZtoP8oAhbKV0SUKTCw4IjOcyfel9s",
    "angle":46.95489,
    "temperature":24.75,
    "temp_units":"C",
    "battery":3.799102,
    "gravity":11.4164,
    "interval":1,
    "RSSI":-54,
    "dateTime":"someDateTime"
}
```

## Delete a device

#### Definition

`DELETE /devices/<identifier>`

#### Response

- `404 Not Found` if the device does not exist
- `204 No Content` on success