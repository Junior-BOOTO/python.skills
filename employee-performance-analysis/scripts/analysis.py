"""Exploratory employee performance analysis with reproducible CSV and PNG outputs.

Run from the repository root:
    python employee-performance-analysis/scripts/analysis.py --input path/to/HR_Analytics.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
ALIASES = {
    "PerformanceScore": ("PerformanceScore", "PerformanceRating", "Performance Score"),
    "HoursWorked": ("HoursWorked", "Hours Worked", "WorkHours"),
    "Department": ("Department",),
    "OverTime": ("OverTime", "Overtime"),
}


def load_data(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"CSV introuvable : {path}. Voir le README.")
    data = pd.read_csv(path)
    data.columns = data.columns.astype(str).str.strip()
    rename = {}
    for canonical, options in ALIASES.items():
        candidate = next((name for name in options if name in data.columns), None)
        if candidate and candidate != canonical:
            rename[candidate] = canonical
    data = data.rename(columns=rename)
    if "PerformanceScore" not in data:
        raise ValueError(
            "Colonne de performance manquante. Colonnes acceptées : "
            + ", ".join(ALIASES["PerformanceScore"])
            + ". Colonnes trouvées : " + ", ".join(data.columns)
        )
    for name in ("PerformanceScore", "HoursWorked"):
        if name in data:
            data[name] = pd.to_numeric(data[name], errors="coerce")
    if data["PerformanceScore"].notna().sum() == 0:
        raise ValueError("Aucune valeur numérique exploitable pour PerformanceScore.")
    return data


def iqr_outliers(data: pd.DataFrame, column: str) -> tuple[pd.DataFrame, tuple[float, float]]:
    values = data[column].dropna()
    if values.empty:
        return data.iloc[0:0].copy(), (float("nan"), float("nan"))
    q1, q3 = values.quantile([0.25, 0.75])
    spread = q3 - q1
    lower, upper = q1 - 1.5 * spread, q3 + 1.5 * spread
    return data.loc[data[column].lt(lower) | data[column].gt(upper)].copy(), (lower, upper)


def save_plot(filename: str, figures: Path) -> None:
    plt.tight_layout()
    plt.savefig(figures / filename, dpi=160, bbox_inches="tight")
    plt.close()


def run(input_path: Path, output_dir: Path) -> dict[str, object]:
    data = load_data(input_path)
    figures, tables = output_dir / "figures", output_dir / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    numeric = data.select_dtypes(include="number")
    numeric.describe().T.to_csv(tables / "descriptive_statistics.csv", index_label="variable")
    report = {"rows": len(data), "columns": list(data.columns), "missing": data.isna().sum().to_dict()}

    sns.histplot(data=data, x="PerformanceScore", bins="auto")
    plt.title("Distribution des performances")
    save_plot("01_performance_distribution.png", figures)

    sns.boxplot(data=data, x="PerformanceScore")
    plt.title("Performances : dispersion et valeurs atypiques")
    save_plot("02_performance_boxplot.png", figures)

    outliers, bounds = iqr_outliers(data, "PerformanceScore")
    outliers.to_csv(tables / "performance_outliers.csv", index=False)
    report["performance_iqr_bounds"] = bounds
    report["performance_outliers"] = len(outliers)

    if "HoursWorked" in data and data["HoursWorked"].notna().any():
        sns.histplot(data=data, x="HoursWorked", bins="auto")
        plt.title("Distribution des heures travaillées")
        save_plot("03_hours_distribution.png", figures)
        sns.boxplot(data=data, x="HoursWorked")
        plt.title("Heures travaillées : dispersion")
        save_plot("04_hours_boxplot.png", figures)
        hours_outliers, hour_bounds = iqr_outliers(data, "HoursWorked")
        hours_outliers.to_csv(tables / "hours_worked_outliers.csv", index=False)
        combined = data.loc[data.index.isin(outliers.index) | data.index.isin(hours_outliers.index)]
        combined.to_csv(tables / "combined_outliers.csv", index=False)
        report["hours_iqr_bounds"] = hour_bounds
        report["hours_outliers"] = len(hours_outliers)
        valid = data[["HoursWorked", "PerformanceScore"]].dropna()
        if len(valid) > 1:
            sns.scatterplot(data=valid, x="HoursWorked", y="PerformanceScore")
            plt.title("Heures travaillées et performance")
            save_plot("05_hours_vs_performance.png", figures)

    if "Department" in data:
        group = data.groupby("Department", dropna=False)["PerformanceScore"].agg(["count", "mean", "median"])
        group.to_csv(tables / "performance_by_department.csv")
        if not group.empty:
            sns.boxplot(data=data, x="PerformanceScore", y="Department")
            plt.title("Performance par département")
            save_plot("06_performance_by_department.png", figures)

    if "OverTime" in data:
        group = data.groupby("OverTime", dropna=False)["PerformanceScore"].agg(["count", "mean", "median"])
        group.to_csv(tables / "performance_by_overtime.csv")
        if not group.empty:
            sns.boxplot(data=data, x="OverTime", y="PerformanceScore")
            plt.title("Performance selon les heures supplémentaires")
            save_plot("07_performance_by_overtime.png", figures)

    if numeric.shape[1] >= 2:
        corr = numeric.corr(numeric_only=True).dropna(how="all").dropna(axis=1, how="all")
        corr.to_csv(tables / "correlations.csv")
        if not corr.empty:
            sns.heatmap(corr, annot=corr.shape[0] <= 12, cmap="coolwarm", center=0)
            plt.title("Corrélations numériques")
            save_plot("08_correlation_heatmap.png", figures)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "HR_Analytics.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs")
    args = parser.parse_args()
    summary = run(args.input, args.output)
    print(f"Analyse terminée : {summary['rows']} lignes ; {summary['performance_outliers']} valeurs atypiques de performance.")
    print(f"Résultats : {args.output.resolve()}")


if __name__ == "__main__":
    main()
