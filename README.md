# Item Pool API

## Item Pool Schema Considerations
[Sheets-Link](https://docs.google.com/spreadsheets/d/1KoMPBrpQwkc_MqvEMF8f3S4bohgVmD9xl5TsExAQftQ/edit?gid=1482087079#gid=1482087079)

## API starten

1. **Installation von `uv`**  
   Anleitung: [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

2. **API starten**  
   ```bash
   uv run fastapi dev main.py
   ```

## ToDo's ItemPool
- [ ] ENUM-Varianten der TaskType-Klasse sollten über HTTP GET abfragbar sein
- [ ] ENUM-Varianten der MaterialType-Klasse sollten als Datenstruktur hinterlegt werden
- [ ] material_information der Klasse TaskMaterial sollte validiert werden
- [ ] task_solutions der Klasse Task ist von TaskType abhängig und sollte nicht nur ein String sein (ENUM-Lösung?)
- [ ] Metadaten-Berechnung für register_task_material und register_task, die zur Filterung genutzt werden könnten
- [ ] In registerTask kann direkt TaskMaterial angelegt werden, welches dann intern erstellt werden muss
- [ ] Aufteilung der Datei in mehrere Teile: models.py, router.py, main.py (Hauptcode), controller.py (Anlegen von TaskMaterial, Berechnung der Metadaten etc.)
- [ ] Anbindung einer echten Datenbank
- [ ] Beispielanfragen für großes Meeting vorbereiten und vorstellen

## Anforderungsspezifikationen
- [ ] ...

## API Spec

<table>
<tr>
<td> API-Route </td> <td> Payload structure  </td>  <td> Payload example </td>  <td> Procedure for specific payload example </td>
</tr>
<tr>
<td> registerTaskMaterial </td>
<td>

```javascript
{
	type: string,
	material_information: {
		[key: string]: unknown
	}
}
```

</td>

<td> 

```json
{
	"type": "database",
	"material_information": {
		"create_db": "CREATE ...",
		"db_dump": "link_to_dump",
		"db_flavour": "postgres"
	}
}
```

</td>

<td> 
  
  - registerDatabase(material) -> databaseId
    - computeDatabaseMetaData(id) -> databaseMetaData
      - storeDatabaseMetaData(databaseMetaData) -> void
  
</td>

</tr>

<tr>
<td> registerTask </td>
<td>

```javascript
{
	type: string,
	task: {
    task_material: Array<MaterialType> | Array<IDType>
    task_solutions: Array<SolutionType>
	}
}
```

</td>
<td> 

```json
{
	"type": "SQL",
	"task": {
		"task_material": [
			{
				"type": "task_description",
				"material_information": {
					"description": "Liste aller Mitarbeiter aus dem Vertrieb, mit PNr. und Name, aufsteigend sortiert nach Namen"
				}
			},
			{
				"type": "schema_description",
				"material_information": {
					"tables": ["mitarbeiter", "abteilung", "hotel", "reisen"]
				}
			},
			{
				"type": "resolve_existing_material",
				"id": "id_of_hotel-database"
			}
		],
		"task_solutions": [
			"SELECT foo FROM bar;"
		]
	}
}
```

</td>
<td> 

  - for material in task_material registerTaskMaterial(material)
    - computeMaterialMetaData(material_id) -> materialMetaData
      - storeMaterialMetaData(materialMetaData) -> void
  
</td>
</tr>

</table>

Ggf. muss ein "task_head" im "Payload" ergänzt werden, bzw. wie auch immer geartete Informationen über die Person, welche die Materialien/Aufgaben "registriert"?

-> Der Eindeutigkeit halber sollte ggf. eine Nutzerregistrierung möglich sein? ("registerUser")

## Exchange format (export?)

Potential exchange format, of which sections serve as a potential payload format for the aforementioned API-routes.

```json
{
	"1": {
		"task_head": {
			"type": "SQL",
			"creator": "Max",
			"university": "THM",

            "computedFilterablePropeties": {
                "tableAmountInSchema": 4,
                "amountOfForeignKeys": 3,
                "amountOfWeakEntities": 3,

                "SQLConcepts": ["SELECT", "GROUP BY", "SUBQUERY"]
            }
		},
		"task_body": {
			"task_description": "Liste aller Mitarbeiter aus dem Vertrieb, mit PNr. und Name, aufsteigend sortiert nach Namen",
            "show_tables": {
                "tables": ["mitarbeiter"]
            },
			"db": {
				"createDB": "CREATE ",
				"dbDump": "link_to_dump",
				"dbFlavor": "postgres"
			}
		},
        "task_solutions": [
            "SELECT bla ..."
        ]
	},
	"2": {
		"task_head": {
			"type": "ERM-Modellierung",
			"creator": "Max",
			"university": "THM"
		},
		"task_body": {
			"task_description": "Liste aller Reservierungen für Heute",
			"schema": {
				"name": "Restaurant",
				"createSchema": "CREATE ...",
				"dbDump": "link_to_dump2",
				"dbFlavor": "mysql"
			}
		},
        "task_solutions": [
            "a->b, "
        ]
	}
}

```