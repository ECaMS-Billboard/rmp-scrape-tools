# rmp-scrape-tools

For web scraping professor ratings from [RateMyProfessors](https://www.ratemyprofessors.com/), I originally used a script adapted from [this repo](https://github.com/tisuela/ratemyprof-api). I was able to collect rating data (`/data/`) as of November 2024 for Lewis University faculty but my script no longer works, so I have since removed it from this repo. I think something changed on the website upstream which broke the approach I was using. The current `scrape.py` uses a [different library](https://github.com/Nobelz/RateMyProfessorAPI) to perform the scraping. And while it is functional, it still has a lot of issues. You'll see if you try running it. If anyone picks up this part of the project in the future there are still plenty of other tools you can check out like [this](https://github.com/Elie-Z/RateMyProfessor.com-Web-Scraper) or [this](https://github.com/lumirth/rmpy) that I never tested.

Otherwise, This repo contains other miscellaneous Python scripts for cleaning/formatting JSON data. Written with [ECaMS Billboard](https://github.com/ECaMS-Billboard/ecams-billboard) in mind, but not necessarily limited to that project.


## Setup
1. Clone repository: `git clone https://github.com/ECaMS-Billboard/rmp-scrape-tools`

2. Install dependencies: `pip install -r requirements.txt`


## Usage
`main.py` uses `argparse` for processing command line arguments. Here are some usage examples. (You can also use `-h` to see a description of each option.)


> *Note that for most functions in this repo, if an output path is not specified, the input file will be overwritten.*

<br/>

### Convert JSON array files to JSONL and back

```bash
python3 main.py --array-to-jsonl -i path/to/input.json
# or vice-versa (shown with optional output argument):
python3 main.py --jsonl-to-array -i input.json -o output.json
```

<br/>

### Format a JSON array file with proper (4-spaces) indentation

```bash
python3 main.py --beautify -i data/input.json
```

<br/>

### Upload a JSONL file as a new collection on MongoDB Atlas

- Requires the `MONGO_URI` string to be set in `secrets.py`.
- Does not create any file output, but be careful as it will overwrite the given collection if it already exists.
- The `_id` property is set by MongoDB automatically.

```bash
# Upload to "Professors" collection:
python3 main.py --upload_to_collection Professors -i input.json

# Database defaults to "EcamsDB", but you can also use --dbname to change that:
python3 main.py --dbname NewDB --upload_to_collection CollectionName -i input.json
```


<br/>

### Scraping

```bash
python3 scrape.py
```
