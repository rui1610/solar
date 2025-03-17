CHANNELS_TO_USE = [
    {
        "deviceName": "Batterie",
        "measurements": [
            {
                "address": "30849",
                "name": "Temperatur",
                "transformation": "JS( | parseFloat(input) / 10 )",
                "unit": "%.1f °C",
                "category": "temperature",
            },
            {
                "address": "30847",
                "name": "Kapazität aktuell",
                "unit": "%d%%",
            },
            {
                "address": "30845",
                "name": "Ladezustand aktuell",
                "unit": "%d%%",
            },
            # {
            #     "address": "31401",
            #     "name": "Entladung gesamt",
            #     "unit": "%.1f W",
            # },
            # {
            #     "address": "31397",
            #     "name": "Ladung gesamt",
            #     "unit": "%.1f W",
            # },
            {
                "address": "31395",
                "name": "Entladung aktuell",
                "unit": "%.1f W",
                "category": "power",
            },
            {
                "address": "31393",
                "name": "Ladung",
                "unit": "%.1f W",
                "category": "power",
            },
        ],
    },
    {
        "deviceName": "Netz",
        "measurements": [
            {
                "address": "32341",
                "name": "Einspeisung aktuell",
                "unit": "%.1f W",
                "category": "power",
            },
            {
                "address": "30867",
                "name": "Leistung Einspeisung",
                "unit": "%.1f W",
                "category": "power",
            },
            {
                "address": "30865",
                "name": "Leistung Bezug",
                "unit": "%.1f W",
                "category": "power",
            },
        ],
    },
    {
        "deviceName": "Haus",
        "measurements": [
            {
                "address": "30775",
                "name": "Leistungsaufnahme aktuell",
                "unit": "%.1f W",
                "category": "power",
            },
        ],
    },
    {
        "deviceName": "Solaranlage",
        "measurements": [
            {
                "address": "30529",
                "name": "Ertrag gesamt",
                "transformation": "JS( | parseFloat(input) / 1000 )",
                "unit": "%.1f kWh",
                "category": "energy",
            },
        ],
    },
    {
        "deviceName": "SMA Wechselrichter",
        "measurements": [
            {
                "address": "30953",
                "name": "Temperatur",
                "unit": "%.1f °C",
                "category": "temperature",
            },
        ],
    },
]
