Start Application \
`flask --app src.adapter.flask.app --debug run`

Problems so far:

- Mapping ORM to Vanilla Python Classes has barely any documentation
- Lazy Loading
- Putting Authorization in domain instead of letting db handle it
- Keeping queries as simple as possible

Testing:

- Entity tests super simple, not much to do here as they barely have functionality
- when using sql alchemy ORM, creating instances of classes has to happen *after* the classes are mapped to the orm
  -> solved by local importing which will only do the import when the function is called (look at )

```
sqlalchemy.orm.exc.UnmappedInstanceError: Class 'src.domain.entities.course.Course' is mapped, 
but this instance lacks instrumentation.  This occurs when the instance is created before 
sqlalchemy.orm.mapper(src.domain.entities.course.Course) was called.
```

- tests shouldn't affect each other, so always gotta rollback. sql-alchemy has
  this: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
-

TODO:

- ~~Lecture Management~~
- ~~Attendance Management~~
- ~~Attendance logging with QR Code~~ or Password
- Course Management
- ~~Frontend~~
- Tests
- DI

- Hexagonal Softwarearchitekturen sollen besonders geeignet hinsichtlich automatischer Tests sein.
- Im Rahmen der BA soll dies für die Programmiersprache Python exemplarisch anhand einer objektorientiert zu
  entwickelnden Software gezeigt werden.
- Hierbei sollen Unit-, Integrations- und Systemtests adressiert werden.
- Als Ergebnis sollen anhand der Realisierung der Software folgende Fragen nachvollziehbar beantwortet werden:
    - Wie lassen sich Unit-, Integrations- und Systemtests bei der Umsetzung hexagonaler Softwarearchitekturen in Python
      effizient realisiert?
    - Was ist hierbei zu beachten? Welche besonderen Herausforderungen ergeben sich bei einer solchen Umsetzung?
- Bei der prototypischen Software soll es sich um eine Applikation handeln, mit deren Hilfe die Dozierenden von
  Unikursen die Anwesenheit von Studierenden zu einzelnen Terminen erfassen können. Folgende funktionalen und
  nichtfunktionalen Anforderungen sollen realisiert werden:
    - Umsetzung als Web-Applikation
    - Es gibt drei Rollen: Admin, Dozent_in, Student_in
    - Admins können Dozent_innen Verwalten.
    - Dozent_innen können Kurse verwalten, Termine verwalten, Anwesenheit verwalten, Übersichten über die Anwesenheit in
      Kursen und Terminen einsehen
    - Student_innen können die Anwesenheit an einem Termin in einem Kurs eintragen.
    - Details zum Eintragen der Anwesenheit:
        - Dozent_innen können festlegen, dass Studierende ein Passwort brauchen, um ihre Anwesenheit eintragen zu
          können.
        - Dozent_innen können festlegen, dass Studierende einen QR-Code scannen müssen um ihre Anwesenheit eintragen zu
          können. Diesen QR-Code können Dozent_innen bei dem Termin (z.B. über einen Beamer) zeigen. Der Code wechselt
          nach
          einer einstellbaren Zeit von Sekunden automatisch. Die Studierenden benutzen eine vorhandene QR-Code-fähige
          Handyapp,
          um sich einzutragen.
        - Es muss geklärt werden, welche Möglichkeiten hinsichtlich eines Missbrauchs des Systems es gibt. Wenn möglich
          müssen Mechanismen implementiert werden, die einen solchen Missbrauch verhindern.,
        - Eine Anbindung an ein System, dass Studierende und Kurse verwaltet (z.B. Moodle), muss möglich sein. Hierüber
          soll
          dann auch eine Anmeldung von Studierenden an die Applikation realisierbar sein, sodass nur angemeldete
          Studierende
          ihre Anwesenheit eintragen können. Eine konkrete Anbindung muss nicht realisiert werden.
        - Die Software soll wartbar und erweiterbar sein. Sicherheitsaspekte sind zu berücksichtigen.
    - Die Software muss auf einer virtuellen Maschine der HTW zur Verfügung gestellt werden.