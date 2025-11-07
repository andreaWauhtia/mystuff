from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

EXCEL_PATH = Path(__file__).with_name("momentum.xlsx")
PLOT_DIR = Path(__file__).resolve().parent / "plots"
OLD_FILES = [
    "momentum_moyen_par_force.png",
    "momentum_moyen_et_cumulatif.png",
    "momentum_cumulatif_par_force.png",
    "tirs_moyens_force_h.png",
    "tirs_moyens_force_l.png",
    "tirs_moyens_force_m.png",
    "momentum_moyen_par_shift.png",
    "momentum_moyen_par_shift_par_force.png",
    "momentum_tous_matches.png",
    "momentum_moyen_par_force_ignore_tilleur.png",
    "momentum_moyen_et_cumulatif_ignore_tilleur.png",
    "momentum_cumulatif_par_force_ignore_tilleur.png",
    "tirs_moyens_force_h_ignore_tilleur.png",
    "tirs_moyens_force_l_ignore_tilleur.png",
    "tirs_moyens_force_m_ignore_tilleur.png",
    "momentum_tous_matches_avec_tilleur.png",
    "momentum_moyen_par_shift_ignore_tilleur.png",
    "momentum_moyen_par_shift_par_force_ignore_tilleur.png",
]
FORCE_COLORS = {"L": "tab:green", "M": "tab:orange", "H": "tab:red"}
INTERVALS = [
    "0-5",
    "5-10",
    "10-15",
    "15-20",
    "20-25",
    "25-30",
    "30-35",
    "35-40",
    "40-45",
    "45-50",
]
TYPE_MAP = {"Tir": "for", "Tirs concédés": "against"}
INTERVAL_BOUNDS = {
    label: tuple(map(int, label.split("-"))) for label in INTERVALS
}
SHIFT_BOUNDARIES = [0, 8, 16, 24, 32, 40, 48, 50]
SHIFT_LABELS = [
    f"{SHIFT_BOUNDARIES[idx]}-{SHIFT_BOUNDARIES[idx + 1]}"
    for idx in range(len(SHIFT_BOUNDARIES) - 1)
]
SHIFT_MAP = {
    SHIFT_LABELS[idx]: (SHIFT_BOUNDARIES[idx], SHIFT_BOUNDARIES[idx + 1])
    for idx in range(len(SHIFT_LABELS))
}


