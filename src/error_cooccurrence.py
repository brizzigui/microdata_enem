from utils.read import read_error_data
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from pathlib import Path
import time
import warnings

warnings.filterwarnings('ignore', category=FutureWarning, message='.*Downcasting object dtype.*')

def mine_association_rules(df: pd.DataFrame, min_support: float = 0.5, 
                           min_confidence: float = 0.6, max_len: int = 2,
                           min_lift: float | None = None) -> pd.DataFrame:
    
    print(f"Mining Association Rules")
    print(f"Parameters:")
    print(f"  min_support: {min_support}")
    print(f"  min_confidence: {min_confidence}")
    print(f"  max_len: {max_len}")
    print(f"  min_lift: {min_lift}")
    
    start_time = time.time()
    
    print("\nRunning Apriori algorithm...")
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True, 
                                max_len=max_len, verbose=1, low_memory=True)
    
    print(f"  Found {len(frequent_itemsets)} frequent itemsets")
    
    if len(frequent_itemsets) == 0:
        print("  WARNING: No frequent itemsets found. Try lowering min_support.")
        return pd.DataFrame()

    print("\nGenerating association rules...")
    rules = association_rules(frequent_itemsets, metric="confidence", 
                              min_threshold=min_confidence, num_itemsets=len(frequent_itemsets))
    
    print(f"  Found {len(rules)} association rules")
    
    if len(rules) == 0:
        print("  WARNING: No rules found. Try lowering min_confidence.")
        return pd.DataFrame()
    
    if min_lift is not None:
        before_count = len(rules)
        rules = rules[rules['lift'] >= min_lift]
        after_count = len(rules)
        print(f"  Filtered rules by min_lift >= {min_lift}: {before_count} -> {after_count}")
        if len(rules) == 0:
            print("  WARNING: No rules remain after applying min_lift filter. Try lowering min_lift or min_confidence.")
            return pd.DataFrame()

    rules = rules.sort_values('confidence', ascending=False)
    
    elapsed_time = time.time() - start_time
    print(f"\nMining completed in {elapsed_time:.2f} seconds")
    
    return rules


def format_itemset(itemset):

    try:
        items = sorted(list(itemset))
    except Exception:
        items = list(itemset)

    if 'COLUMN_MAPPING' in globals() and globals()['COLUMN_MAPPING'] is not None:
        mapping = globals()['COLUMN_MAPPING']
        mapped = []
        for i in items:
            try:
                idx = int(i)
            except Exception:
                idx = None
            if idx is not None and 0 <= idx < len(mapping):
                mapped.append(mapping[idx])
            else:
                mapped.append(f"idx_{i}")
        return "{" + ", ".join(mapped) + "}"

    areas = ["CN", "CH", "LC", "MT"]
    items = sorted([int(i) for i in items])
    items = [f"q_{areas[i//45]}_{i%45}" for i in items]
    return "{" + ", ".join(items) + "}"


def save_rules(rules: pd.DataFrame, year: int, top_n: int = 50):

    output_dir = Path("output/error_cooccurrence")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"association_rules_{year}_top{top_n}.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"CO-OCORRÊNCIA DE ERROS - ENEM {year}\n")
        f.write(f"TOP {top_n} REGRAS DE ASSOCIAÇÃO\n\n")
        
        top_rules = rules.head(top_n)
        
        for idx, rule in top_rules.iterrows():
            antecedent = format_itemset(rule['antecedents'])
            consequent = format_itemset(rule['consequents'])
            
            f.write(f"Rule #{idx + 1}:\n")
            f.write(f"  {antecedent} => {consequent}\n")
            f.write(f"  Support:    {rule['support']:.4f} ({rule['support']*100:.2f}%)\n")
            f.write(f"  Confidence: {rule['confidence']:.4f} ({rule['confidence']*100:.2f}%)\n")
            f.write(f"  Lift:       {rule['lift']:.4f}\n")
            f.write(f"  Conviction: {rule['conviction']:.4f}\n")
            f.write("\n")
    
    print(f"\nTop {top_n} rules saved to: {output_path}")


