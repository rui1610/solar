CHANNELS_TO_USE = [
    {
        "deviceName": "Batterie",
        "measurements": [
            {
                "channel": "30849",
                "device": "Batterie",
                "name": "Temperatur",
                "transformation": "JS(divide10.js)",
                "unit": "C",
            },
            {
                "channel": "30847",
                "device": "Batterie",
                "name": "Kapazität aktuell",
                "unit": "%",
            },
            {
                "channel": "30845",
                "device": "Batterie",
                "name": "Ladezustand aktuell",
                "unit": "%",
            },
            {
                "channel": "31401",
                "device": "Batterie",
                "name": "Entladung gesamt",
                "unit": "W",
            },
            {
                "channel": "31397",
                "device": "Batterie",
                "name": "Ladung gesamt",
                "unit": "W",
            },
            {
                "channel": "31395",
                "device": "Batterie",
                "name": "Entladung aktuell",
                "unit": "W",
            },
            {
                "channel": "31393",
                "device": "Batterie aktuell",
                "name": "Ladung",
                "unit": "W",
            },
        ],
    },
    {
        "device": "Netz",
        "measurements": [
            {
                "channel": "32341",
                "device": "Netz",
                "name": "Einspeisung aktuell",
                "unit": "W",
            },
            {
                "channel": "30867",
                "device": "Netz",
                "name": "Leistung Einspeisung",
                "unit": "W",
            },
            {
                "channel": "30865",
                "device": "Netz",
                "name": "Leistung Bezug",
                "unit": "W",
            },
        ],
    },
    {
        "device": "Haus",
        "measurements": [
            {
                "channel": "30775",
                "device": "Haus",
                "name": "Leistungsaufnahme aktuell",
                "unit": "W",
            },
        ],
    },
    {
        "device": "Solar2",
        "measurements": [
            {
                "channel": "30529",
                "device": "PV vorne",
                "name": "Ertrag gesamt",
                "unit": "W",
            },
            {
                "channel": "30529",
                "device": "PV vorne",
                "name": "Ertrag gesamt",
                "unit": "W",
            },
        ],
    },
    {
        "device": "MA Wechselrichter",
        "measurements": [
            {
                "channel": "30953",
                "device": "SMA Wechselrichter",
                "name": "Temperatur",
                "unit": "C",
            },
        ],
    },
]
