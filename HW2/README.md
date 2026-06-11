1. Create “HW2.ipynb” – this will be the file for your homework (HW2_ScientificPython.ipynb).

2. In this homework, you deal with two databases – Uniprot (for protein sequences)
and ENSEMBL (for nucleotide sequences).

3. You can follow HW2_template to complete the task:
a. Implement function get_<db_name> for each database that accepts an ID and outputs API response.
b. Implement function parse_response_<db_name> for each database that accepts API response and outputs parsed information about the given ID.
c. Implement function main that accepts a list of IDs and outputs a DataFrame with responses. Here you should define regular expressions to distinguish between IDs of different databases. Also, you should use here get and parse functions written beforehand.

**Note:** the links for the necessary Uniprot and ENSEMBL documentation are
provided in lecture materials (jupyter notebook examples).

4. Test your code with test_data.txt.
5. Create “HW2” branch in your repo.
6. Create a directory “HW2” inside.
7. Upload your IPYNB file into “HW2” and create a pull request to submit your work.

# Code overview

## Database identification (using regex)

I defined two compiled regular expression patterns at the global level to classify incoming biological IDs:

- `IDENTIFY_UNIPROT`matches standard 6-character and 10-character UniProt protein accessions;
- `IDENTIFY_ENSEMBL`validates nucleotide and gene identifiers with typical prefix and numeric formatting.
```python
IDENTIFY_UNIPROT = re.compile(r"^(?:[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2}|[OPQ][0-9][A-Z0-9]{3}[0-9])(?:-\d+)?$")

IDENTIFY_ENSEMBL = re.compile(r"^ENS[A-Z]{0,10}(?:E|FM|G|GT|P|R|T)\d{6,}(?:\.\d+)?$")
```
## The `get_uniprot` function

This method communicates with the UniProtKB REST API accessions endpoint to pull down raw entry payloads.
```python
def get_uniprot(uniprot_id: str):
    api_url = "https://rest.uniprot.org/uniprotkb/accessions"
    query_params = {"accessions": uniprot_id}
    return requests.get(api_url, params=query_params, timeout=25)
```
## The `uniprot_parse_response` function

This method handles JSON conversion, checks for empty query results and extracts the target attributes (`organism`, `geneInfo`, `sequenceInfo`, and `type`). It returns a dictionary map or an error message wrapper.
```python
def uniprot_parse_response(resp):
    try:
        json_data = resp.json()
        records = json_data.get("results", [])
        
        if not records:
            return {"err_msg": "No UniProt records found"}
            
        parsed_results = {}
        for item in records:
            accession = item.get("primaryAccession")
            parsed_results[accession] = {
                "organism": item.get("organism", {}).get("scientificName"),
                "geneInfo": item.get("genes"),
                "sequenceInfo": item.get("sequence"),
                "type": "protein"
            }
        return parsed_results
    except (KeyError, TypeError, ValueError) as err:
        return {"err_msg": f"UniProt parse error: {str(err)}"}
```
## The get_ensembl function

This method targets specific Ensembl feature endpoints to fetch genomic records in .JSON.
```python
def get_ensembl(ensembl_id: str):
    api_url = f"https://rest.ensembl.org/lookup/id/{ensembl_id}"
    req_headers = {"Content-Type": "application/json"}
    return requests.get(api_url, headers=req_headers, timeout=25)
```
## The `ensembl_parse_response` function

This method unpacks Ensembl query payloads into ten specific keys requested in the template assignment, capturing structural features and transcript IDs.

```python
def ensembl_parse_response(resp):
    try:
        json_data = resp.json()
        feature_id = json_data.get("id")
        
        if not feature_id:
            return {"err_msg": "No Ensembl feature ID discovered"}
            
        extracted_fields = {
            "object_type": json_data.get("object_type"),
            "species": json_data.get("species"),
            "assembly_name": json_data.get("assembly_name"),
            "biotype": json_data.get("biotype"),
            "display_name": json_data.get("display_name"),
            "id": feature_id,
            "db_type": json_data.get("db_type"),
            "description": json_data.get("description"),
            "source": json_data.get("source"),
            "canonical_transcript": json_data.get("canonical_transcript")
        }
        return {feature_id: extracted_fields}
    except (KeyError, TypeError, ValueError) as err:
        return {"err_msg": f"Ensembl parse error: {str(err)}"}
```
## The `main` function

Chains everything together. It iterates over input elements, strips whitespaces, checks regex matches, routes calls to network clients, handles HTTP errors and updates local dictionary records.
```python
def main(ids: list):
    dataset_rows = []
    
    for raw_id in ids:
        clean_id = raw_id.strip()
        if not clean_id:
            continue
            
        record_entry = {"input_id": clean_id}
        
        try:
            if IDENTIFY_ENSEMBL.match(clean_id):
                api_resp = get_ensembl(clean_id)
                api_resp.raise_for_status()
                parsed_data = ensembl_parse_response(api_resp)
                
            elif IDENTIFY_UNIPROT.match(clean_id):
                api_resp = get_uniprot(clean_id)
                api_resp.raise_for_status()
                parsed_data = uniprot_parse_response(api_resp)
                
            else:
                record_entry["error"] = "error:unknown database"
                dataset_rows.append(record_entry)
                continue

            if "err_msg" in parsed_data:
                record_entry["error"] = parsed_data["err_msg"]
            else:
                inner_data = parsed_data.get(clean_id, next(iter(parsed_data.values())))
                record_entry.update(inner_data)
                
        except requests.RequestException as network_err:
            record_entry["error"] = f"Network/HTTP error: {str(network_err)}"
            
        dataset_rows.append(record_entry)
        
    return pd.DataFrame(dataset_rows)
```
## Test

```python
results = main(['P11473', 'Q91XI3', 'hello', 'ENSG00000157764', 'ENSG00000139618', 'MGP_AJ_G0023128'])
```
