from Register import U32, U64, STR32, S32, S16, U16, Register

from modbus import Modbus


"""
German registers, description and TAGLIST for SMA inverters

Modbus® Parameter und Messwerte
STP 15000TL-30 / STP 17000TL-30 / STP 20000TL-30 / STP 25000TL-30
Diese Liste gilt ab folgender Firmware-Version: 2.83.03.R

to build the list for other languages or other SMA inverters:
1) go to https://www.sma.de/en/products/monitoring-control/modbus-protocol-interface.html
2) under Downloads --> Background Knowledge
3) search the "Modbus list ..." zip file for yor inverter (the zip file includes all languages)
4) import the html-file in excel
5) filter out on column F: "-" and "WO" ... this entries don't work .. you will get an error, if you try to read this
6) build the register list, with a formula (STR32 has a different formula!), see the excel file in this project
7) for the taglist: 
    filter column E for taglist end enum
    extract and union all values from column O (use text editor!)
    back in excel filter unique values, split text data by ":" and "generate code" with a formula  

"""


def set_tripower_TAGLIST():
    Register.SMA_TAGLIST = {
        27: "Sondereinstellung (Adj)",
        35: "Fehler (Alm)",
        42: "AS4777.3 (AS4777.3)",
        51: "Geschlossen (Cls)",
        258: "Schaltzustand Netzrelais (GriSwCpy)",
        295: "MPP (Mpp)",
        302: "------- (None)",
        303: "Aus (Off)",
        306: "Inselbetrieb 60 Hz (OFF-Grid60)",
        307: "Ok (Ok)",
        308: "Ein (On)",
        311: "Offen (Opn)",
        313: "Inselbetrieb 50 Hz (OFF-Grid50)",
        333: "PPC (PPC)",
        336: "Hersteller kontaktieren (PrioA)",
        337: "Installateur kontaktieren (PrioC)",
        338: "ungültig (PrioIna)",
        381: "Stopp (Stop)",
        438: "VDE0126-1-1 (VDE0126-1-1)",
        443: "Konstantspannung (VolDCConst)",
        455: "Warnung (Wrn)",
        557: "Abregelung aufgrund Temperatur (TmpDrt)",
        560: "EN50438 (EN50438)",
        777: "Deutsch (LangDE)",
        778: "English (LangEN)",
        779: "Italiano (LangIT)",
        780: "Español (LangES)",
        781: "Français (LangFR)",
        782: "Ελληνικά (LangEL)",
        783: "한국어 (LangKO)",
        784: "Česky (LangCS)",
        785: "Português (LangPT)",
        786: "Nederlands (LangNL)",
        796: "Slovenski (LangSL)",
        797: "Български (LangBG)",
        798: "Polski (LangPL)",
        799: "日本語 (LangJA)",
        884: "nicht aktiv (NoneDrt)",
        885: "keine (NoneDsc)",
        886: "keine (NoneMsg)",
        887: "keine (NonePrio)",
        1013: "Andere Norm (OthStd)",
        1020: "Mittelspannungsrichtlinie (Deutschland) (MVtgDirective)",
        1032: "MVtgDirective Internal (MVtgDirectiveInt)",
        1041: "Übererregt (OvExt)",
        1042: "Untererregt (UnExt)",
        1069: "Blindleistungs-/Spannungskennlinie Q(U) (VArCtlVol)",
        1070: "Blindleistung Q, direkte Vorgabe (VArCnstNom)",
        1072: "Blindleistung Q, Vorgabe durch Anlagensteuerung (VArCtlCom)",
        1074: "cos Phi, direkte Vorgabe (PFCnst)",
        1075: "cos Phi, Vorgabe durch Anlagensteuerung (PFCtlCom)",
        1076: "cos Phi(P)-Kennlinie (PFCtlW)",
        1077: "Wirkleistungsbegrenzung P in W (WCnst)",
        1078: "Wirkleistungsbegrenzung P in % Pmax (WCnstNom)",
        1079: "Wirkleistungsbegrenzung P durch Anlagensteuerung (WCtlCom)",
        1129: "Ja (Yes)",
        1130: "Nein (No)",
        1233: "SDLWindV (SDLWindV)",
        1264: "Vollständige dynamische Netzstützung (DGSFl)",
        1265: "Eingeschränkte dynamische Netzstützung (DGSPa)",
        1341: "Störungsmeldung (FltInd)",
        1342: "Lüftersteuerung (FanCtl)",
        1343: "Eigenverbrauch (SelfCsmp)",
        1349: "Steuerung über Kommunikation (ComCtl)",
        1359: "Batteriebank (BatCha)",
        1392: "Fehler (Flt)",
        1393: "Warte auf PV-Spannung (WaitPV)",
        1467: "Start (Str)",
        1469: "Herunterfahren (Shtdwn)",
        1480: "Warte auf EVU (WaitUtil)",
        1720: "10 Mbit/s (ConnSpd10)",
        1721: "100 Mbit/s (ConnSpd100)",
        1725: "Keine Verbindung (NotConn)",
        1726: "Halbduplex (HalfDpx)",
        1727: "Vollduplex (FulDpx)",
        1749: "Voller Stopp (FulStop)",
        1779: "Getrennt (Dscon)",
        1780: "Öffentliches Stromnetz (PubGri)",
        1781: "Inselnetz (IsoGri)",
        1855: "Stand-Alone Operation (SocOp)",
        1975: "Spannung in Volt (XRefV)",
        1976: "Spannung in Prozent von Un (XRefVNom)",
        1977: "Var in Prozent von Pmax (YRefVarNom)",
        1978: "Watt in Prozent von Pmax (YRefWNom)",
        1979: "Watt in Prozent der eingefrorenen Wirkleistung (YRefWNomActl)",
        1984: "Blindleistungs-/Spannungskennlinie Q(U) mit Stützpunkten (VArCtlVolCrv)",
        2119: "Abregelung (Drt)",
        2270: "cos Phi- oder Q-Vorgabe durch Anlagensteuerung (VArPFCtlCom)",
        2476: "Wie statische Spannungshaltung (VArModRef)",
        2478: "Sekunden (XRefTms)",
        2479: "Spannung in Prozent von Unenn (YRefVNom)",
        2506: "Werte beibehalten (UsStp)",
        2507: "Verwendung Fallback-Einstellung (UsFlb)",
        7501: "RD1663/661-A (RD1663/661-A)",
        7510: "VDE-AR-N4105 (VDE-AR-N4105)",
        7514: "VDE-AR-N4105-HP (VDE-AR-N4105-HP)",
        7518: "CEI 0-21 extern (CEI0-21Ext)",
        7522: "NEN-EN50438 (NEN-EN50438)",
        7523: "C10/11/2012 (C10/11/2012)",
        7524: "RD1699 (RD1699)",
        7527: "VFR2014 (VFR2014)",
        7528: "G59/3 (G59/3)",
        7529: "SI4777_HS131_Pf (SI4777_HS131_Pf)",
        7530: "MEA2013 (MEA2013)",
        7531: "PEA2013 (PEA2013)",
        7532: "EN50438:2013 (EN50438_2013)",
        7533: "NEN-EN50438:2013 (NEN-EN50438_13)",
        7539: "RD1699/413 (RD1699/413)",
        7540: "KEMCO2013 (KEMCO2013)",
        7549: "AS4777.2_2015 (AS4777.2_2015)",
        7551: "NT_Ley2057 (NT_Ley2057)",
        8001: "Solar-Wechselrichter (DevClss1)",
        9284: "STP 20000TL-30 (STP 20000TL-30)",
        9285: "STP 25000TL-30 (STP 25000TL-30)",
        9336: "STP 15000TL-30 (STP 15000TL-30)",
        9337: "STP 17000TL-30 (STP 17000TL-30)",
        16777213: "Information liegt nicht vor (NaNStt)",
    }


