import csv
import os

import pandas as pd
import ruamel.yaml


class Converter(object):
    """ Converts a CSV containing texts and corresponding intents into a Rasa
        compatible yaml 'intents' nlu file and exports it to specified directory.

        One also has the option to convert a Rasa 'intents' yaml file into a
        csv with 'text' and 'intent' columns for data analysis purposes.
    Args:
        file_path (str): Full path to csv or yaml file to be converted
        intent_column (str): Header name of intent column
        text_column (str): Header name of text column
        examples_column (str): YAML key for text examples
        rasa_version (str): Rasa version
        export_dir (str): Directory to export the yaml or csv file to
        output_file (str): What to name exported yaml or csv file
        to_csv (bool): Whether to convert yaml to csv
    """

    def __init__(
            self,
            file_path: str,
            intent_column: str = 'intent',
            text_column: str = 'text',
            examples_column: str = 'examples',
            rasa_version: str = '3.0',
            export_dir: str = '.',
            output_file_name: str = 'nlu.yml'
    ):
        self.file_path = file_path
        self.intent_column = intent_column
        self.text_column = text_column
        self.examples_column = examples_column
        self.rasa_version = rasa_version
        self.export_dir = export_dir
        self.output_file_name = output_file_name
        self.yaml = ruamel.yaml.YAML()
        # Set to ensure Rasa indentation formatting compliance
        self.yaml.indent(mapping=2, sequence=4, offset=2)

    def convert_csv_to_yaml(self, rasa_version: str = "3.0"):
        """ Converts CSV to Rasa compatible YAML

        Args:
            rasa_version (str): Rasa version
        """
        literal = ruamel.yaml.scalarstring.LiteralScalarString
        yaml_path = os.path.join(self.export_dir, self.output_file_name)
        df = pd.read_csv(self.file_path)
        nlu = []

        intents = df[self.intent_column].unique().tolist()
        for intent in intents:
            sample = {}
            sample['intent'] = intent
            intent_texts = df[
                df[self.intent_column] == intent][self.text_column].tolist()

            intent_texts = filter(lambda x: (x.lower().find("are") != -1 or x.lower().find("do") != -1 or x.lower().find("can") != -1 or x.lower().find("is") != -1 or x.lower().find("may") != -1 ) and x.lower().find("what") == -1 and x.lower().find("how") == -1 and x.lower().find("why") == -1 and x.lower().find("when") == -1 and x.lower().find("where") == -1 and x.lower().find("which") == -1 and x.lower().find("?") != -1, intent_texts)
            # Workaround that allows for injection of scalar literal '|'
            intent_texts_str = ''
            for text in intent_texts:
                intent_texts_str += f'- {text}\n'

            # Injection of scalar literal to ensure Rasa formatting compliance
            sample['examples'] = literal(intent_texts_str)
            nlu.append(sample)

        yaml_dict = {
            'version': rasa_version,
            'nlu': nlu
        }

        with open(yaml_path, 'w') as f:
            self.yaml.dump(yaml_dict, f)

    def convert_yaml_to_csv(self):
        """ Converts Rasa intent YAML to CSV
        """
        with open(self.file_path) as file:
            documents = self.yaml.load(file)['nlu']

        csv_file_path = os.path.join(self.export_dir, self.output_file_name)
        with open(csv_file_path, 'w') as csv_file:
            wr = csv.writer(csv_file, lineterminator='\n')
            # Creating header for csv
            wr.writerow([self.text_column, self.intent_column])

            for item in documents:
                examples = item[self.examples_column].split('- ')

                # Removing empty values
                examples = list(filter(None, examples))
                examples = examples[0:30]
                for example in examples:
                    wr.writerow([example.strip(), item[self.intent_column]])


def convert(file_path: str,
            intent_column: str,
            text_column: str,
            examples_column: str,
            rasa_version: str,
            export_dir: str,
            output_file_name: str,
            to_csv: bool):
    """ Instantiates a Converter object and calls the appropriate method
        to either convert a csv to a yaml file or a yaml to a csv.
    Args:
        file_path (str): Full path to csv or yaml file to be converted
        intent_column (str): Header name of intent column
        text_column (str): Header name of text column
        examples_column (str): YAML key for text examples
        rasa_version (str): Rasa version
        export_dir (str): Directory to export the yaml or csv file to
        output_file (str): What to name exported yaml or csv file
    """
    converter = Converter(
        file_path,
        intent_column,
        text_column,
        examples_column,
        rasa_version,
        export_dir,
        output_file_name
    )

    converter.convert_yaml_to_csv() if to_csv \
        else converter.convert_csv_to_yaml()


if __name__ == '__main__':
    convert('C:\\Users\\DELL\\Desktop\\train.csv', 'intent', 'text', 'examples', '3.0', '.', 'nlu_count_how.yml', False)
