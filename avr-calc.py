# **Definition der anzuwendenden AVR Bedingungen**

# Aktuelle Tarifstruktur mit den korrekten Entgelten für Regionalkommission West
tarifstruktur = {
    "I": {1: 5288.32, 2: 5588.11, 3: 5802.19, 4: 6173.28, 5: 6615.77, 6: 6797.77},
    "II": {1: 6979.74, 2: 7564.95, 3: 8078.81, 4: 8378.57, 5: 8671.15, 6: 8963.74},
    "III": {1: 8742.54, 2: 9256.37, 3: 9991.49},
    "IV": {1: 10284.04, 2: 11019.20},
}

# Korrekte Zeitzuschläge in Prozent des Stundenlohns des auf eine Stunde anfallenden Anteils des Tabellenentgelts der Stufe 3 der jeweiligen Entgeltgruppe
zuschläge = {
    "nacht": 0.15,  # 15% für Nachtarbeit
    "sonntag": 0.25,  # 25% für Sonntagsarbeit
    "feiertag_mit_fza": 0.35,  # 35% für Feiertagsarbeit mit FZA
    "feiertag_ohne_fza": 1.35 # 135% für Feiertagsarbeit ohne FZA
}

# Bereitschaftsdienstzeiten in Stunden (Stufe III - vollständig vergütet)
bd_zeiten = {
    "werktag": 20.5,
    "freitag": 21.75,
    "samstag": 24,
    "sonntag": 22.75,
}

# Bereitschaftsdienstzeiten in Stunden (Stufe III - vollständig vergütet)
bd_zeit_bereitschaft = {
    "werktag": 20.5,
    "freitag": 21.75,
    "samstag": 24,
    "sonntag": 22.75,
}

# Zeiten der Regelarbeitszeit bei Ableistung von BD an bestimmtem Tag
bd_zeit_regelarbeit = {
    "werktag": 20.5,
    "freitag": 21.75,
    "samstag": 24,
    "sonntag": 22.75,
}

# Stundenlöhne für den Bereitschaftsdienst gemäß AVR §8 Abs. 2
stundenlohn_bd = {
    "I": {1: 34.07, 2: 34.07, 3: 35.36, 4: 35.36, 5: 36.65, 6: 36.65},
    "II": {1: 40.51, 2: 40.51, 3: 41.80, 4: 41.80, 5: 43.11, 6: 43.11},
    "III": {1: 43.74, 2: 43.74, 3: 45.02},
    "IV": {1: 47.60, 2: 47.60},
}

# Beispielhafte Benutzereingaben, hier interaktive Abfrage implementieren
eingaben = {
    "tarifgruppe": "II",
    "stufe": 3,
    "arbeitszeit_prozent": 100,  # 100% Stelle
    "bd_anzahl": {
        "werktag": 2,
        "freitag": 2,
        "samstag": 1,
        "sonntag": 1,
    },
    "einsätze_rettungsdienst": 3  # Beispiel: 3 Einsätze im Monat
}

# Zusätzliche Variable: Einsatzzuschlag für Rettungsdienst (pro Einsatz)
einsatzzuschlag = 31.38  # Pro Einsatz

# Berechnung der Grundvergütung
grundgehalt = tarifstruktur[eingaben["tarifgruppe"]][eingaben["stufe"]]
if eingaben["arbeitszeit_prozent"] < 100:
    grundgehalt *= eingaben["arbeitszeit_prozent"] / 100

# Berechnung der Bereitschaftsdienstvergütung (volle Vergütung aller BD-Stunden)
bd_gesamtstunden = sum(
    eingaben["bd_anzahl"][tag] * bd_zeiten[tag] for tag in bd_zeiten
)

# Abzug für den entfallenden Arbeitstag nach BD (bei Vollzeit 8h, sonst anteilig)
arbeitstag_abzug = 8 * (eingaben["arbeitszeit_prozent"] / 100)
bd_abzugsstunden = (
    eingaben["bd_anzahl"]["werktag"] + eingaben["bd_anzahl"]["sonntag"]
) * arbeitstag_abzug

# Tatsächlich vergütete BD-Zeit (volle Vergütung)
bd_relevante_stunden = bd_gesamtstunden - bd_abzugsstunden

# **Korrekte Stundenlohn für Bereitschaftsdienst aus Tabelle verwenden**
bd_stundenlohn = stundenlohn_bd[eingaben["tarifgruppe"]][eingaben["stufe"]]

# Stundenanteil des Tabellenentgelts für Stufe 3 der jeweiligen Entgeltgruppe
zuschlag_stundenlohn = tarifstruktur[eingaben["tarifgruppe"]][3] / (38.5 * 4.33)

# Berechnung der Zuschläge mit dem korrekten BD-Stundenlohn
nachtstunden = 8 * sum(eingaben["bd_anzahl"].values())  # Jede BD-Nacht hat 8h Nachtzeit
sonntagsstunden = eingaben["bd_anzahl"]["samstag"] * 8.75 + eingaben["bd_anzahl"]["sonntag"] * 15.25

zuschlag_nacht = nachtstunden * zuschlag_stundenlohn * zuschläge["nacht"]
zuschlag_sonntag = sonntagsstunden * zuschlag_stundenlohn * zuschläge["sonntag"]

# Berechnung des Rettungsdienst-Einsatzzuschlags
gesamt_einsatzzuschlag = eingaben["einsätze_rettungsdienst"] * einsatzzuschlag

# Gesamtbruttovergütung
gesamt_brutto = grundgehalt + (bd_relevante_stunden * bd_stundenlohn) + zuschlag_nacht + zuschlag_sonntag + gesamt_einsatzzuschlag

# Ergebnisse anzeigen
ergebnisse = pd.DataFrame({
    "Kategorie": [
        "Grundgehalt",
        "Bereitschaftsdienst (volle Stunden)",
        "Nachtzuschläge",
        "Sonntagszuschläge",
        "Rettungsdienst-Einsatzzuschlag",
        "Gesamt-Brutto"
    ],
    "Betrag (€)": [
        grundgehalt,
        bd_relevante_stunden * bd_stundenlohn,
        zuschlag_nacht,
        zuschlag_sonntag,
        gesamt_einsatzzuschlag,
        gesamt_brutto
    ]
})

tools.display_dataframe_to_user(name="Vollständige Berechnung der Vergütung mit allen Daten", dataframe=ergebnisse)
