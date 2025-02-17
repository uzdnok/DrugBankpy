import pytest
import matplotlib.pyplot as plt
import matplotlib.figure
from Pdp6 import create_dictPDP6


@pytest.fixture
def sample_xml(tmp_path):

    content = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug>
        <drugbank-id>DB0001</drugbank-id>
        <name>Drug One</name>
        <pathways>
            <pathway>
                <drugs>
                    <drug>
                        <name>Drug A</name>
                    </drug>
                    <drug>
                        <name>Drug B</name>
                    </drug>
                </drugs>
            </pathway>
        </pathways>
    </drug>
    <drug>
        <drugbank-id>DB0002</drugbank-id>
        <name>Drug Two</name>
        <pathways>
            <pathway>
                <drugs>
                    <drug>
                        <name>Drug B</name>
                    </drug>
                    <drug>
                        <name>Drug C</name>
                    </drug>
                </drugs>
            </pathway>
        </pathways>
    </drug>
    <drug>
        <drugbank-id>DB0003</drugbank-id>
        <name>Drug Three</name>
    </drug>
</drugbank>
'''
    file = tmp_path / "drugbank_partial.xml"
    file.write_text(content, encoding="utf-8")
    return file


def test_parse_drug_interactions(sample_xml):
    interactions = create_dictPDP6(str(sample_xml))
    expected = {
        "Drug A": 1,
        "Drug B": 2,
        "Drug C": 1,
        "Drug Three": 0
    }
    assert interactions == expected

