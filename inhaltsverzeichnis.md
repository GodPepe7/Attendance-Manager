---

Inhaltsverzeichnis

1. Einleitung
   - Hintergrund und Motivation
   - Zielsetzung der Bachelorarbeit
   - Aufbau der Arbeit

2. Grundlagen der Hexagonalen Softwarearchitektur
   - Prinzipien der Hexagonalen Architektur
   - Vorteile für automatische Tests

3. Softwareentwicklung in Python
   - Objektorientierte Programmierung in Python
   - Einführung in die verwendeten Technologien und Werkzeuge

4. Entwicklung der Prototyp-Applikation
   - Anforderungen und Spezifikationen der Applikation
   - Rollen und Berechtigungen

5. Teststrategien für Hexagonale Softwarearchitekturen
   - Übersicht der Testebenen: Unit-, Integrations- und Systemtests
   - Relevanz der Hexagonalen Architektur für testgetriebene Ansätze

6. Effiziente Umsetzung von Tests in Python
   - Frameworks und Tools für Unit-Tests
     - Einführung in relevante Python-Frameworks (z.B. unittest, pytest)
     - Praktische Implementierung in der Prototyp-Applikation
   - Integrationstests in der Praxis
     - Simulationsansätze und Mocking-Techniken
     - Integration in der hexagonalen Architektur
   - Systemtests und Gesamtsystemvalidierung
     - Testumfang und Methodik
     - Einsatz von automatisierten Testtools für Systemtests

7. Analyse der besonderen Herausforderungen
   - Effizienz der Testumsetzung in hexagonalen Architekturen
     - Strukturierung von Testfällen in Teilsystemen
     - Isolierung und Testbarkeit von Schnittstellen
   - Herausforderungen bei der Umsetzung
     - Komplexität der Architektur und Testimplementierung
     - Umgang mit Abhängigkeiten und Schnittstellen
   - Best Practices und Lessons Learned

8. Beantwortung der Forschungsfragen
   - Ergebnisse der Testimplementierung in der Prototyp-Applikation
   - Schlussfolgerungen aus der Analyse der realisierten Tests
   - Empfehlungen für zukünftige Projekte

9. Erweiterungen und Anbindungsmöglichkeiten
   - Potenziale für Erweiterbarkeit
   - Sicherheitsaspekte
   - Anbindung an externe Systeme (z.B. Moodle)

10. Bereitstellung der Applikation
    - Deployment auf einer virtuellen Maschine der HTW
    - Technische Anforderungen

11. Fazit und Ausblick
    - Zusammenfassende Bewertung
    - Mögliche Weiterentwicklungen und Forschungsfelder

12. Anhang
    - Quellcode-Auszüge
    - Testprotokolle
    - Benutzerhandbuch

13. Literaturverzeichnis

---

1. Einführung in die hexagonale Architektur:
    - Erläuterung der Grundkonzepte der hexagonalen Architektur.
    - Vergleich mit anderen Softwarearchitekturen (z. B. Schichtenarchitektur) und deren Testbarkeit.

2. Theoretische Grundlagen:
    - Prinzipien der Testbarkeit in Software.
    - Verbindung zwischen Architekturentscheidungen und Testbarkeit.
    - Typische Herausforderungen der Testbarkeit in traditionellen vs. hexagonalen Architekturen.

3. Aufbau einer Webapplikation mit hexagonaler Architektur:
    - Beschreibung eines konkreten Beispiels einer Webapplikation.
    - Erklärung der Implementierung der Kernelemente (Domänenlogik, Ports, Adapters).

4. Teststrategien in der hexagonalen Architektur:
    - Einheitentests: Testen der Domänenlogik isoliert von der Infrastruktur.
    - Integrationstests: Testen von Ports and Adapters, um sicherzustellen, dass die Kommunikation mit externen Systemen
      korrekt funktioniert.
    - End-to-End-Tests, wenn sinnvoll, um Benutzeraktionen zu simulieren.

5. Vorteile der hexagonalen Architektur für die Testbarkeit:
    - Untersuchung, wie die Trennung von Domänenlogik und Infrastruktur die Erstellung von Tests vereinfacht.
    - Diskussion der Flexibilität bei der Gestaltung von Testszenarien.

6. Herausforderungen und Grenzen:
    - Mögliche Nachteile bei der Einführung der hexagonalen Architektur in bestehende Systeme.
    - Diskussion über den Mehraufwand für die initiale Einrichtung und Schulung.

7. Fallstudie oder Experiment:
    - Entwicklung (oder Analyse) einer Beispiel-Webapplikation unter Anwendung der hexagonalen Architektur.
    - Durchführung einer empirischen Untersuchung zur Testbarkeit und Vergleich mit einer ähnlichen Applikation ohne
      hexagonale Architektur.

8. Zusammenfassung und Ausblick:
    - Zusammenfassen der Hauptbefunde Ihrer Arbeit.
    - Empfehlungen für Entwickler, die die hexagonale Architektur einsetzen oder erforschen wollen.

9. Literaturverzeichnis und Anhänge:
    - Verzeichnis der verwendeten Literatur und Quellen.
    - Optional: Code-Beispiele, Diagramme, und zusätzliche Materialien zur Unterstützung der Diskussion in der Arbeit.