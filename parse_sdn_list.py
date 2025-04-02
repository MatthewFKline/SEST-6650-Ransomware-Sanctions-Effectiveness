"""
Script for parsing OFAC's SDN list.

See https://sanctionslist.ofac.treas.gov/Home/SdnList
The associated list is SDN_ENHANCED.XML

Extracts all entities with bitcoin address features, providing their ID, features (addresses),
and associated sanctions programs.
"""

import xml.etree.ElementTree as ET


def get_tag_name(element) -> str:
    """Get rid of XML's long document name and just give us the tag we care about.

    :param element: XML Element
    :return: A string that isn't horrific
    """
    return element.tag.replace(
        "{https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ENHANCED_XML}", "")


class Entity:
    """Defines an entity from the SDN entity list"""

    def __init__(self, element: ET.Element):
        """Init method for Entity class

        :param element: An element from the SDN entity list
        """
        self.general_info = {}
        self.sanctions_lists = None
        self.sanctions_programs = []
        self.legal_authorities = None
        self.names = []
        self.addresses = []
        self.features = []
        self._raw = ET.tostring(element)

        def _parse_general_info(element) -> None:
            """Find the identity ID and add it to the instance attributes.

            :param element: tHiS cODe iS SElF-dOCuMenTiNG
            """
            for entry in element:
                if get_tag_name(entry) == "identityId":
                    self.general_info["identityId"] = entry.text

        def _parse_features(element) -> None:
            """Find bitcoin addresses in features and add them to instance list of features.

            :param element: tHiS cODe iS SElF-dOCuMenTiNG
            """
            for entry in element:
                if get_tag_name(entry) == "feature":

                    # Somehow this never becomes True when parsing the entire SDN
                    # I have no idea how this script ever worked
                    is_bitcoin_address = False

                    for sub_entry in entry:

                        if get_tag_name(sub_entry) == "type":
                            if sub_entry.text == "Digital Currency Address - XBT":
                                is_bitcoin_address = True

                        if get_tag_name(sub_entry) == "value":
                            if is_bitcoin_address:
                                self.features.append(sub_entry.text)

        def _parse_sanctions_program(element) -> None:
            """Find sanctions programs and add them to instance list of sanctions programs.

            :param element: tHiS cODe iS SElF-dOCuMenTiNG
            """
            for entry in element:
                if get_tag_name(entry) == "sanctionsProgram":
                    self.sanctions_programs.append(entry.text)

        # Iterate over the entity's elements and extract the data we care about
        for entry in element:
            if get_tag_name(entry) == "generalInfo":
                _parse_general_info(entry)

            if get_tag_name(entry) == "features":
                _parse_features(entry)

            if get_tag_name(entry) == "sanctionsPrograms":
                _parse_sanctions_program(entry)

    def __str__(self) -> str:
        return f"Entity object || {self.general_info} || {self.sanctions_programs} || {self.features}"


# Open and parse entities document
tree = ET.parse("data/SDN_ENHANCED.XML")
root = tree.getroot()
entities_data = []

# Grab the actual entities list out of the XML document
for child in root:
    if get_tag_name(child) == "entities":
        entities_data = child
        break

if not entities_data:
    raise ValueError("Could not find entities data")

# Parse obtained entities
entities = []
for entry in entities_data:
    entities.append(Entity(entry))

# Filter for entities containing bitcoin addresses
entities_with_bitcoin: list[Entity] = [item for item in filter(lambda x: x.features, entities)]

# Print data to terminal
for entry in entities_with_bitcoin:
    for address in entry.features:
        for order in entry.sanctions_programs:
            print(f"{address},{order}\n")

# Write data to CSV file
# with open("ofac_sanctions_w_programs.csv", "x") as f:
#     for entry in entities_with_bitcoin:
#         for address in entry.features:
#             for order in entry.sanctions_programs:
#                 f.write(f"{address},{order}\n")
