import pytest

from Pdp4 import solvePDP4


@pytest.fixture
def sample_xml(tmp_path):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug>
        <drugbank-id>DB0001</drugbank-id>
        <pathways>
            <pathway>
                <name>Pathway A</name>
                <category>Metabolic</category>
                <smpdb-id>SMP1234</smpdb-id>
            </pathway>
        </pathways>
    </drug>
    <drug>
        <drugbank-id>DB0002</drugbank-id>
        <pathways>
            <pathway>
                <name>Pathway B</name>
                <category>Signaling</category>
                <smpdb-id>SMP2468</smpdb-id>
            </pathway>
            <pathway>
                <name>Pathway C</name>
                <category>Metabolic</category>
                <smpdb-id>SMP3333</smpdb-id>
            </pathway>
        </pathways>
    </drug>
</drugbank>
'''
    file = tmp_path / "drugbank_partial.xml"
    file.write_text(content, encoding="utf-8")
    return file


def test_parse_drugbank_xml(sample_xml):
    df, num_pathways = solvePDP4(sample_xml)

    assert num_pathways == 3, "Liczba szlaków powinna wynosić 3."

    expected_columns = ['name', 'category', 'smpdb-id']
    assert list(df.columns) == expected_columns, "Nieprawidłowe kolumny w ramce danych."

    expected_data = [
        {'name': 'Pathway A', 'category': 'Metabolic', 'smpdb-id': 'SMP1234'},
        {'name': 'Pathway B', 'category': 'Signaling', 'smpdb-id': 'SMP2468'},
        {'name': 'Pathway C', 'category': 'Metabolic', 'smpdb-id': 'SMP3333'}
    ]

    result = df.to_dict(orient='records')
    assert result == expected_data, "Zwrócone dane nie zgadzają się z oczekiwanymi."

