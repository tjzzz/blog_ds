#!/usr/bin/env python3
"""
Estimate the honest sample-size / MDE benefit of a log(1 + X/c) transform.

Core idea (apples-to-apples, same-DGP):
  1. Use the CONTROL group's empirical distribution as the data-generating truth.
  2. Counterfactual treatment = control * (1 + r)   (multiplicative relative lift r).
  3. Raw  analysis: two-sample mean difference on X.
     Log  analysis: two-sample mean difference on Y = log(1 + X/c).
  4. For SAME true lift r, compute required n per arm (alpha, power) for each scale.
       n_raw = (z_{1-a/2}+z_{1-b})^2 * (Var_c + Var_t) / delta^2
  5. Benefit_n = 1 - n_log / n_raw      (== 1 - (MDE_log/MDE_raw)^2)
     Benefit_MDE = 1 - MDE_log/MDE_raw  (= 1 - sqrt(1 - Benefit_n))
  6. Bootstrap over control units for CI; sweep c for sensitivity.

Why not just compare Var(X) vs Var(log(1+X/c)) directly?
  They live on different scales (Var(X) has units^2, Var(Y) is dimensionless).
  Comparing them is meaningless. You MUST anchor the comparison on the same
  estimand (relative lift r) and compare required n or MDE. This script does that.

Usage:
  python estimate_transform_benefit.py --data data.csv --group-col group --x-col x
  python estimate_transform_benefit.py --data data.csv --r 0.03 --power 0.8 --alpha 0.05 --boot 1000

CSV needs: one row per user, a group column (0/1 or control/treatment), an x column (>=0).
The treatment group is optional (used only as a reality check); the benefit
calculation itself only needs the control distribution.
"""
import argparse
import csv
import math
import sys
from statistics import NormalDist

import numpy as np

Z = NormalDist()


def zq(p):
    return Z.inv_cdf(p)


def read_csv(path, gcol, xcol):
    gc, tc = [], []
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        if gcol not in rd.fieldnames or xcol not in rd.fieldnames:
            sys.exit(f"CSV must contain columns '{gcol}' and '{xcol}'. Got: {rd.fieldnames}")
        for row in rd:
            try:
                x = float(row[xcol])
            except (TypeError, ValueError):
                continue
            if not (x == x) or x < 0:  # NaN / negative guard
                continue
            g = str(row[gcol]).strip().lower()
            if g in ("1", "t", "test", "treatment", "exp", "b"):
                is_t = True
            elif g in ("0", "c", "control", "base", "a"):
                is_t = False
            else:
                try:
                    is_t = float(g) >= 0.5
                except ValueError:
                    continue
            (tc if is_t else gc).append(x)
    return np.asarray(gc, float), np.asarray(tc, float)


def ytrans(x, c):
    """log(1 + x/c). Requires x >= 0, c > 0."""
    return np.log1p(x / c)


def n_per_arm(var_c, var_t, delta, alpha, power):
    if delta <= 0 or (var_c + var_t) <= 0:
        return float("inf")
    return (zq(1 - alpha / 2) + zq(power)) ** 2 * (var_c + var_t) / (delta ** 2)


def mde_abs(var_c, var_t, n_per, alpha, power):
    return (zq(1 - alpha / 2) + zq(power)) * math.sqrt((var_c + var_t) / n_per)


def delta_log_empirical(xc, r, c):
    """Theoretical mean effect on Y-scale when control x is lifted by (1+r)."""
    return float(np.mean(np.log((c + (1.0 + r) * xc) / (c + xc))))


def eu_empirical(xc, c):
    """E[X/(c+X)] on control -- the 'transmission' factor."""
    return float(np.mean(xc / (c + xc)))


