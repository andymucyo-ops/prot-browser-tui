
def _data_as_ROWS(display_data: dict[str, str]) -> list[tuple[str]]:
    data_as_ROWS: list[tuple[str]] = [
            ("Entry n°", "Accession", "UniprotKB ID", "Organism Name", "Common Name")
            ]
    count: int = 1
    for entry in display_data:
        prot: dict[str,str] = display_data[entry]
        data_as_ROWS.append(
               (count, prot["Accession"], prot["UniprotKB ID"], prot["Organism Name"], prot["Common Name"]) 
                )
        count += 1

    return data_as_ROWS
