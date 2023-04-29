# Gradient Boosted DNS

Personal project to create a machine learning model to classify, in near-real time, DNS queries that my recursive resolver sees and adds them to my PiHole blocklist.

## Plan

### Data

Utilize large-scale pDNS data as a training set, sourced from the following sources:

1. [Tranco top 1m domains](https://tranco-list.eu/) [[3]](#3)

    - Note that we are assuming that these domains are legitimate, so we use this dataset as our negative class training data

2. [CERTPL](https://cert.pl/en/posts/2020/03/malicious_domains/)

    - We will randomly sample domains in a daily list of malicious domains from CERTPL over a week timespan

3. SANS suspicious domains ([low](https://web.archive.org/web/20200503151842/https://www.dshield.org/feeds/suspiciousdomains_Low.txt), [medium](https://web.archive.org/web/20190412151141/https://dshield.org/feeds/suspiciousdomains_Medium.txt), [high](https://web.archive.org/web/20170617154646/https://secure.dshield.org/feeds/suspiciousdomains_High.txt))

    - These datasets are slightly old (2020), but it's the most recent dataset available from SANS

4. [oisd blocklist](https://oisd.nl/)

    - The big blocklist, specifically

5. [AirVPN malware blocklist](https://airvpn.org/api/dns_lists/?code=air_malware&block=0.0.0.0&style=domains)

I'll utilize the dataset generation code from [[2]](#2) to enrich my domains with additional features. I will have to modify this slightly.

### Model

I will use gradient boosted trees for this project, due to their performance as suggested in [[1]](#1). Once the model is trained, it will sit on the recursive resolver (Unbound) and periodically poll the PiHole cache to classify domains recently seen. Those domains that are classified as malicious will be automatically added to the PiHole block list. I have a dedicated machine that acts as my PiHole and run Unbound on that same machine.

## References

<a id="1">[1]</a>
Alhogail, A., Al-Turaiki, I. (2022). Improved Detection of Malicious Domain Names using Gradient Boosted Machines and Feature Engineering. Information Technology and Control, 51(2), 313-331. <http://dx.doi.org/10.5755/j01.itc.51.2.30380>

<a id="2">[2]</a>
Marques, C., Malta, S., & Magalhães, J. A. (2021). DNS dataset for malicious domains detection. Data in Brief, 38, 107342. <https://doi.org/10.1016/j.dib.2021.107342>

<a id="3">[3]</a>
Victor Le Pochat, Tom Van Goethem, Samaneh Tajalizadehkhoob, Maciej Korczyński, and Wouter Joosen. 2019. "Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation," Proceedings of the 26th Annual Network and Distributed System Security Symposium (NDSS 2019). <https://doi.org/10.14722/ndss.2019.23386>
