"""Collecte locale, exploration et ACP descriptive du jeu UCI Wine Quality."""
from pathlib import Path
import hashlib
import json
import importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parent
FEATURES = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
            'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
            'pH', 'sulphates', 'alcohol']

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def fit_pca(frame):
    scaler = StandardScaler()
    z = scaler.fit_transform(frame[FEATURES])
    pca = PCA(svd_solver='full').fit(z)
    scores = pca.transform(z)
    assert np.isclose(pca.explained_variance_ratio_.sum(), 1)
    assert np.allclose(pca.inverse_transform(scores), z, atol=1e-10)
    return scaler, pca, scores

def main():
    for folder in ['collected', 'analysis', 'models', 'reports']:
        (ROOT / folder).mkdir(exist_ok=True)
    frames = []
    sources = []
    for color in ['red', 'white']:
        path = ROOT / 'raw' / f'winequality-{color}.csv'
        df = pd.read_csv(path, sep=';')
        assert list(df.columns) == FEATURES + ['quality']
        df['color'] = color
        df['source_row'] = np.arange(1, len(df) + 1)
        frames.append(df)
        sources.append({'file': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'rows': len(df)})
    data = pd.concat(frames, ignore_index=True)
    assert len(data) == 6497 and data.isna().sum().sum() == 0
    assert np.isfinite(data[FEATURES].to_numpy()).all()
    assert data['quality'].between(0, 10).all()
    data.to_csv(ROOT / 'collected' / 'vins.csv', index=False)
    duplicates = int(data.duplicated(FEATURES + ['quality', 'color']).sum())
    quality = {'rows': len(data), 'red': len(frames[0]), 'white': len(frames[1]),
               'missing_cells': int(data.isna().sum().sum()), 'repeated_profiles': duplicates,
               'quality_min': int(data.quality.min()), 'quality_max': int(data.quality.max())}
    write_json(ROOT / 'reports' / 'qualite.json', quality)
    # Les profils répétés restent : aucun identifiant ne permet de confirmer un doublon technique.
    data.groupby('color')[FEATURES + ['quality']].describe().to_csv(ROOT / 'analysis' / 'statistiques.csv')
    data.groupby(['color', 'quality']).size().rename('count').to_csv(ROOT / 'analysis' / 'qualite_par_couleur.csv')
    scaler, pca, scores = fit_pca(data)
    ratios = pca.explained_variance_ratio_
    cumulative = np.cumsum(ratios)
    k80 = int(np.searchsorted(cumulative, .8) + 1)
    variance = pd.DataFrame({'component': np.arange(1, 12), 'variance_ratio': ratios, 'cumulative_ratio': cumulative})
    variance.to_csv(ROOT / 'analysis' / 'variance_expliquee.csv', index=False)
    # Corrélations empiriques variables/composantes ; distinctes des coefficients des axes.
    z = scaler.transform(data[FEATURES])
    correlations = np.corrcoef(z.T, scores.T)[:11, 11:]
    pd.DataFrame(pca.components_.T, index=FEATURES, columns=[f'PC{i+1}' for i in range(11)]).to_csv(ROOT / 'analysis' / 'coefficients_axes.csv')
    pd.DataFrame(correlations, index=FEATURES, columns=[f'PC{i+1}' for i in range(11)]).to_csv(ROOT / 'analysis' / 'correlations_axes.csv')
    # Export numérique transparent, sans pickle. Application : standardiser puis multiplier.
    np.savez(ROOT / 'models' / 'acp.npz', mean=scaler.mean_, scale=scaler.scale_,
             pca_mean=pca.mean_, components=pca.components_, variance_ratio=ratios)
    with np.load(ROOT / 'models' / 'acp.npz', allow_pickle=False) as saved:
        new_scores = ((data[FEATURES].iloc[:5].to_numpy() - saved['mean']) / saved['scale'] - saved['pca_mean']) @ saved['components'].T
    assert np.allclose(new_scores, scores[:5])
    pd.DataFrame(scores[:, :3], columns=['PC1', 'PC2', 'PC3']).assign(color=data.color, quality=data.quality, source_row=data.source_row).to_csv(ROOT / 'analysis' / 'coordonnees.csv', index=False)
    sensitivity = []
    for name, frame in [('pooled', data), ('unique_profiles', data.drop_duplicates(FEATURES + ['quality', 'color'])), ('red', frames[0]), ('white', frames[1])]:
        _, fitted, _ = fit_pca(frame)
        c = np.cumsum(fitted.explained_variance_ratio_)
        sensitivity.append({'scope': name, 'rows': len(frame), 'variance_2d': float(c[1]), 'variance_3d': float(c[2]), 'components_80pct': int(np.searchsorted(c, .8)+1)})
    pd.DataFrame(sensitivity).to_csv(ROOT / 'analysis' / 'sensibilite.csv', index=False)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(np.arange(1, 12), ratios*100, color='#167d8d', label='Par composante')
    ax.plot(np.arange(1, 12), cumulative*100, '-o', color='#d57633', label='Cumul')
    ax.axhline(80, ls='--', color='gray', label='Repère descriptif 80 %')
    ax.set(xlabel='Composante principale', ylabel='Variance expliquée (%)', title='Wine Quality · ACP sur 11 variables standardisées', xticks=np.arange(1,12), ylim=(0,105))
    ax.legend(); fig.tight_layout(); fig.savefig(ROOT / 'reports' / 'variance.png', dpi=150); plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for color, label, shade in [('red', 'Vins rouges', '#b84949'), ('white', 'Vins blancs', '#247f9e')]:
        mask = data.color.eq(color)
        axes[0].scatter(scores[mask,0], scores[mask,1], s=8, alpha=.22, color=shade, label=label, rasterized=True)
    axes[0].legend(); axes[0].set_title('Coloration par type de vin')
    plot = axes[1].scatter(scores[:,0], scores[:,1], c=data.quality, s=8, alpha=.35, cmap='viridis', vmin=0, vmax=10, rasterized=True)
    axes[1].set_title('Note sensorielle, exclue du calcul de l’ACP'); fig.colorbar(plot, ax=axes[1], label='Qualité (0–10)')
    for ax in axes:
        ax.set(xlabel=f'PC1 ({ratios[0]*100:.1f} %)', ylabel=f'PC2 ({ratios[1]*100:.1f} %)'); ax.axhline(0,color='gray',lw=.5); ax.axvline(0,color='gray',lw=.5)
    fig.suptitle('Wine Quality · Plan principal (toutes les observations)'); fig.tight_layout(); fig.savefig(ROOT / 'reports' / 'projection.png', dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 8))
    circle = plt.Circle((0,0), 1, color='#bcc8d4', fill=False); ax.add_patch(circle)
    for i, feature in enumerate(FEATURES):
        x, y = correlations[i,:2]
        ax.arrow(0,0,x,y,color='#167d8d',head_width=.025,length_includes_head=True)
        offset = (0, 15) if feature == 'total sulfur dioxide' else ((0, -8) if feature == 'free sulfur dioxide' else (0, 0))
        ax.annotate(feature, (x*1.08,y*1.08), xytext=offset, textcoords='offset points', fontsize=8,ha='center')
    ax.set(xlim=(-1.25,1.25),ylim=(-1.25,1.25),xlabel='Corrélation avec PC1',ylabel='Corrélation avec PC2',title='Cercle des corrélations · Variables chimiques')
    ax.set_aspect('equal'); ax.axhline(0,color='gray',lw=.5); ax.axvline(0,color='gray',lw=.5)
    fig.tight_layout(); fig.savefig(ROOT / 'reports' / 'correlations.png',dpi=150); plt.close(fig)
    summary = {**quality, 'features': 11, 'variance_2d': float(cumulative[1]), 'variance_3d': float(cumulative[2]), 'components_80pct': k80,
               'pc1_top': sorted(zip(FEATURES,correlations[:,0]),key=lambda x:abs(x[1]),reverse=True)[:4],
               'pc2_top': sorted(zip(FEATURES,correlations[:,1]),key=lambda x:abs(x[1]),reverse=True)[:4]}
    write_json(ROOT / 'reports' / 'resultats.json',summary)
    versions = {name: importlib.metadata.version(name) for name in ['pandas','numpy','scikit-learn','matplotlib']}
    (ROOT / 'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest = {'objective': 'ACP descriptive des profils chimiques des vins, sans prédiction ni segmentation de clients.', 'source': 'https://archive.ics.uci.edu/dataset/186/wine+quality', 'doi': '10.24432/C56S3T', 'license': 'CC BY 4.0', 'raw_sources': sources, 'target': None, 'horizon': None, 'steps': {'DataCollect': 'completed', 'DataAnalyse': 'completed', 'DataML': 'completed'}, 'model_scope': 'ACP exploratoire, ajustée à toutes les observations ; aucune performance hors échantillon revendiquée.', 'transformations': ['Fusion avec couleur et ligne source', 'Profils répétés conservés ; sensibilité sans répétitions', 'Standardisation des 11 variables chimiques, qualité et couleur exclues de l’ACP'], 'versions': versions, 'verification': ['6497 lignes, 0 valeur manquante', 'Somme des ratios de variance = 1', 'Reconstruction avec les 11 axes', 'Rechargement numérique et projection de 5 observations'], 'files': sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name != 'manifest.json'), 'next_action': 'Interpréter les axes ; ne pas déduire de segments clients de ces données.'}
    write_json(ROOT / 'manifest.json',manifest)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
