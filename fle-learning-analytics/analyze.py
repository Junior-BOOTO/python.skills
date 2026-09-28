"""Descriptive analysis of synthetic FLE learning evidence; no predictive labels."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
INPUT = ROOT / 'data' / 'synthetic_assessments.csv'
REPORT = ROOT / 'reports' / 'summary.md'
FIGURE = ROOT / 'reports' / 'skill_progress.svg'
SKILLS = ['CO', 'CE', 'PO', 'PE']
LABELS = {'CO':'Listening (CO)', 'CE':'Reading (CE)', 'PO':'Speaking (PO)', 'PE':'Writing (PE)'}


def analyze():
    df = pd.read_csv(INPUT, dtype={'synthetic_id':str, 'grade':int, 'period':str, 'skill':str, 'support':str})
    needed = {'synthetic_id','grade','period','skill','criterion_1','criterion_2','criterion_3','support'}
    if set(df.columns) != needed or len(df) != 4*8*2*4:
        raise ValueError('Unexpected schema or number of records')
    if df.duplicated(['synthetic_id','grade','period','skill']).any():
        raise ValueError('Duplicate learner/period/skill rows')
    if set(df.period) != {'T1','T2'} or set(df.skill) != set(SKILLS):
        raise ValueError('Unexpected period or skill')
    if not df.synthetic_id.str.match(r'^SYN-G[2-5]-\d{2}$').all():
        raise ValueError('Only generated synthetic identifiers are accepted')
    if not (df.synthetic_id.str.extract(r'SYN-G(\d)')[0].astype(int) == df.grade).all():
        raise ValueError('ID/grade mismatch')
    scores = df[['criterion_1','criterion_2','criterion_3']]
    if scores.isna().any().any() or not scores.apply(lambda col: col.between(0,3)).all().all():
        raise ValueError('Criteria must be integers from 0 to 3')
    if not scores.apply(lambda col: (col % 1 == 0)).all().all():
        raise ValueError('Criteria must be integers')
    df['score'] = scores.sum(axis=1)
    aggregate = df.groupby(['skill','period']).score.agg(['mean','count']).reset_index()
    means = aggregate.pivot(index='skill',columns='period',values='mean').reindex(SKILLS)
    gains = (means['T2']-means['T1']).sort_values(ascending=False)
    grade_means = df.groupby(['grade','period','skill']).score.mean().unstack('period')
    grade_means['change'] = grade_means['T2']-grade_means['T1']

    fig, ax = plt.subplots(figsize=(8,4.5))
    x = range(4)
    ax.bar([i-.18 for i in x],means['T1'],width=.36,label='T1',color='#376b91')
    ax.bar([i+.18 for i in x],means['T2'],width=.36,label='T2',color='#e1a84c')
    ax.set_xticks(list(x),[LABELS[s] for s in SKILLS])
    ax.set_ylim(0,9); ax.set_ylabel('Mean local rubric score (0–9)')
    ax.set_title('Synthetic example · four separate language skills')
    ax.legend(); ax.grid(axis='y',alpha=.2); fig.tight_layout()
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(FIGURE,format='svg'); plt.close(fig)

    def row(values): return '| '+' | '.join(str(v) for v in values)+' |'
    lines = ['# Synthetic FLE learning evidence', '',
             '**Demonstration only.** Every identifier and score was algorithmically generated. These are local rubric scores out of 9, not CEFR levels or observations of actual pupils.', '',
             '## Cohort means by skill', '',
             '| Skill | T1 / 9 | T2 / 9 | Change |', '|---|---:|---:|---:|']
    for skill in SKILLS:
        lines.append(row([LABELS[skill],f'{means.loc[skill,"T1"]:.2f}',f'{means.loc[skill,"T2"]:.2f}',f'{means.loc[skill,"T2"]-means.loc[skill,"T1"]:+.2f}']))
    lines += ['',f'Each period has {len(df[df.period=="T1"])} skill observations across {df.synthetic_id.nunique()} synthetic learners. Each skill has {int(aggregate[aggregate.period=="T1"].iloc[0]["count"])} observations per period.', '',
              '![Mean scores by skill](skill_progress.svg)', '', '## Grade-level descriptive view', '',
              '| Grade | Skill | T1 / 9 | T2 / 9 | Change |', '|---:|---|---:|---:|---:|']
    for (grade,skill),r in grade_means.iterrows():
        lines.append(row([grade,LABELS[skill],f'{r.T1:.2f}',f'{r.T2:.2f}',f'{r["change"]:+.2f}']))
    lines += ['', '## Instructional interpretation', '',
              f'The largest modeled mean gain is {LABELS[gains.index[0]]} ({gains.iloc[0]:+.2f}); the smallest is {LABELS[gains.index[-1]]} ({gains.iloc[-1]:+.2f}). These patterns are imposed by the simulation and cannot establish that an intervention worked.',
              'Use the table to rehearse a decision cycle: inspect item-level work, choose a targeted task, offer feedback, and reassess the same skill with a fresh prompt. Small synthetic groups and local ordinal scores do not justify inferential claims.', '',
              '## Safeguards', '',
              '- Never replace the synthetic CSV with pupil data in this public repository.',
              '- Keep four skills separate; no overall CEFR label or ranking of individual children.',
              '- Scores with differing support conditions need careful interpretation; the support field is retained for that discussion.',
              '- Reassess a missing task rather than assigning zero; this sample contains no missing observations.', '']
    REPORT.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Wrote {REPORT} and {FIGURE}')


if __name__ == '__main__':
    analyze()