def r_from_deltaY(xc, c, dy, lo=0.0, hi=5.0):
    """Invert dy = E[log(1 + r*u)] for r."""
    if dy <= 0:
        return 0.0
    for _ in range(100):
        m = 0.5 * (lo + hi)
        if delta_log_empirical(xc, m, c) < dy:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def compute_benefit(xc, r, c, alpha, power, n_fixed=None):
    """Return dict of honest benefit metrics for a given c."""
    xc = np.asarray(xc, float)
    xt = xc * (1.0 + r)

    # ---- raw scale ----
    mu_c, mu_t = xc.mean(), xt.mean()
    var_c, var_t = xc.var(ddof=1), xt.var(ddof=1)
    delta_raw = mu_t - mu_c
    n_raw = n_per_arm(var_c, var_t, delta_raw, alpha, power)

    # ---- log(1+x/c) scale ----
    yc, yt = ytrans(xc, c), ytrans(xt, c)
    vYc, vYt = yc.var(ddof=1), yt.var(ddof=1)
    delta_Y = yt.mean() - yc.mean()
    n_log = n_per_arm(vYc, vYt, delta_Y, alpha, power)

    benefit_n = 1.0 - n_log / n_raw if n_raw not in (0, float("inf")) else float("nan")
    mde_ratio = math.sqrt(n_log / n_raw) if n_raw not in (0, float("inf")) else float("nan")
    benefit_mde = 1.0 - mde_ratio

    out = {
        "c": c,
        "cv_raw": math.sqrt(var_c) / mu_c if mu_c else float("nan"),
        "var_log": vYc,
        "delta_Y": delta_Y,
        "Eu": eu_empirical(xc, c),          # E[X/(c+X)]
        "n_raw": n_raw,
        "n_log": n_log,
        "benefit_n": benefit_n,
        "benefit_mde": benefit_mde,
    }
    if n_fixed:
        mde_raw = mde_abs(var_c, var_t, n_fixed, alpha, power)
        mde_log = mde_abs(vYc, vYt, n_fixed, alpha, power)
        out["mde_raw_rel"] = mde_raw / mu_c
        out["mde_log_rel"] = r_from_deltaY(xc, c, mde_log)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--group-col", default="group")
    ap.add_argument("--x-col", default="x")
    ap.add_argument("--r", type=float, default=0.05, help="true relative lift to detect")
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--n-fixed", type=int, default=None, help="for MDE at fixed n per arm")
    ap.add_argument("--out-prefix", default="transform_benefit")
    args = ap.parse_args()

    xc, xt = read_csv(args.data, args.group_col, args.x_col)
    if len(xc) < 30:
        sys.exit(f"Need >=30 control rows, got {len(xc)}")

    mu_c = xc.mean()
    n_fixed = args.n_fixed or int(len(xc))

    print("=" * 74)
    print("INPUT")
    print(f"  control n={len(xc)}  mean={mu_c:.4g}  sd={xc.std(ddof=1):.4g}"
          f"  zeros={np.mean(xc == 0):.1%}")
    print(f"  treatment n={len(xt)}" + (f"  mean={xt.mean():.4g}" if len(xt) else "  (none)"))
    print(f"  target relative lift r={args.r:.3%}  power={args.power}  alpha={args.alpha}")
    print(f"  MDE reference n per arm = {n_fixed}")

    # ---- c grid: relative to control mean ----
    c_grid = []
    if mu_c > 0:
        c_grid = [mu_c * f for f in (0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0)]
    c_grid = sorted(set([c for c in c_grid if c > 0]))

    results = []
    for c in c_grid:
        results.append(compute_benefit(xc, args.r, c, args.alpha, args.power, n_fixed))

    # ---- bootstrap CI on benefit_n for each c ----
    rng = np.random.default_rng(42)
    n = len(xc)
    boot_benefit = {c: [] for c in c_grid}
    for _ in range(args.boot):
        idx = rng.integers(0, n, n)
        xb = xc[idx]
        for c in c_grid:
            b = compute_benefit(xb, args.r, c, args.alpha, args.power)
            boot_benefit[c].append(b["benefit_n"])
    for res in results:
        arr = np.asarray(boot_benefit[res["c"]])
        arr = arr[np.isfinite(arr)]
        if len(arr):
            res["benefit_n_lo"] = float(np.percentile(arr, 2.5))
            res["benefit_n_hi"] = float(np.percentile(arr, 97.5))
        else:
            res["benefit_n_lo"] = res["benefit_n_hi"] = float("nan")

    # ---- report table ----
    hdr = (f"{'c/mean':>7} {'E[X/(c+X)]':>11} {'Var(log)':>9} "
           f"{'n_raw':>10} {'n_log':>10} {'benefit_n':>10} {'95%CI':>17} {'benefit_MDE':>12}")
    print("\n" + "=" * 74)
    print("HONEST BENEFIT (same-DGP, same true lift r)")
    print(hdr)
    print("-" * len(hdr))
    for res in results:
        cr = res["c"] / mu_c
        ci = f"[{res['benefit_n_lo']:.1%},{res['benefit_n_hi']:.1%}]"
        print(f"{cr:7.3g} {res['Eu']:11.3f} {res['var_log']:9.3f} "
              f"{res['n_raw']:10.0f} {res['n_log']:10.0f} "
              f"{res['benefit_n']:10.1%} {ci:>17} {res['benefit_mde']:12.1%}")

    # ---- recommendations ----
    best = max(results, key=lambda d: d["benefit_n"])
    print("\n" + "=" * 74)
    print("READING")
    print(f"  max benefit_n = {best['benefit_n']:.1%} at c = {best['c']/mu_c:.3g} x mean")
    print(f"  at that c: E[X/(c+X)] = {best['Eu']:.3f}  "
          f"(log-scale effect is ~{best['Eu']:.0%} of relative lift r)")
    print(f"  theoretical delta_Y at best c = {best['delta_Y']:.5f}  "
          f"vs r*E[u] = {args.r * best['Eu']:.5f}  (should match for small r)")

    if len(xt):
        obs = np.mean(ytrans(xt, best["c"])) - np.mean(ytrans(xc, best["c"])) \
            if best["c"] > 0 else float("nan")
        print(f"\n  REALITY CHECK: observed delta_Y (best c) = {obs:.5f}")
        print(f"                 theoretical delta_Y(r)   = {best['delta_Y']:.5f}")

    print("\n  CAVEAT: benefit is monotone in skew; if your data has heavy tail + zeros,")
    print("  the '90%' can be real BUT is c-dependent and comes with a shrunken estimand.")
    print("  Compare against CUPED (pre-period covariate) before committing to log.")

    # ---- write outputs ----
    import os
    outdir = os.path.dirname(os.path.abspath(args.data))
    csv_path = os.path.join(outdir, f"{args.out_prefix}_vs_c.csv")
    keys = ["c", "Eu", "cv_raw", "var_log", "delta_Y", "n_raw", "n_log",
            "benefit_n", "benefit_n_lo", "benefit_n_hi", "benefit_mde"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for res in results:
            w.writerow({k: res.get(k) for k in keys})
    print(f"\n[wrote] {csv_path}")


if __name__ == "__main__":
    main()