def load_momentum(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df = df.rename(
        columns={
            "Moment": "Type",
            "Unnamed: 11": "Adversaire",
            "Force (L, M, H)": "Force",
        }
    )
    df["Adversaire"] = df["Adversaire"].ffill()
    df["Force"] = df["Force"].ffill()
    df["Type"] = df["Type"].map(TYPE_MAP)
    if df["Type"].isna().any():
        missing_rows = df[df["Type"].isna()]
        raise ValueError(f"Lignes avec type inconnu:\n{missing_rows}")
    df = df.set_index(["Adversaire", "Force", "Type"])[INTERVALS]
    return df.sort_index()


def compute_momentum(for_df: pd.DataFrame, against_df: pd.DataFrame) -> pd.DataFrame:
    momentum_df = for_df.subtract(against_df, fill_value=0)
    momentum_df = momentum_df.reset_index()
    return momentum_df


def compute_shift_momentum(momentum_df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in momentum_df.iterrows():
        totals = {label: 0.0 for label in SHIFT_LABELS}
        durations = {label: 0.0 for label in SHIFT_LABELS}
        for interval in INTERVALS:
            value = row[interval]
            start, end = INTERVAL_BOUNDS[interval]
            interval_length = end - start
            for shift_label, (shift_start, shift_end) in SHIFT_MAP.items():
                overlap = max(0, min(end, shift_end) - max(start, shift_start))
                if overlap <= 0:
                    continue
                totals[shift_label] += value * (overlap / interval_length)
                durations[shift_label] += overlap
        normalized = {}
        for label in SHIFT_LABELS:
            minutes = durations[label]
            if minutes == 0:
                normalized[label] = 0.0
            else:
                normalized[label] = totals[label] * (5.0 / minutes)
        record = {"Adversaire": row["Adversaire"], "Force": row["Force"], **normalized}
        records.append(record)
    return pd.DataFrame(records)


def main() -> None:
    base_df = load_momentum(EXCEL_PATH)
    for_df_all = base_df.xs("for", level="Type")
    against_df_all = base_df.xs("against", level="Type")
    momentum_df_all = compute_momentum(for_df_all, against_df_all)

    without_tilleur_df = base_df.drop(index="Tilleur", level="Adversaire", errors="ignore")
    for_df_without = without_tilleur_df.xs("for", level="Type")
    against_df_without = without_tilleur_df.xs("against", level="Type")
    momentum_df_without = compute_momentum(for_df_without, against_df_without)

    mean_global = momentum_df_all[INTERVALS].mean()
    mean_by_force = momentum_df_all.groupby("Force")[INTERVALS].mean()
    cumulative_global = mean_global.cumsum()
    cumulative_by_force = mean_by_force.cumsum(axis=1)

    mean_for_by_force = for_df_all.groupby(level="Force")[INTERVALS].mean()
    mean_against_by_force = against_df_all.groupby(level="Force")[INTERVALS].mean()

    shift_df_all = compute_shift_momentum(momentum_df_all)
    mean_shift = shift_df_all[SHIFT_LABELS].mean()
    mean_shift_by_force_all = shift_df_all.groupby("Force")[SHIFT_LABELS].mean()

    shift_df_without = compute_shift_momentum(momentum_df_without)
    mean_shift_by_force_without = shift_df_without.groupby("Force")[SHIFT_LABELS].mean()

    PLOT_DIR.mkdir(exist_ok=True)
    for old_name in OLD_FILES:
        old_path = PLOT_DIR / old_name
        if old_path.exists():
            old_path.unlink()
    for match_file in PLOT_DIR.glob("momentum_match_*.png"):
        match_file.unlink()

    print("Momentum moyen global par intervalle:")
    print(mean_global.round(3))
    print("\nMomentum moyen par force:")
    print(mean_by_force.round(3))
    print("\nMomentum cumulatif global:")
    print(cumulative_global.round(3))
    print("\nMomentum cumulatif par force:")
    print(cumulative_by_force.round(3))
    print("\nMomentum moyen par shift (tous matches):")
    print(mean_shift.round(3))
    print("\nMomentum moyen par shift et par force (tous matches):")
    print(mean_shift_by_force_all.round(3))
    print("\nMomentum moyen par shift et par force (sans Tilleur):")
    print(mean_shift_by_force_without.round(3))

    fig, ax = plt.subplots(figsize=(10, 6))
    for force in mean_by_force.index:
        ax.plot(INTERVALS, mean_by_force.loc[force], marker="o", label=f"Force {force}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentum moyen par intervalle selon force adverse")
    ax.set_xlabel("Intervalle (minutes)")
    ax.set_ylabel("Momentum moyen")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "momentum_moyen_par_force.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(INTERVALS, mean_global, marker="o", label="Momentum moyen global")
    ax.plot(
        INTERVALS,
        cumulative_global,
        marker="s",
        linestyle="--",
        label="Momentum cumulatif global",
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentum moyen et cumulatif (global)")
    ax.set_xlabel("Intervalle (minutes)")
    ax.set_ylabel("Momentum")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "momentum_moyen_et_cumulatif.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    for force in cumulative_by_force.index:
        ax.plot(
            INTERVALS,
            cumulative_by_force.loc[force],
            marker="o",
            label=f"Cumul Force {force}",
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentum cumulatif moyen par force adverse")
    ax.set_xlabel("Intervalle (minutes)")
    ax.set_ylabel("Momentum cumulatif")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "momentum_cumulatif_par_force.png", dpi=150)
    plt.close(fig)

    for force in mean_for_by_force.index:
        fig, ax = plt.subplots(figsize=(10, 6))
        mean_for = mean_for_by_force.loc[force]
        mean_against = mean_against_by_force.loc[force]
        ax.bar(INTERVALS, mean_for, width=0.6, label="Tirs pour (moyen)")
        ax.bar(
            INTERVALS,
            -mean_against,
            width=0.6,
            label="Tirs contre (moyen)",
            alpha=0.8,
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(f"Tirs moyens pour/contre — Force {force}")
        ax.set_xlabel("Intervalle (minutes)")
        ax.set_ylabel("Nombre moyen de tirs (négatif = contre)")
        max_abs = max(mean_for.max(), mean_against.max())
        if max_abs == 0:
            max_abs = 1.0
        ax.set_ylim(-max_abs * 1.1, max_abs * 1.1)
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        outfile = PLOT_DIR / f"tirs_moyens_force_{force.lower()}.png"
        fig.savefig(outfile, dpi=150)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(SHIFT_LABELS, mean_shift, color="tab:blue")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentum moyen par shift")
    ax.set_xlabel("Shift (minutes)")
    ax.set_ylabel("Momentum moyen")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "momentum_moyen_par_shift.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    for force in mean_shift_by_force_all.index:
        label = f"Force {force}"
        ax.plot(
            SHIFT_LABELS,
            mean_shift_by_force_all.loc[force],
            marker="o",
            label=label,
            color=FORCE_COLORS.get(force, "tab:gray"),
        )
    if "H" in mean_shift_by_force_without.index:
        ax.plot(
            SHIFT_LABELS,
            mean_shift_by_force_without.loc["H"],
            marker="s",
            linestyle="--",
            label="Force H (sans Tilleur)",
            color=FORCE_COLORS.get("H", "tab:gray"),
            alpha=0.8,
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentum moyen par shift selon force adverse")
    ax.set_xlabel("Shift (minutes)")
    ax.set_ylabel("Momentum moyen")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(
        PLOT_DIR / "momentum_moyen_par_shift_par_force.png",
        dpi=150,
    )
    plt.close(fig)

    # Graphe momentum par match (Tilleur inclus)
    momentum_plot_df = momentum_df_all.drop_duplicates(subset=["Adversaire", "Force"]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    cmap = plt.colormaps["tab20"].resampled(max(1, len(momentum_plot_df)))
    markers = ["o", "s", "^", "D", "v", "P", "X", "*", "h", "+"]
    for idx, row in momentum_plot_df.iterrows():
        adversaire = row["Adversaire"]
        force = row["Force"]
        color = cmap(idx)
        marker = markers[idx % len(markers)]
        ax.plot(
            INTERVALS,
            row[INTERVALS],
            marker=marker,
            linestyle="-",
            label=f"{adversaire} (Force {force})",
            color=color,
            alpha=0.85,
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Momentums par match (Tilleur inclus)")
    ax.set_xlabel("Intervalle (minutes)")
    ax.set_ylabel("Momentum (pour - contre)")
    ax.grid(alpha=0.3)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "momentum_tous_matches.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()