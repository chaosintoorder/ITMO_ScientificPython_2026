1. Create “HW4.ipynb” – this will be the file for your homework.
2. In this hometask you will implement a FASTA parser that will read FASTA files, scan them for possible Uniprot/ENSEMBL IDs in definition line and calling corresponding databases for a detailed data.
3. Additionally, you will practice calling command line tool SeqKit from Python using subprocess module.
4. You have three fasta files. One is correct, one contains incorrect ID and one is invalid.
5. Your task is to write a parser that will do the following:
a. Call “seqkit stats” on a given fasta file.
b. Parse an output from the seqkit. If collection raised an error – capture it and
return as a final output.
c. If the stats collection is successful, you should find a file type (DNA or Protein) in
the output.
d. Read a given fasta file with biopython.
e. Iterate over sequences to read the descriptions.
f. While iterating, check each description for a possible ID from either Uniprot or
ENSEBL depending on what type you identified before (one fasta file contains
only one type of data - nucleotides or aminoacids – so you can define your search
criteria before starting an iteration) - use regular expressions from HW2_1.
g. Perform an API call to a given database (Uniprot or ENSEMBL) – use requests
from HW2.
h. The final output should contain info about each sequence (description,
sequence, info from DB and the name of this DB).
6. As for code structure, you have a template provided and test_data.txt to see the exampe. The parser can be implemented as a Class, containing
a. Several utility methods (starting with __) for API calls and parsing responses –
you can use your code from HW2.
b. Public methods that should be used for producing an actual output - seqkit call
and biopython parser.
7. Test your work and save the output inside Jupyter notebook.

# Code overview

We have 5 files:
- **test_file.fasta** - test file for checking;
- **uniprot_download.fasta** - file with UniProt IDs;
- **ensembl_download_1.fasta** - file with ENSEMBL IDs (correct one);
- **ensembl_download_2.fasta** - file with ENSEMBL IDs (contains errors);
- **test_data.txt** - sample expected output.
## Imports and class definition

Our imports:
```python
!pip install Bio
!wget https://github.com/shenwei356/seqkit/releases/download/v2.5.1/seqkit_linux_amd64.tar.gz
!tar -xzf seqkit_linux_amd64.tar.gz
!chmod +x seqkit
!sudo mv seqkit /usr/local/bin/
!seqkit version

import requests
import re
import json
from Bio import SeqIO
import subprocess
import sys
```

Our classes:
```python
class MyFastaParser:
    """
    Class for parsing FASTA files with seqkit calls and database queries.
    """
    def __init__(self, file_name):
        """
        Initializes the parser with the specified file name.
        
        Args:
            file_name (str): Path to the FASTA file
        """
        self.filename = file_name
        # Regular expressions for finding IDs in sequence descriptions
        self.uniprot_pattern = re.compile(
            r"(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})(?:-\d+)?"
        )
        self.ensembl_pattern = re.compile(
            r"ENS[A-Z]{0,10}(?:E|FM|G|GT|P|R|T)\d{6,}(?:\.\d+)?"
        )

    def _get_uniprot(self, accession):
        """
        Internal method for querying the UniProt API.
        
        Args:
            accession (str): UniProt accession identifier
            
        Returns:
            requests.Response: Response from the API
        """
        endpoint = "https://rest.uniprot.org/uniprotkb/accessions"
        http_function = requests.get
        http_args = {"params": {"accessions": accession}, "timeout": 30}
        return http_function(endpoint, **http_args)

    def _get_ensembl(self, id):
        """
        Internal method for querying the ENSEMBL API.
        
        Args:
            id (str): ENSEMBL identifier
            
        Returns:
            requests.Response: Response from the API
        """
        endpoint = f"https://rest.ensembl.org/lookup/id/{id.split('.')[0]}"
        http_function = requests.get
        http_args = {"headers": {"Content-Type": "application/json"}, "timeout": 30}
        return http_function(endpoint, **http_args)

    def _uniprot_parse_response(self, resp: dict):
        """
        Parses the response from the UniProt API.
        
        Args:
            resp (dict): JSON response from UniProt
            
        Returns:
            dict: Structured information about the protein
        """
        resp = resp.json()
        output = {}
        for val in resp["results"]:
            accession = val["primaryAccession"]
            output[accession] = {
                "organism": val["organism"]["scientificName"],
                "geneInfo": val["genes"],
                "sequenceInfo": val["sequence"],
                "type": "protein"
            }
        return output

    def _ensembl_parse_response(self, resp: dict):
        """
        Parses the response from the ENSEMBL API.
        
        Args:
            resp (dict): JSON response from ENSEMBL
            
        Returns:
            dict: Structured information about the gene/transcript
        """
        resp = resp.json()
        id = resp["id"]
        output = {
            id: {
                "object_type": resp.get("object_type"),
                "assembly_name": resp.get("assembly_name"),
                "species": resp.get("species"),
                "db_type": resp.get("db_type"),
                "biotype": resp.get("biotype"),
                "display_name": resp.get("display_name"),
                "id": resp.get("id"),
                "description": resp.get("description"),
                "canonical_transcript": resp.get("canonical_transcript"),
                "source": resp.get("source")
            }
        }
        return output

    def _access_database(self, id, database, seq_description, seq_sequence) -> dict:
        """
        Queries the appropriate database and parses the response.
        
        Args:
            id (str): Identifier to search for
            database (str): 'uniprot' or 'ensembl'
            seq_description (str): Sequence description from FASTA
            seq_sequence (str): The sequence itself
            
        Returns:
            dict: Combined information from FASTA and the database
        """
        output = {
            f"file_info_{id}": {
                "description": seq_description,
                "sequence": seq_sequence
            }
        }
        response = None
        try:
            if database == "uniprot":
                response = self._get_uniprot(id)
                response.raise_for_status()
                parsed = self._uniprot_parse_response(response)
            else:
                response = self._get_ensembl(id)
                response.raise_for_status()
                parsed = self._ensembl_parse_response(response)
            output[f"database_info_{id}"] = next(iter(parsed.values()))
        except requests.RequestException as error:
            if response is not None:
                try:
                    error_output = response.json()
                except ValueError:
                    error_output = str(error)
            else:
                error_output = str(error)
            output[f"database_info_{id}"] = error_output
        return output

    def seqkit_stats(self) -> dict:
        """
        Calls seqkit stats to obtain statistics for the FASTA file.
        
        Returns:
            dict: File statistics or error
        """
        try:
            seqkit = subprocess.run(
                ("seqkit", "stats", self.filename, "-a"),
                capture_output=True,
                text=True
            )
        except FileNotFoundError as error:
            return {"error": str(error)}
        if seqkit.stderr:
            return {"error": seqkit.stderr.strip()}
        seqkit_out = seqkit.stdout.strip().split("\n")
        prop_names = seqkit_out[0].split()[1:]
        prop_vals = seqkit_out[1].split()[1:]
        seq_info = dict(zip(prop_names, prop_vals))
        seqkit_result = {
            "fasta_seqkit_stat_info": seq_info,
            "fasta_type": seq_info["type"],
            "fasta_num_seqs": int(seq_info["num_seqs"].replace(",", ""))
        }
        return seqkit_result

    def biopython_parser(self, seqkit_result) -> dict:
        """
        Parses the FASTA file using Biopython and queries databases.
        
        Args:
            seqkit_result (dict): Result from seqkit_stats()
            
        Returns:
            dict: Information about each sequence with database data
        """
        if "fasta_type" not in seqkit_result:
            return seqkit_result
        if seqkit_result["fasta_type"] == "Protein":
            pattern = self.uniprot_pattern
            database = "uniprot"
        else:
            pattern = self.ensembl_pattern
            database = "ensembl"
        output = {"DB_name": database}
        warning = False
        for seq in SeqIO.parse(self.filename, "fasta"):
            match = pattern.search(seq.description)
            if match is None:
                warning = True
                continue
            output.update(
                self._access_database(
                    match.group(0),
                    database,
                    seq.description,
                    str(seq.seq)
                )
            )
        if warning:
            output["WARNING"] = {"No ID match found."}
        return output

    def show_output(self, output, indent=0):
        """
        Pretty-prints structured data.
        
        Args:
            output (dict): Data to print
            indent (int): Indentation level
        """
        for key, value in output.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.show_output(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))
```
## Testing on test_file.fasta

