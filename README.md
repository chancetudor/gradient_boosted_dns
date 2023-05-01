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

    - These datasets are slightly old (2020), but they're the most recent datasets available from SANS

4. [oisd blocklist](https://oisd.nl/)

    - The big blocklist, specifically

5. [AirVPN malware blocklist](https://airvpn.org/api/dns_lists/?code=air_malware&block=0.0.0.0&style=domains)

I'll utilize the dataset generation code from [[2]](#2) to enrich my domains with additional features. I will have to modify this slightly.

The training, validation, and test split was originally as follows:

- Training dataset: ~1,846,000 records (80% of the overall dataset)

- Validation dataset: ~231,000 records (10% of the overall dataset)

- Test dataset: ~231,000 records (10% of the overall dataset)

However, due to overfitting seen in the original model run, I am decreasing the splits as follows:

- Training dataset: ~1,546,000 records (67% of the overall dataset)

- Validation dataset: ~300,000 records (13% of the overall dataset)

- Test dataset: ~461,000 records (20% of the overall dataset)

### Model

I will use gradient boosted trees for this project, due to their performance as suggested in [[1]](#1). In addition, GBTs have low hardware ovehead and are trained quickly. I will use the authors' initial hyperparameters: "...the learning rate is set to 0.1, tolerance for the early stopping to 0.0001, the quality of split is measured using Friedman mean squared error, and the loss function to be optimized is set to deviance, which refers to logistic regression." Also per [[1]](#1), I will use just six features:

1. Domain Length,
2. Strange Character Count,
3. Numeric Sequence,
4. Numeric Ratio,
5. Consonant Ratio, and
6. Vowel Ratio

The authors of [[1]](#1) suggest that they found these 5 features (Numeric Sequence, Numeric Ratio, Strange Characters, Consonant Ratio, Vowel Ratio) most important, plus DNS record type. As I did not have access to DNS record types for my training data, and my resolver primarily deals with A record requests (and does not handle IPv6) I have opted to not include this and instead replace it with domain length, which was a top 10 most important feature for the authors. Unfortunately, for many of the authors' feature importance measures, DNS record type was at the top, so my model may have lower performance without being trained on record type.

I will use the following performance measures:

- accuracy = (TP + TN) / TP + TN + FP + FN
- precision (P) = TP / TP + FP
- false positive rate (FPR) = FP / FP + TN
- true positive rate (TPR) = TP / TP + FN
- F-measure = (2 x P x TPR) / P + DR

Once the model is trained, it will sit on the recursive resolver (Unbound) and periodically poll the PiHole cache to classify domains recently seen. Those domains that are classified as malicious will be automatically added to the PiHole block list. I have a dedicated machine that acts as both my PiHole and recursive resolver.

## References

<a id="1">[1]</a>
Alhogail, A., Al-Turaiki, I. (2022). Improved Detection of Malicious Domain Names using Gradient Boosted Machines and Feature Engineering. Information Technology and Control, 51(2), 313-331. <http://dx.doi.org/10.5755/j01.itc.51.2.30380>

<a id="2">[2]</a>
Marques, C., Malta, S., & Magalhães, J. A. (2021). DNS dataset for malicious domains detection. Data in Brief, 38, 107342. <https://doi.org/10.1016/j.dib.2021.107342>

<a id="3">[3]</a>
Victor Le Pochat, Tom Van Goethem, Samaneh Tajalizadehkhoob, Maciej Korczyński, and Wouter Joosen. 2019. "Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation," Proceedings of the 26th Annual Network and Distributed System Security Symposium (NDSS 2019). <https://doi.org/10.14722/ndss.2019.23386>
