configfile: "config.json"

rule all:
    input:
        expand("img/{year}-age-vs-time.pdf", year=config)

rule fetch:
    output:
        page="html/{year}.html",
        ind_csv="csv/{year}-individuals.csv"
    params: event_id=lambda wildcards: config[int(wildcards.year)]
    shell: "./fetch.py --event_id {params.event_id} > {output.page} 2> {output.ind_csv}"

rule:
    input: "html/{year}.html"
    output: "csv/{year}-main.csv"
    shell: "./make_csv.py < {input} > {output}"


rule age_vs_time:
    input:
        main="csv/{year}-main.csv",
        ind="csv/{year}-individuals.csv"
    output: "img/{year}-age-vs-time.pdf"
    shell: "./vis.py --year {wildcards.year}"