def print_rules_summary(rules: pd.DataFrame, top_n: int = 10):

    print(f"TOP {top_n} ASSOCIATION RULES (by confidence)")
    
    top_rules = rules.head(top_n)
    
    for idx, rule in top_rules.iterrows():
        antecedent = format_itemset(rule['antecedents'])
        consequent = format_itemset(rule['consequents'])
        
        print(f"Rule #{idx + 1}:")
        print(f"  {antecedent} => {consequent}")
        print(f"  Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}, Lift: {rule['lift']:.4f}")
        print()


def analyze_rules_statistics(rules: pd.DataFrame, year: int):

    output_dir = Path("output/error_cooccurrence")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"rules_statistics_{year}.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"ASSOCIATION RULES STATISTICS - ENEM {year}\n\n")
        
        f.write(f"Total rules found: {len(rules)}\n\n")
        
        f.write("Support Statistics:\n")
        f.write(f"  Mean:   {rules['support'].mean():.4f}\n")
        f.write(f"  Median: {rules['support'].median():.4f}\n")
        f.write(f"  Min:    {rules['support'].min():.4f}\n")
        f.write(f"  Max:    {rules['support'].max():.4f}\n\n")
        
        f.write("Confidence Statistics:\n")
        f.write(f"  Mean:   {rules['confidence'].mean():.4f}\n")
        f.write(f"  Median: {rules['confidence'].median():.4f}\n")
        f.write(f"  Min:    {rules['confidence'].min():.4f}\n")
        f.write(f"  Max:    {rules['confidence'].max():.4f}\n\n")
        
        f.write("Lift Statistics:\n")
        f.write(f"  Mean:   {rules['lift'].mean():.4f}\n")
        f.write(f"  Median: {rules['lift'].median():.4f}\n")
        f.write(f"  Min:    {rules['lift'].min():.4f}\n")
        f.write(f"  Max:    {rules['lift'].max():.4f}\n\n")
        
        rules['antecedent_len'] = rules['antecedents'].apply(len)
        
        f.write("Rules by antecedent size:\n")
        for size in sorted(rules['antecedent_len'].unique()):
            count = (rules['antecedent_len'] == size).sum()
            f.write(f"  Size {size}: {count} rules\n")
    
    print(f"Statistics saved to: {output_path}")


def main():

    print("ERROR CO-OCCURRENCE ANALYSIS - ENEM")
    print("\nParameters:")
    print("  - min_support: 0.3 (30% of students)")
    print("  - min_confidence: 0.6 (60%)")
    print("  - max_items: 3")
    print("  - top_rules: 50 per year")
    
    # Configurações
    years = [2020, 2021, 2022, 2023, 2024]
    min_support = 0.5
    min_confidence = 0.8
    max_len = 2
    min_lift = 1.05
    top_n = 50
        
    for year in years:
        try:
            res = read_error_data(year, max_rows=None, return_mapping=True)
            if isinstance(res, tuple):
                df_errors, col_map = res
            else:
                df_errors = res
                col_map = None

            global COLUMN_MAPPING
            COLUMN_MAPPING = col_map

            if df_errors.empty:
                print(f"  WARNING: No data for year {year}. Skipping.")
                continue
            
            rules = mine_association_rules(df_errors, 
                                          min_support=min_support,
                                          min_confidence=min_confidence,
                                          max_len=max_len,
                                          min_lift=min_lift)
            
            if rules.empty:
                print(f"  WARNING: No rules found for year {year}. Skipping.")
                continue
            
            save_rules(rules, year, top_n=top_n)
            analyze_rules_statistics(rules, year)
            
            print_rules_summary(rules, top_n=10)
            
        except Exception as e:
            print(f"ERROR processing year {year}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"Results saved to: output/error_cooccurrence/")


if __name__ == "__main__":
    main()