```python
parser = MyFastaParser('test_file.fasta')
stats = parser.seqkit_stats()
print("=== Statistics seqkit for test_file.fasta ===")
print(json.dumps(stats, indent=2, ensure_ascii=False))
```
## Parsing and displaying results for test_file.fasta

```python
biopython = parser.biopython_parser(stats)
print("\n=== Parsing results for test_file.fasta ===")
parser.show_output(biopython)
```
## Testing on uniprot_download.fasta

```python
parser_uniprot = MyFastaParser('uniprot_download.fasta')
stats_uniprot = parser_uniprot.seqkit_stats()
print("=== seqkit stats for uniprot_download.fasta ===")
print(json.dumps(stats_uniprot, indent=2, ensure_ascii=False))

biopython_uniprot = parser_uniprot.biopython_parser(stats_uniprot)
print("\n=== Parsing results for uniprot_download.fasta ===")
parser_uniprot.show_output(biopython_uniprot)
```

## Testing on ensembl_download_1.fasta

```python
parser_ensembl1 = MyFastaParser('ensembl_download_1.fasta')
stats_ensembl1 = parser_ensembl1.seqkit_stats()
print("=== seqkit stats for ensembl_download_1.fasta ===")
print(json.dumps(stats_ensembl1, indent=2, ensure_ascii=False))

biopython_ensembl1 = parser_ensembl1.biopython_parser(stats_ensembl1)
print("\n=== Parsing results for ensembl_download_1.fasta ===")
parser_ensembl1.show_output(biopython_ensembl1)
```

## Testing on ensembl_download_2.fasta

```python
parser_ensembl2 = MyFastaParser('ensembl_download_2.fasta')
stats_ensembl2 = parser_ensembl2.seqkit_stats()
print("=== seqkit stats for ensembl_download_2.fasta ===")
print(json.dumps(stats_ensembl2, indent=2, ensure_ascii=False))

biopython_ensembl2 = parser_ensembl2.biopython_parser(stats_ensembl2)
print("\n=== Parsing results for ensembl_download_2.fasta ===")
parser_ensembl2.show_output(biopython_ensembl2)
```

Output:
```
=== seqkit stats for ensembl_download_2.fasta === { "error": "\u001b[31m[ERRO]\u001b[0m ensembl_download_2.fasta: fastx: invalid FASTA/Q format" } === Parsing results for ensembl_download_2.fasta === error [ERRO] ensembl_download_2.fasta: fastx: invalid FASTA/Q format
```

So, the second file (`ensembl_download_2.fasta`) is invalid.


```python
results = main(['P11473', 'Q91XI3', 'hello', 'ENSG00000157764', 'ENSG00000139618', 'MGP_AJ_G0023128'])
```
