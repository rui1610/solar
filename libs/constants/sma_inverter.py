CHANNELS_TO_USE = [
    {
        "deviceName": "Batterie",
        "measurements": [
            {
                "address": "30849",
                "name": "Temperatur",
                "transformation": "JS( | input / 10 )",
                "unit": "C",
            },
            {
                "address": "30847",
                "name": "Kapazität aktuell",
                "unit": "%",
            },
            {
                "address": "30845",
                "name": "Ladezustand aktuell",
                "unit": "%",
            },
            {
                "address": "31401",
                "name": "Entladung gesamt",
                "unit": "W",
            },
            {
                "address": "31397",
                "name": "Ladung gesamt",
                "unit": "W",
            },
            {
                "address": "31395",
                "name": "Entladung aktuell",
                "unit": "W",
            },
            {
                "address": "31393",
                "name": "Ladung",
                "unit": "W",
            },
        ],
    },
    {
        "deviceName": "Netz",
        "measurements": [
            {
                "address": "32341",
                "name": "Einspeisung aktuell",
                "unit": "W",
            },
            {
                "address": "30867",
                "name": "Leistung Einspeisung",
                "unit": "W",
            },
            {
                "address": "30865",
                "name": "Leistung Bezug",
                "unit": "W",
            },
        ],
    },
    {
        "deviceName": "Haus",
        "measurements": [
            {
                "address": "30775",
                "name": "Leistungsaufnahme aktuell",
                "unit": "W",
            },
        ],
    },
    {
        "deviceName": "Solar2",
        "measurements": [
            {
                "address": "30529",
                "name": "Ertrag gesamt",
                "unit": "W",
            },
            {
                "address": "30529",
                "name": "Ertrag gesamt",
                "unit": "W",
            },
        ],
    },
    {
        "deviceName": "SMA Wechselrichter",
        "measurements": [
            {
                "address": "30953",
                "name": "Temperatur",
                "unit": "C",
            },
        ],
    },
]