def add_tripower_register(wr: Modbus):
    wr.add_register(
        U32(30001, "SMA.Modbus.Profile", "Versionsnummer SMA Modbus-Profil", "RAW", "")
    )
    wr.add_register(U32(30003, "Nameplate.SusyId", "SUSyID Modul", "RAW", ""))
    wr.add_register(U32(30005, "Nameplate.SerNum", "Seriennummer", "RAW", ""))
    wr.add_register(U32(30051, "Nameplate.MainModel", "Geräteklasse", "TAGLIST", ""))
    wr.add_register(U32(30053, "Nameplate.Model", "Gerätetyp", "TAGLIST", ""))
    wr.add_register(U32(30055, "Nameplate.Vendor", "Hersteller", "TAGLIST", ""))
    wr.add_register(U32(30057, "Nameplate.SerNum", "Seriennummer", "RAW", ""))
    wr.add_register(U32(30059, "Nameplate.PkgRev", "Softwarepaket", "FW", ""))
    wr.add_register(U32(30193, "DtTm.Tm", "Systemzeit", "DT", ""))
    wr.add_register(
        U32(30197, "Operation.Evt.EvtNoShrt", "Aktuelle Ereignisnummer", "FIX0", "")
    )
    wr.add_register(
        U32(30199, "Operation.RmgTms", "Wartezeit bis Einspeisung", "Dauer", "s")
    )
    wr.add_register(U32(30201, "Operation.Health", "Zustand", "TAGLIST", ""))
    wr.add_register(
        U32(30203, "Operation.HealthStt.Ok", "Nennleistung im Zustand Ok", "FIX0", "W")
    )
    wr.add_register(
        U32(
            30205,
            "Operation.HealthStt.Wrn",
            "Nennleistung im Zustand Warnung",
            "FIX0",
            "W",
        )
    )
    wr.add_register(
        U32(
            30207,
            "Operation.HealthStt.Alm",
            "Nennleistung im Zustand Fehler",
            "FIX0",
            "W",
        )
    )
    wr.add_register(
        U32(30211, "Operation.Evt.Prio", "Empfohlene Aktion", "TAGLIST", "")
    )
    wr.add_register(U32(30213, "Operation.Evt.Msg", "Meldung", "TAGLIST", ""))
    wr.add_register(
        U32(30215, "Operation.Evt.Dsc", "Fehlerbehebungsmaßnahme", "TAGLIST", "")
    )
    wr.add_register(
        U32(30217, "Operation.GriSwStt", "Netzrelais/-schütz", "TAGLIST", "")
    )
    wr.add_register(
        U32(30219, "Operation.DrtStt", "Leistungsreduzierung", "TAGLIST", "")
    )
    wr.add_register(
        U32(30225, "Isolation.LeakRis", "Isolationswiderstand", "FIX0", "Ohm")
    )
    wr.add_register(
        U32(30231, "Inverter.WLim", "Maximale Gerätewirkleistung", "FIX0", "W")
    )
    wr.add_register(
        U32(30233, "Inverter.WMax", "Eingestellte Wirkleistungsgrenze", "FIX0", "W")
    )
    wr.add_register(
        U32(
            30247,
            "Operation.Evt.EvtNo",
            "Aktuelle Ereignisnummer für Hersteller",
            "FIX0",
            "",
        )
    )
    wr.add_register(U64(30513, "Metering.TotWhOut", "Gesamtertrag", "FIX0", "Wh"))
    wr.add_register(U64(30517, "Metering.DyWhOut", "Tagesertrag", "FIX0", "Wh"))
    wr.add_register(U64(30521, "Metering.TotOpTms", "Betriebszeit", "Dauer", "s"))
    wr.add_register(U64(30525, "Metering.TotFeedTms", "Einspeisezeit", "Dauer", "s"))
    wr.add_register(U32(30529, "Metering.TotWhOut", "Gesamtertrag", "FIX0", "Wh"))
    wr.add_register(U32(30531, "Metering.TotWhOut", "Gesamtertrag", "FIX0", "kWh"))
    wr.add_register(U32(30533, "Metering.TotWhOut", "Gesamtertrag", "FIX0", "MWh"))
    wr.add_register(U32(30535, "Metering.DyWhOut", "Tagesertrag", "FIX0", "Wh"))
    wr.add_register(U32(30537, "Metering.DyWhOut", "Tagesertrag", "FIX0", "kWh"))
    wr.add_register(U32(30539, "Metering.DyWhOut", "Tagesertrag", "FIX0", "MWh"))
    wr.add_register(U32(30541, "Metering.TotOpTms", "Betriebszeit", "Dauer", "s"))
    wr.add_register(U32(30543, "Metering.TotFeedTms", "Einspeisezeit", "Dauer", "s"))
    wr.add_register(
        U32(30559, "Operation.EvtCntUsr", "Anzahl Ereignisse für Benutzer", "FIX0", "")
    )
    wr.add_register(
        U32(
            30561,
            "Operation.EvtCntIstl",
            "Anzahl Ereignisse für Installateur",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U32(30563, "Operation.EvtCntSvc", "Anzahl Ereignisse für Service", "FIX0", "")
    )
    wr.add_register(
        U32(
            30583,
            "Metering.GridMs.TotWhOut",
            "Zählerstand Netzeinspeise-Zähler",
            "FIX0",
            "Wh",
        )
    )
    wr.add_register(
        U32(30599, "Operation.GriSwCnt", "Anzahl Netzzuschaltungen", "FIX0", "")
    )
    wr.add_register(S32(30769, "DcMs.Amp.MPPT1", "DC Strom Eingang MPPT1", "FIX3", "A"))
    wr.add_register(
        S32(30771, "DcMs.Vol.MPPT1", "DC Spannung Eingang  MPPT1", "FIX2", "V")
    )
    wr.add_register(
        S32(30773, "DcMs.Watt.MPPT1", "DC Leistung Eingang  MPPT1", "FIX0", "W")
    )
    wr.add_register(S32(30775, "GridMs.TotW", "Leistung", "FIX0", "W"))
    wr.add_register(S32(30777, "GridMs.W.phsA", "Leistung L1", "FIX0", "W"))
    wr.add_register(S32(30779, "GridMs.W.phsB", "Leistung L2", "FIX0", "W"))
    wr.add_register(S32(30781, "GridMs.W.phsC", "Leistung L3", "FIX0", "W"))
    wr.add_register(U32(30783, "GridMs.PhV.phsA", "Netzspannung Phase L1", "FIX2", "V"))
    wr.add_register(U32(30785, "GridMs.PhV.phsB", "Netzspannung Phase L2", "FIX2", "V"))
    wr.add_register(U32(30787, "GridMs.PhV.phsC", "Netzspannung Phase L3", "FIX2", "V"))
    wr.add_register(U32(30795, "GridMs.TotA", "Netzstrom", "FIX3", "A"))
    wr.add_register(U32(30803, "GridMs.Hz", "Netzfrequenz", "FIX2", "Hz"))
    wr.add_register(S32(30805, "GridMs.TotVAr", "Blindleistung", "FIX0", "VAr"))
    wr.add_register(S32(30807, "GridMs.VAr.phsA", "Blindleistung L1", "FIX0", "VAr"))
    wr.add_register(S32(30809, "GridMs.VAr.phsB", "Blindleistung L2", "FIX0", "VAr"))
    wr.add_register(S32(30811, "GridMs.VAr.phsC", "Blindleistung L3", "FIX0", "VAr"))
    wr.add_register(S32(30813, "GridMs.TotVA", "Scheinleistung", "FIX0", "VA"))
    wr.add_register(S32(30815, "GridMs.VA.phsA", "Scheinleistung L1", "FIX0", "VA"))
    wr.add_register(S32(30817, "GridMs.VA.phsB", "Scheinleistung L2", "FIX0", "VA"))
    wr.add_register(S32(30819, "GridMs.VA.phsC", "Scheinleistung L3", "FIX0", "VA"))
    wr.add_register(
        U32(
            30825,
            "Inverter.VArModCfg.VArMod",
            "Betriebsart der statischen Spannungshaltung, Konfiguration der statischen Spannungshaltung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            30829,
            "Inverter.VArModCfg.VArCnstCfg.VArNom",
            "Blindleistungssollwert in %",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        S32(
            30831,
            "Inverter.VArModCfg.PFCnstCfg.PF",
            "Sollwert des cos Phi, Konfiguration des cos Phi, direkte Vorgabe",
            "FIX2",
            "",
        )
    )
    wr.add_register(
        U32(
            30833,
            "Inverter.VArModCfg.PFCnstCfg.PFExt",
            "Erregungsart des cos Phi, Konfiguration des cos Phi, direkte Vorgabe",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            30835,
            "Inverter.WModCfg.WMod",
            "Betriebsart des Einspeisemanagements",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            30837,
            "Inverter.WModCfg.WCnstCfg.W",
            "Wirkleistungsbegrenzung in W",
            "FIX0",
            "W",
        )
    )
    wr.add_register(
        U32(
            30839,
            "Inverter.WModCfg.WCnstCfg.WNom",
            "Wirkleistungsbegrenzung in %",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(30881, "Operation.PvGriConn", "Netzanbindung der PV-Anlage ", "TAGLIST", "")
    )
    wr.add_register(
        U32(
            30919,
            "Inverter.VArModCfg.VArModDmd",
            "Betriebsart der statischen Spannungshaltung bei Q on Demand, Konfiguration der statischen Spannungshaltung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            30925,
            "Spdwr.ComSocA.ConnSpd",
            "Verbindungsgeschwindigkeit von SMACOM A",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(30927, "Spdwr.ComSocA.DpxMode", "Duplexmodus von SMACOM A", "TAGLIST", "")
    )
    wr.add_register(
        U32(
            30929,
            "Spdwr.ComSocA.Stt",
            "Speedwire-Verbindungsstatus von SMACOM A",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            30931,
            "Spdwr.ComSocB.ConnSpd",
            "Verbindungsgeschwindigkeit von SMACOM B",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(30933, "Spdwr.ComSocB.DpxMode", "Duplexmodus von SMACOM B", "TAGLIST", "")
    )
    wr.add_register(
        U32(
            30935,
            "Spdwr.ComSocB.Stt",
            "Speedwire-Verbindungsstatus von SMACOM B",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(U32(30949, "GridMs.TotPFPrc", "Verschiebungsfaktor", "FIX3", ""))
    wr.add_register(S32(30953, "Coolsys.Cab.TmpVal", "Innentemperatur", "TEMP", "°C"))
    wr.add_register(S32(30957, "DcMs.Amp.MPPT2", "DC Strom Eingang MPPT2", "FIX3", "A"))
    wr.add_register(
        S32(30959, "DcMs.Vol.MPPT2", "DC Spannung Eingang MPPT2", "FIX2", "V")
    )
    wr.add_register(
        S32(30961, "DcMs.Watt.MPPT2", "DC Leistung Eingang  MPPT2", "FIX0", "W")
    )
    wr.add_register(S32(30975, "Inverter.DclVol", "Zwischenkreisspannung", "FIX2", "V"))
    wr.add_register(S32(30977, "GridMs.A.phsA", "Netzstrom Phase L1", "FIX3", "A"))
    wr.add_register(S32(30979, "GridMs.A.phsB", "Netzstrom Phase L2", "FIX3", "A"))
    wr.add_register(S32(30981, "GridMs.A.phsC", "Netzstrom Phase L3", "FIX3", "A"))
    wr.add_register(STR32(31017, "Spdwr.ActlIp", "-", 8))
    wr.add_register(STR32(31025, "Spdwr.ActlSnetMsk", "-", 8))
    wr.add_register(STR32(31033, "Spdwr.ActlGwIp", "-", 8))
    wr.add_register(STR32(31041, "Spdwr.ActlDnsSrvIp", "-", 8))
    wr.add_register(
        U32(31085, "Operation.HealthStt.Ok", "Nennleistung im Zustand Ok", "FIX0", "W")
    )
    wr.add_register(
        S32(
            31159,
            "Operation.Dmd.VArCtl",
            "Aktuelle Vorgabe Blindleistung Q",
            "FIX0",
            "VAr",
        )
    )
    wr.add_register(S32(31247, "Isolation.FltA", "Fehlerstrom", "FIX3", "A"))
    wr.add_register(S32(31793, "DcMs.Amp__1", "DC Strom Eingang ?1", "FIX3", "A"))
    wr.add_register(S32(31795, "DcMs.Am__2", "DC Strom Eingang ?2", "FIX3", "A"))
    wr.add_register(S32(34113, "Coolsys.Cab.TmpVal", "Innentemperatur", "TEMP", "°C"))
    wr.add_register(
        U64(35377, "Operation.EvtCntUsr", "Anzahl Ereignisse für Benutzer", "FIX0", "")
    )
    wr.add_register(
        U64(
            35381,
            "Operation.EvtCntIstl",
            "Anzahl Ereignisse für Installateur",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U64(35385, "Operation.EvtCntSvc", "Anzahl Ereignisse für Service", "FIX0", "")
    )
    wr.add_register(U32(40009, "Operation.OpMod", "Betriebszustand", "TAGLIST", ""))
    wr.add_register(
        U32(40013, "CntrySettings.Lang", "Sprache der Oberfläche", "TAGLIST", "")
    )
    wr.add_register(U32(40029, "Operation.OpStt", "Betriebsstatus", "TAGLIST", ""))
    wr.add_register(
        U32(
            40063,
            "Nameplate.CmpMain.SwRev",
            "Firmware-Version des Hauptprozessors",
            "FW",
            "",
        )
    )
    wr.add_register(
        U32(
            40065,
            "Nameplate.CmpSigProc.SwRev",
            "Firmware-Version der Logikkomponente",
            "FW",
            "",
        )
    )
    wr.add_register(U32(40067, "Nameplate.SerNum", "Seriennummer", "RAW", ""))
    wr.add_register(
        U32(
            40095,
            "GridGuard.Cntry.VolCtl.Max",
            "Spannungsüberwachung obere Maximalschwelle",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(40109, "GridGuard.Cntry", "Eingestellte Ländernorm", "TAGLIST", "")
    )
    wr.add_register(
        U32(40133, "GridGuard.Cntry.VRtg", "Netz-Nennspannung", "FIX0", "V")
    )
    wr.add_register(U32(40135, "GridGuard.Cntry.HzRtg", "Nennfrequenz", "FIX2", "Hz"))
    wr.add_register(STR32(40155, "Nameplate.MacId", "-", 2))
    wr.add_register(
        U32(
            40157,
            "Spdwr.AutoCfgIsOn",
            "Automatische Speedwire-Konfiguration eingeschaltet",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(STR32(40159, "Spdwr.Ip", "-", 8))
    wr.add_register(STR32(40167, "Spdwr.SnetMsk", "-", 8))
    wr.add_register(STR32(40175, "Spdwr.GwIp", "-", 8))
    wr.add_register(
        U32(40185, "Inverter.VALim", "Maximale Gerätescheinleistung", "FIX0", "VA")
    )
    wr.add_register(
        U32(40195, "Inverter.VAMax", "Eingestellte Scheinleistungsgrenze", "FIX0", "VA")
    )
    wr.add_register(
        U32(
            40200,
            "Inverter.VArModCfg.VArMod",
            "Betriebsart der statischen Spannungshaltung, Konfiguration der statischen Spannungshaltung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            40204,
            "Inverter.VArModCfg.VArCnstCfg.VArNom",
            "Blindleistungssollwert in %",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        S32(
            40206,
            "Inverter.VArModCfg.PFCnstCfg.PF",
            "Sollwert des cos Phi, Konfiguration des cos Phi, direkte Vorgabe",
            "FIX2",
            "",
        )
    )
    wr.add_register(
        U32(
            40208,
            "Inverter.VArModCfg.PFCnstCfg.PFExt",
            "Erregungsart des cos Phi, Konfiguration des cos Phi, direkte Vorgabe",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40210,
            "Inverter.WModCfg.WMod",
            "Betriebsart des Einspeisemanagements",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40212,
            "Inverter.WModCfg.WCnstCfg.W",
            "Wirkleistungsbegrenzung in W",
            "FIX0",
            "W",
        )
    )
    wr.add_register(
        U32(
            40214,
            "Inverter.WModCfg.WCnstCfg.WNom",
            "Wirkleistungsbegrenzung in %",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40216,
            "Inverter.WCtlHzModCfg.WCtlHzMod",
            "Betriebsart der Wirkleistungsreduktion bei Überfrequenz P(f)",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40218,
            "Inverter.WCtlHzModCfg.WCtlHzCfg.HzStr",
            "Abstand der Startfrequenz zur Netzfrequenz, Konfiguration des linearen Gradienten der Momentanleistung",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40220,
            "Inverter.WCtlHzModCfg.WCtlHzCfg.HzStop",
            "Abstand der Rücksetzfrequenz zur Netzfrequenz, Konfiguration des linearen Gradienten der Momentanleistung",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40222,
            "Inverter.VArModCfg.PFCtlWCfg.PFStr",
            "cos Phi des Startpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "FIX2",
            "",
        )
    )
    wr.add_register(
        U32(
            40224,
            "Inverter.VArModCfg.PFCtlWCfg.PFExtStr",
            "Erregungsart des Startpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40226,
            "Inverter.VArModCfg.PFCtlWCfg.PFStop",
            "cos Phi des Endpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "FIX2",
            "",
        )
    )
    wr.add_register(
        U32(
            40228,
            "Inverter.VArModCfg.PFCtlWCfg.PFExtStop",
            "Erregungsart des Endpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40230,
            "Inverter.VArModCfg.PFCtlWCfg.WNomStr",
            "Wirkleistung des Startpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40232,
            "Inverter.VArModCfg.PFCtlWCfg.WNomStop",
            "Wirkleistung des Endpunktes, Konfiguration der cos Phi(P)-Kennlinie",
            "FIX0",
            "%",
        )
    )
    wr.add_register(U32(40234, "Inverter.WGra", "Wirkleistungsgradient", "FIX0", "%"))
    wr.add_register(
        U32(
            40238,
            "Inverter.WCtlHzModCfg.WCtlHzCfg.WGra",
            "Wirkleistungsgradient, Konfiguration des linearen Gradienten der Momentanleistung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40240,
            "Inverter.WCtlHzModCfg.WCtlHzCfg.HystEna",
            "Aktivierung der Schleppzeigerfunktion, Konfiguration des linearen Gradienten der Momentanleistung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40242,
            "Inverter.WCtlHzModCfg.WCtlHzCfg.HzStopWGra",
            "Wirkleistungsgradient nach Rücksetzfrequenz, Konfiguration des linearen Gradienten der Momentanleistung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40244,
            "Inverter.DGSModCfg.DGSFlCfg.ArGraMod",
            "Blindstromstatik, Konfiguration der vollständigen dynamischen Netzstützung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40250,
            "Inverter.DGSModCfg.DGSMod",
            "Betriebsart der dynamischen Netzstützung, Konfiguration der dynamischen Netzstützung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            40252,
            "Inverter.DGSModCfg.DGSFlCfg.DbVolNomMin",
            "Untergrenze Spannungstotband, Konfiguration der vollständigen dynamischen Netzstützung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40254,
            "Inverter.DGSModCfg.DGSFlCfg.DbVolNomMax",
            "Obergrenze Spannungstotband, Konfiguration der vollständigen dynamischen Netzstützung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40256,
            "Inverter.DGSModCfg.PwrCirInopVolNom",
            "PWM-Sperrspannung, Konfiguration der dynamischen Netzstützung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        U32(
            40258,
            "Inverter.DGSModCfg.PwrCirInopTms",
            "PWM-Sperrverzögerung, Konfiguration der dynamischen Netzstützung",
            "FIX2",
            "s",
        )
    )
    wr.add_register(
        U32(
            40260,
            "Inverter.WCtlVolModCfg.CrvNum",
            "Kennliniennummer, Konfiguration der Wirkleistungs-/Spannungskennlinie P(U)",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U32(
            40428,
            "GridGuard.Cntry.FrqCtl.hhLim",
            "Frequenzüberwachung mittlere Maximalschwelle",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40430,
            "GridGuard.Cntry.FrqCtl.hhLimTmms",
            "Frequenzüberwachung mittlere Maximalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40432,
            "GridGuard.Cntry.FrqCtl.hLim",
            "Frequenzüberwachung untere Maximalschwelle",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40434,
            "GridGuard.Cntry.FrqCtl.hLimTmms",
            "Frequenzüberwachung untere Maximalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40436,
            "GridGuard.Cntry.FrqCtl.lLim",
            "Frequenzüberwachung obere Minimalschwelle",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40438,
            "GridGuard.Cntry.FrqCtl.lLimTmms",
            "Frequenzüberwachung obere Minimalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40440,
            "GridGuard.Cntry.FrqCtl.llLim",
            "Frequenzüberwachung mittlere Minimalschwelle",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            40442,
            "GridGuard.Cntry.FrqCtl.llLimTmms",
            "Frequenzüberwachung mittlere Minimalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40446,
            "GridGuard.Cntry.VolCtl.MaxTmms",
            "Spannungsüberwachung obere Maximalschwelle Auslösezeit",
            "FIX3",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40448,
            "GridGuard.Cntry.VolCtl.hhLim",
            "Spannungsüberwachung mittlere Maximalschwelle",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            40450,
            "GridGuard.Cntry.VolCtl.hhLimTmms",
            "Spannungsüberwachung mittlere Maximalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40452,
            "GridGuard.Cntry.VolCtl.hLim",
            "Spannungsüberwachung untere Maximalschwelle",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            40456,
            "GridGuard.Cntry.VolCtl.hLimTmms",
            "Spannungsüberwachung untere Maximalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40458,
            "GridGuard.Cntry.VolCtl.lLim",
            "Spannungsüberwachung obere Minimalschwelle",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            40462,
            "GridGuard.Cntry.VolCtl.lLimTmms",
            "Spannungsüberwachung obere Minimalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40464,
            "GridGuard.Cntry.VolCtl.llLim",
            "Spannungsüberwachung mittlere Minimalschwelle",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            40466,
            "GridGuard.Cntry.VolCtl.llLimTmms",
            "Spannungsüberwachung mittlere Minimalschwelle Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            40472,
            "Inverter.PlntCtl.VRef",
            "Referenzspannung, Anlagensteuerung",
            "FIX0",
            "V",
        )
    )
    wr.add_register(
        S32(
            40474,
            "Inverter.PlntCtl.VRefOfs",
            "Referenzkorrekturspannung, Anlagensteuerung",
            "FIX0",
            "V",
        )
    )
    wr.add_register(
        U32(40482, "Inverter.VArGra", "Blindleistungsgradient", "FIX0", "%")
    )
    wr.add_register(
        U32(
            40484,
            "Inverter.WGraEna",
            "Aktivierung des Wirkleistungsgradienten",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            40490,
            "Inverter.VArModCfg.VArCtlVolCfg.VArGraNom",
            "Blindleistungsgradient, Konfiguration der Blindleistungs-/Spannungskennlinie Q(U)",
            "FIX1",
            "%",
        )
    )
    wr.add_register(STR32(40497, "Nameplate.MacId", "-", 16))
    wr.add_register(STR32(40513, "Spdwr.DnsSrvIp", "-", 8))
    wr.add_register(
        U32(
            40575,
            "MltFncSw.OpMode",
            "Betriebsart des Multifunktionsrelais",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(STR32(40631, "Nameplate.Location", "-", 16))
    wr.add_register(U32(40789, "Nameplate.ComRev", "Kommunikationsversion", "REV", ""))
    wr.add_register(
        U32(
            40809,
            "Nameplate.CmpSigProc.Rev",
            "Umbaustand der Logikkomponente",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U32(40915, "Inverter.WMax", "Eingestellte Wirkleistungsgrenze", "FIX0", "W")
    )
    wr.add_register(
        U32(
            40997,
            "Inverter.DGSModCfg.HystVolNom",
            "Hysteresespannung, Konfiguration der dynamischen Netzstützung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(
        S32(
            41001,
            "Inverter.VArLimQ1",
            "Maximal erreichbare Blindleistung Quadrant 1",
            "FIX0",
            "VAr",
        )
    )
    wr.add_register(
        S32(
            41007,
            "Inverter.VArLimQ4",
            "Maximal erreichbare Blindleistung Quadrant 4",
            "FIX0",
            "VAr",
        )
    )
    wr.add_register(
        S32(
            41009,
            "Inverter.PFLimQ1",
            "Minimal erreichbarer cos(Phi) Quadrant 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41015,
            "Inverter.PFLimQ4",
            "Minimal erreichbarer cos(Phi) Quadrant 4",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        U32(
            41017,
            "Inverter.UtilCrvCfg.Crv.CrvTms",
            "Einstellzeit des Kennlinienarbeitspunktes, Konf. der Netzintegrationskennlinie 1",
            "FIX1",
            "s",
        )
    )
    wr.add_register(
        U32(
            41019,
            "Inverter.UtilCrvCfg.Crv.RmpDec",
            "Absenkungsrampe, Konfiguration der Netzintegrationskennlinie 1",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        U32(
            41021,
            "Inverter.UtilCrvCfg.Crv.RmpInc",
            "Steigerungsrampe, Konfiguration der Netzintegrationskennlinie 1",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        U32(
            41023,
            "Inverter.UtilCrvCfg.Crv.NumPt",
            "Anzahl zu verwendender Punkte, Konfiguration der Netzintegrationskennlinie 1",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U32(
            41025,
            "Inverter.UtilCrvCfg.Crv.XRef",
            "X-Achsen-Referenz, Konf. der Netzintegrationskennlinie 1",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            41027,
            "Inverter.UtilCrvCfg.Crv.YRef",
            "Y-Achsen-Referenz, Konf. der Netzintegrationskennlinie 1",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            41029,
            "Inverter.UtilCrvCfg.Crv.XVal1",
            "X-Wert 1, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41031,
            "Inverter.UtilCrvCfg.Crv.YVal1",
            "Y-Wert 1, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41033,
            "Inverter.UtilCrvCfg.Crv.XVal2",
            "X-Wert 2, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41035,
            "Inverter.UtilCrvCfg.Crv.YVal2",
            "Y-Wert 2, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41037,
            "Inverter.UtilCrvCfg.Crv.XVal3",
            "X-Wert 3, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41039,
            "Inverter.UtilCrvCfg.Crv.YVal3",
            "Y-Wert 3, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41041,
            "Inverter.UtilCrvCfg.Crv.XVal4",
            "X-Wert 4, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41043,
            "Inverter.UtilCrvCfg.Crv.YVal4",
            "Y-Wert 4, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41045,
            "Inverter.UtilCrvCfg.Crv.XVal5",
            "X-Wert 5, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41047,
            "Inverter.UtilCrvCfg.Crv.YVal5",
            "Y-Wert 5, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41049,
            "Inverter.UtilCrvCfg.Crv.XVal6",
            "X-Wert 6, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41051,
            "Inverter.UtilCrvCfg.Crv.YVal6",
            "Y-Wert 6, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41053,
            "Inverter.UtilCrvCfg.Crv.XVal7",
            "X-Wert 7, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41055,
            "Inverter.UtilCrvCfg.Crv.YVal7",
            "Y-Wert 7, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41057,
            "Inverter.UtilCrvCfg.Crv.XVal8",
            "X-Wert 8, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41059,
            "Inverter.UtilCrvCfg.Crv.YVal8",
            "Y-Wert 8, Konfiguration der Netzintegrationskennlinie 1",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        U32(
            41065,
            "Inverter.UtilCrvCfg.Crv2.CrvTms",
            "Einstellzeit des Kennlinienarbeitspunktes, Konfiguration der Netzintegrationskennlinie 2",
            "FIX1",
            "s",
        )
    )
    wr.add_register(
        U32(
            41067,
            "Inverter.UtilCrvCfg.Crv2.RmpDec",
            "Absenkungsrampe, Konfiguration der Netzintegrationskennlinie 2",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        U32(
            41069,
            "Inverter.UtilCrvCfg.Crv2.RmpInc",
            "Steigerungsrampe, Konfiguration der Netzintegrationskennlinie 2",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        U32(
            41071,
            "Inverter.UtilCrvCfg.Crv2.NumPt",
            "Anzahl zu verwendender Punkte, Konfiguration der Netzintegrationskennlinie 2",
            "FIX0",
            "",
        )
    )
    wr.add_register(
        U32(
            41073,
            "Inverter.UtilCrvCfg.Crv2.XRef",
            "Eingangseinheit, Konfiguration der Netzintegrationskennlinie 2",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            41075,
            "Inverter.UtilCrvCfg.Crv2.YRef",
            "Ausgangsreferenz, Konfiguration der Netzintegrationskennlinie 2",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            41077,
            "Inverter.UtilCrvCfg.Crv2.XVal1",
            "X-Wert 1, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41079,
            "Inverter.UtilCrvCfg.Crv2.YVal1",
            "Y-Wert 1, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41081,
            "Inverter.UtilCrvCfg.Crv2.XVal2",
            "X-Wert 2, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41083,
            "Inverter.UtilCrvCfg.Crv2.YVal2",
            "Y-Wert 2, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41085,
            "Inverter.UtilCrvCfg.Crv2.XVal3",
            "X-Wert 3, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41087,
            "Inverter.UtilCrvCfg.Crv2.YVal3",
            "Y-Wert 3, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41089,
            "Inverter.UtilCrvCfg.Crv2.XVal4",
            "X-Wert 4, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41091,
            "Inverter.UtilCrvCfg.Crv2.YVal4",
            "Y-Wert 4, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41093,
            "Inverter.UtilCrvCfg.Crv2.XVal5",
            "X-Wert 5, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41095,
            "Inverter.UtilCrvCfg.Crv2.YVal5",
            "Y-Wert 5, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41097,
            "Inverter.UtilCrvCfg.Crv2.XVal6",
            "X-Wert 6, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41099,
            "Inverter.UtilCrvCfg.Crv2.YVal6",
            "Y-Wert 6, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41101,
            "Inverter.UtilCrvCfg.Crv2.XVal7",
            "X-Wert 7, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41103,
            "Inverter.UtilCrvCfg.Crv2.YVal7",
            "Y-Wert 7, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41105,
            "Inverter.UtilCrvCfg.Crv2.XVal8",
            "X-Wert 8, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        S32(
            41107,
            "Inverter.UtilCrvCfg.Crv2.YVal8",
            "Y-Wert 8, Konfiguration der Netzintegrationskennlinie 2",
            "FIX3",
            "",
        )
    )
    wr.add_register(
        U32(
            41111,
            "GridGuard.Cntry.VolCtl.MinEff",
            "Spannungsüberwachung untere Minimalschwelle als Effektivwert",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            41113,
            "GridGuard.Cntry.VolCtl.MinEffTmms",
            "Spannungsüberwachung untere Minimalschwelle als Effektivwert Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(
            41115,
            "GridGuard.Cntry.VolCtl.MaxEff",
            "Spannungsüberwachung obere Maximalschwelle als Effektivwert",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            41117,
            "GridGuard.Cntry.VolCtl.MaxEffTmms",
            "Spannungsüberwachung obere Maximalschwelle als Effektivwert Auslösezeit",
            "FIX0",
            "ms",
        )
    )
    wr.add_register(
        U32(41121, "GridGuard.CntrySet", "Setze Ländernorm", "FUNKTION_SEC", "")
    )
    wr.add_register(
        U32(
            41123,
            "GridGuard.Cntry.VolCtl.ReconMin",
            "Min. Spannung zur Wiederzuschaltung",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            41125,
            "GridGuard.Cntry.VolCtl.ReconMax",
            "Max. Spannung zur Wiederzuschaltung",
            "FIX2",
            "V",
        )
    )
    wr.add_register(
        U32(
            41127,
            "GridGuard.Cntry.FrqCtl.ReconMin",
            "Untere Frequenz für Wiederzuschaltung",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(
            41129,
            "GridGuard.Cntry.FrqCtl.ReconMax",
            "Obere Frequenz für Wiederzuschaltung",
            "FIX2",
            "Hz",
        )
    )
    wr.add_register(
        U32(41131, "DcCfg.StrVol", "minimale Spannung Eingang ", "FIX2", "V")
    )
    wr.add_register(
        U32(41133, "DcCfg.StrVol", "minimale Spannung Eingang ", "FIX2", "V")
    )
    wr.add_register(
        U32(41155, "DcCfg.StrTms", "Startverzögerung Eingang ", "FIX0", "s")
    )
    wr.add_register(
        U32(41157, "DcCfg.StrTms", "Startverzögerung Eingang ", "FIX0", "s")
    )
    wr.add_register(
        U32(
            41169,
            "GridGuard.Cntry.LeakRisMin",
            "Minimaler Isolationswiderstand",
            "FIX0",
            "Ohm",
        )
    )
    wr.add_register(
        U32(41171, "Metering.TotkWhOutSet", "Setze Gesamtertrag", "FIX0", "kWh")
    )
    wr.add_register(
        U32(
            41173,
            "Metering.TotOpTmhSet",
            "Setze Gesamte Betriebszeit am Netzanschlusspunkt",
            "Dauer",
            "h",
        )
    )
    wr.add_register(
        U32(
            41193,
            "Inverter.CtlComCfg.WCtlCom.CtlComMssMod",
            "Betriebsart für ausbleibende Wirkleistungsbegrenzung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            41195,
            "Inverter.CtlComCfg.WCtlCom.TmsOut",
            "Timeout für ausbleibende Wirkleistungsbegrenzung",
            "Dauer",
            "s",
        )
    )
    wr.add_register(
        U32(
            41197,
            "Inverter.CtlComCfg.WCtlCom.FlbWNom",
            "Fallback Wirkleistungsbegrenzung P in % von WMax für ausbleibende Wirkleistungsbegrenzung",
            "FIX2",
            "%",
        )
    )
    wr.add_register(
        U32(
            41219,
            "Inverter.CtlComCfg.VArCtlCom.CtlComMssMod",
            "Betriebsart für ausbleibende Blindleistungsregelung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            41221,
            "Inverter.CtlComCfg.VArCtlCom.TmsOut",
            "Timeout für ausbleibende Blindleistungsregelung",
            "Dauer",
            "s",
        )
    )
    wr.add_register(
        S32(
            41223,
            "Inverter.CtlComCfg.VArCtlCom.FlbVArNom",
            "Fallback Blindleistung Q in % von WMax für ausbleibende Blindleistungsregelung",
            "FIX2",
            "%",
        )
    )
    wr.add_register(
        U32(
            41225,
            "Inverter.CtlComCfg.PFCtlCom.CtlComMssMod",
            "Betriebsart für ausbleibende cos Phi-Vorgabe",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        U32(
            41227,
            "Inverter.CtlComCfg.PFCtlCom.TmsOut",
            "Timeout für ausbleibende cos Phi-Vorgabe",
            "Dauer",
            "s",
        )
    )
    wr.add_register(
        S32(
            41229,
            "Inverter.CtlComCfg.PFCtlCom.FlbPF",
            "Fallback cos Phi für ausbleibende cos Phi-Vorgabe",
            "FIX4",
            "",
        )
    )
    wr.add_register(
        U64(42109, "Modbus.UnitID", "Unit ID des Wechselrichters", "RAW", "")
    )
    wr.add_register(U32(43090, "SMA.GridGuard.Code", "SMA Grid Guard-Code", "RAW", ""))


# Registers to Write Values ... writing not yet implemented .. you can't read this
def add_tripower_writeonly_register(wr: Modbus):
    wr.add_register(
        S16(
            40015,
            "Inverter.VArModCfg.VArCtlComCfg.VArNom",
            "Normierte Blindleistungsbegrenzung durch Anlagensteuerung",
            "FIX1",
            "%",
        )
    )
    wr.add_register(
        S16(
            40016,
            "Inverter.WModCfg.WCtlComCfg.WNom",
            "Normierte Wirkleistungsbegrenzung durch Anlagensteuerung",
            "FIX0",
            "%",
        )
    )
    wr.add_register(U32(40018, "Inverter.FstStop", "Schnellabschaltung", "TAGLIST", ""))
    wr.add_register(
        S16(
            40022,
            "Inverter.VArModCfg.VArCtlComCfg.VArNomPrc",
            "Normierte Blindleistungsbegrenzung durch Anlagensteuerung",
            "FIX2",
            "%",
        )
    )
    wr.add_register(
        S16(
            40023,
            "Inverter.WModCfg.WCtlComCfg.WNomPrc",
            "Normierte Wirkleistungsbegrenzung durch Anlagensteuerung",
            "FIX2",
            "%",
        )
    )
    wr.add_register(
        U16(
            40024,
            "Inverter.VArModCfg.PFCtlComCfg.PF",
            "Verschiebungsfaktor durch Anlagensteuerung",
            "FIX4",
            "",
        )
    )
    wr.add_register(
        U32(
            40025,
            "Inverter.VArModCfg.PFCtlComCfg.PFExt",
            "Erregungsart durch Anlagensteuerung",
            "TAGLIST",
            "",
        )
    )
    wr.add_register(
        S32(
            40999,
            "Inverter.VArModCfg.PFCtlComCfg.PFEEI",
            "Sollwert cos(Phi) gemäß EEI-Konvention",
            "FIX4",
            "",
        )
    )


"""