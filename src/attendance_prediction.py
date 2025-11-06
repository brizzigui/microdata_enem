import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.dummy import DummyClassifier
from utils.read import read_attendance_data


def preprocess_data(df: pd.DataFrame):

    df_copy = df.copy()
    
    X = df_copy.drop('attended', axis=1)
    y = df_copy['attended']
    
    for col in X.columns:
        median_val = X[col].median()
        X[col] = X[col].fillna(median_val)
    
    return X, y


def train_random_forest(X_train, y_train):

    print("\nTraining Random Forest...")
    
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced',  
        verbose=1
    )
    
    rf.fit(X_train, y_train)
    
    print("Training complete!")
    return rf


def evaluate_model(model, X_test, y_test, year: int, save_plots=True):

    print(f"Random Forest evaluation on year {year}")
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    if len(np.unique(y_test)) > 1:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"ROC-AUC: {roc_auc:.4f}")
    else:
        roc_auc = None
        print("ROC-AUC: N/A (only one class in test set)")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Absent', 'Attended']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    if save_plots:
        save_confusion_matrix(cm, year)
        
    return {
        'year': year,
        'accuracy': accuracy,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm
    }


def save_confusion_matrix(cm, year: int):
    
    output_dir = Path("output/attendance_prediction")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Absent', 'Attended'],
                yticklabels=['Absent', 'Attended'])
    plt.title(f'Confusion Matrix (Random Forest) - Year {year}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    output_path = output_dir / f"confusion_matrix_{year}.png"
    plt.savefig(output_path, dpi=300, format="png")
    plt.close()
    
    print(f"Confusion matrix saved to {output_path}")


def plot_feature_importance(model, feature_names):

    output_dir = Path("output/attendance_prediction")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    top_n = 15
    top_indices = indices[:top_n]
    
    plt.figure(figsize=(10, 8))
    plt.title('Top 15 Feature Importances - Random Forest')
    plt.barh(range(top_n), importances[top_indices], align='center')
    plt.yticks(range(top_n), [feature_names[i] for i in top_indices])
    plt.xlabel('Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    output_path = output_dir / "feature_importance.png"
    plt.savefig(output_path, dpi=300, format="png")
    plt.close()
    
    print(f"\nFeature importance plot saved to {output_path}")
    
    print("\nTop 15 Most Important Features:")
    for i, idx in enumerate(top_indices, 1):
        print(f"{i:2d}. {feature_names[idx]:6s}: {importances[idx]:.4f}")


def save_results_summary(results_list):

    output_dir = Path("output/attendance_prediction")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "results_summary.txt"
    
    with open(output_path, 'w') as f:
        f.write("ATTENDANCE PREDICTION - RESULTS SUMMARY\n\n")
        f.write("Model: Random Forest Classifier\n")
        f.write("Training Year: 2020\n")
        f.write("Validation Years: 2021, 2022, 2023\n\n")
        
        for result in results_list:
            f.write(f"\nYear {result['year']}:\n")
            f.write(f"  Accuracy:  {result['accuracy']:.4f}\n")
            f.write(f"  F1-Score:  {result['f1_score']:.4f}\n")
            if result['roc_auc'] is not None:
                f.write(f"  ROC-AUC:   {result['roc_auc']:.4f}\n")
            else:
                f.write(f"  ROC-AUC:   N/A\n")
            f.write(f"  Confusion Matrix:\n")
            cm = result['confusion_matrix']
            f.write(f"    [[{cm[0,0]:6d}, {cm[0,1]:6d}],\n")
            f.write(f"     [{cm[1,0]:6d}, {cm[1,1]:6d}]]\n")
    
    print(f"\nResults summary saved to {output_path}")


def train_baseline_random(X_train, y_train):

    print("\nTraining Baseline (Random Uniform)...")
    
    baseline = DummyClassifier(strategy='uniform', random_state=42)
    baseline.fit(X_train, y_train)
    
    print("Baseline training complete!")
    return baseline


def evaluate_baseline(model, X_test, y_test, year: int):

    print(f"Baseline Evaluation on year {year}")
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Absent', 'Attended'], zero_division=0))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    return {
        'year': year,
        'accuracy': accuracy,
        'f1_score': f1,
        'confusion_matrix': cm
    }


def compare_models(rf_results, baseline_results):

    output_dir = Path("output/attendance_prediction")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "baseline_comparison.txt"
    
    with open(output_path, 'w') as f:
        f.write("RANDOM FOREST vs BASELINE RANDOM - COMPARISON\n\n")
        
        f.write("Baseline Strategy: Random Uniform (chute aleatório)\n")
        f.write("Random Forest: 100 estimators, max_depth=20\n\n")
        
        f.write(f"{'Year':<6} | {'Model':<12} | {'Accuracy':>10} | {'F1-Score':>10} | {'Improvement':>12}\n")
        f.write("-" * 75 + "\n")
        
        for rf_result, bl_result in zip(rf_results, baseline_results):
            year = rf_result['year']
            
            f.write(f"{year:<6} | {'Baseline':<12} | {bl_result['accuracy']:>10.4f} | {bl_result['f1_score']:>10.4f} | {'-':>12}\n")
            
            improvement_acc = ((rf_result['accuracy'] - bl_result['accuracy']) / bl_result['accuracy'] * 100) if bl_result['accuracy'] > 0 else 0
            improvement_f1 = ((rf_result['f1_score'] - bl_result['f1_score']) / bl_result['f1_score'] * 100) if bl_result['f1_score'] > 0 else 0
            
            f.write(f"{year:<6} | {'RandomForest':<12} | {rf_result['accuracy']:>10.4f} | {rf_result['f1_score']:>10.4f} | {improvement_acc:>11.2f}%\n")
            f.write("-" * 75 + "\n")
    
    print(f"\nBaseline comparison saved to {output_path}")
    
    print("MODEL COMPARISON SUMMARY")
    print(f"\n{'Year':<6} | {'Model':<12} | {'Accuracy':>10} | {'F1-Score':>10}")
    print("-" * 60)
    
    for rf_result, bl_result in zip(rf_results, baseline_results):
        year = rf_result['year']
        print(f"{year:<6} | {'Baseline':<12} | {bl_result['accuracy']:>10.4f} | {bl_result['f1_score']:>10.4f}")
        print(f"{year:<6} | {'RandomForest':<12} | {rf_result['accuracy']:>10.4f} | {rf_result['f1_score']:>10.4f}")
        print("-" * 60)


def main():

    print("STEP 1: Loading training data (2020)")
    df_train = read_attendance_data(2020)
    X_train, y_train = preprocess_data(df_train)
    
    print("STEP 2: Training Random Forest")
    model = train_random_forest(X_train, y_train)
    
    print("STEP 3: Analyzing Feature Importance")
    plot_feature_importance(model, X_train.columns.tolist())

    print("STEP 4: Training and Evaluating Baseline (Random)")
    
    baseline_model = train_baseline_random(X_train, y_train)
    baseline_results = []
    
    print("STEP 5: Validation on other years")
    
    results_list = []
    validation_years = [2021, 2022, 2023]
    
    for year in validation_years:
        try:
            df_test = read_attendance_data(year)
            X_test, y_test = preprocess_data(df_test)
            
            result = evaluate_model(model, X_test, y_test, year, save_plots=True)
            results_list.append(result)

            bl_result = evaluate_baseline(baseline_model, X_test, y_test, year)
            baseline_results.append(bl_result)
        except Exception as e:
            print(f"Error processing year {year}: {e}")
            continue
    
    print("STEP 6: Comparing Random Forest vs Baseline")
    compare_models(results_list, baseline_results)
    
    print("STEP 7: Saving results summary")
    save_results_summary(results_list)
    
    print("COMPLETED!")
    print("All results saved to: output/attendance_prediction/")


if __name__ == "__main__":
    main()
