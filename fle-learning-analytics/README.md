# FLE Learning Analytics · synthetic classroom case study

**Junior BOOTO WABA** · Python + French language education · Grades 2–5, A1 classroom goals.

This reproducible **demonstration** shows how four separate skill assessments—compréhension orale (CO), compréhension écrite (CE), production orale (PO) and production écrite (PE)—can inform a next teaching step. All 32 learner IDs and 256 assessment rows are **synthetic and algorithmically generated**. They are not records from my school or evidence that a real intervention improved outcomes.

## See the result

- [Illustrative results and chart](reports/summary.md)
- [Teaching decision case study](teaching-case.md)
- [Synthetic assessment data](data/synthetic_assessments.csv)

## Reproduce

```bash
python -m pip install -r requirements.txt
python generate_data.py
python analyze.py
```

Python 3.10+ is recommended. The first script regenerates identical fictional data using a fixed seed; the second validates the schema, computes scores and period means, and generates `reports/summary.md` and `reports/skill_progress.svg`. Run from any working directory. The checked-in results can be compared after rerunning.

## Data dictionary

| Field | Meaning |
|---|---|
| synthetic_id | Explicitly fake stable identifier; eight fictional learners per grade |
| grade | 2, 3, 4 or 5 |
| period | T1 or T2; two illustrative measurement points, not actual school terms |
| skill | CO, CE, PO or PE, assessed separately |
| criterion_1/2/3 | Locally designed rubric criteria, each integer 0–3; total 0–9 |
| support | Example access scaffold recorded alongside the evidence |

The [programme assessment framework](https://github.com/Junior-BOOTO/portfolio-fle/blob/main/ib-pyp-french-programme/assessment/framework.md) explains the local rubric. Scores and changes are descriptive illustrations and **must not be converted into CEFR certification or used to rank pupils**. Scores for different skills reflect different tasks and criteria, so compare each skill over time with attention to task comparability and support.

## Limitations and privacy

The model intentionally builds an improvement pattern, especially in speaking. It cannot test teaching effectiveness, causal impact, or individual proficiency. Any real use would require school authorization, an appropriate data process, minimal collection, secure storage, and assessment moderation. Public GitHub should contain only fictional or properly authorized non-identifying material. Do not upload actual pupil names, grades, recordings, written work or school exports here.

## Sources

- [Council of Europe: CEFR descriptors](https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors) for observable communicative goals.
- [IB: About assessment](https://ibo.org/about-the-ib/what-it-means-to-be-an-ib-student/recognizing-student-achievement/about-assessment/) for feedback and reflection in the PYP.
- [UNESCO IITE: personal data and privacy protection in online learning](https://iite.unesco.org/publications/personal-data-and-privacy-protection-in-online-learning/).

The dataset, code, chart and interpretation are independently authored for this portfolio; no IB or Council of Europe endorsement is implied.
