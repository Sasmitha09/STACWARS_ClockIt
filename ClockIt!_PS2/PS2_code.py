from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

sns.set_theme(style="whitegrid")


BASE = Path(__file__).resolve().parent
CSV = BASE / "solar_data.csv"
if not CSV.exists():
    CSV = BASE / "Solar project" / "solar_data.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(r"C:\Users\IITIAN HARSHITA\.vscode-shared\Solar project\solar_data.csv")
df.columns = df.columns.str.strip()
df = df.rename(columns={"WindDirection(Degrees)": "WindDirection", "Speed": "WindSpeed"})
print("Rows:", len(df), "| Missing values:", int(df.isna().sum().sum()))


date_part = pd.to_datetime(df["Data"]).dt.normalize()
df["Date"] = date_part
df["datetime"] = date_part + pd.to_timedelta(df["Time"].astype(str).str.strip())
df["Sunrise"] = date_part + pd.to_timedelta(df["TimeSunRise"].astype(str).str.strip())
df["Sunset"] = date_part + pd.to_timedelta(df["TimeSunSet"].astype(str).str.strip())
df = df.sort_values("datetime").reset_index(drop=True)
df["Hour"] = df["datetime"].dt.hour
df["HourFrac"] = df["datetime"].dt.hour + df["datetime"].dt.minute / 60


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=150)
    plt.close()


fig, ax = plt.subplots(2, 1, figsize=(13, 8))
ax[0].plot(df["datetime"], df["Radiation"], lw=0.5, color="orange")
ax[0].set(title="Solar radiation over the whole observation period",
          ylabel="Radiation (W/m²)")
daily = df.groupby("Date")["Radiation"].agg(["max", "mean"])
ax[1].plot(daily.index, daily["max"], label="Daily max", color="red")
ax[1].plot(daily.index, daily["mean"], label="Daily mean", color="blue")
ax[1].set(title="Daily maximum and mean radiation", ylabel="Radiation (W/m²)")
ax[1].legend()
save("A1_radiation_vs_time.png")


plt.figure(figsize=(9, 5))
sns.lineplot(data=df, x="HourFrac", y="Radiation", errorbar="sd", color="darkorange")
plt.title("Radiation through the day (mean ± 1 SD)")
plt.xlabel("Hour of day")
plt.ylabel("Radiation (W/m²)")
save("A2_radiation_by_hour.png")

params = ["Temperature", "Humidity", "Pressure", "WindSpeed"]
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
for a, p in zip(axes.ravel(), params):
    a.scatter(df[p], df["Radiation"], s=3, alpha=0.3)
    a.set(xlabel=p, ylabel="Radiation (W/m²)", title=f"Radiation vs {p}")
save("A3_radiation_vs_parameters.png")


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.boxplot(data=df, x="Hour", y="Radiation", ax=axes[0], fliersize=2)
axes[0].set_title("Radiation by hour (outliers shown)")
sns.boxplot(y=df["WindSpeed"], ax=axes[1])
axes[1].set_title("Wind speed")
sns.boxplot(y=df["Humidity"], ax=axes[2])
axes[2].set_title("Humidity")
save("A4_boxplots_outliers.png")


num = df[["Radiation", "Temperature", "Pressure", "Humidity",
          "WindDirection", "WindSpeed", "HourFrac"]]
plt.figure(figsize=(8, 6))
sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation matrix")
save("A5_correlation_heatmap.png")


plt.figure(figsize=(9, 6))
sc = plt.scatter(df["Temperature"], df["Humidity"], c=df["Radiation"],
                 cmap="inferno", s=4)
plt.colorbar(sc, label="Radiation (W/m²)")
plt.xlabel("Temperature")
plt.ylabel("Humidity")
plt.title("Radiation, temperature and humidity together")
save("A6_temp_humidity_radiation.png")

pivot = df.pivot_table(index="Date", columns="Hour", values="Radiation", aggfunc="mean")
plt.figure(figsize=(12, 8))
sns.heatmap(pivot, cmap="YlOrRd", cbar_kws={"label": "Mean radiation (W/m²)"})
plt.title("Bonus: radiation by date and hour (shows seasonal shrinking of the day)")
save("A_bonus_date_hour_heatmap.png")

print("\n================ B. INFERENCES (numbers for your report) ================")
hourly = df.groupby("Hour")["Radiation"].mean()
print(f"Hour with highest mean radiation: {hourly.idxmax()}:00 "
      f"({hourly.max():.1f} W/m²)")

corr = num.corr()["Radiation"].drop("Radiation").sort_values(key=abs, ascending=False)
print("\nCorrelation of each parameter with radiation (strongest first):")
print(corr.round(3))

print("\nTemperature vs Humidity correlation:",
      round(df["Temperature"].corr(df["Humidity"]), 3))
day = df[(df["datetime"] >= df["Sunrise"]) & (df["datetime"] <= df["Sunset"])]
print("Daytime Radiation vs Humidity correlation:",
      round(day["Radiation"].corr(day["Humidity"]), 3))

q1, q3 = day["Radiation"].quantile([0.25, 0.75])
iqr = q3 - q1
high = day[day["Radiation"] > q3 + 1.5 * iqr]
night = df[(df["datetime"] < df["Sunrise"]) | (df["datetime"] > df["Sunset"])]
night_hi = night[night["Radiation"] > 5]
print(f"\nDaytime IQR outliers (very high radiation): {len(high)}")
print(f"Night-time readings with radiation > 5 W/m² (likely sensor noise): {len(night_hi)}")
print("Wind speed > 20:", int((df["WindSpeed"] > 20).sum()), "readings (storms/gusts)")
print("Hint: a sudden low-radiation reading at midday with high humidity = clouds/fog.")


print("\n================ C. SOLAR DAY ANALYSIS ================")
report = df.groupby("Date").agg(
    Max_Radiation=("Radiation", "max"),
    Avg_Radiation=("Radiation", "mean"),
).round(2)
print(report.head(10))

best_date = report["Max_Radiation"].idxmax()
print("\nDate with highest recorded radiation:", best_date.date(),
      "->", report.loc[best_date, "Max_Radiation"], "W/m²")

peak = df.loc[df[df["Date"] == best_date]["Radiation"].idxmax()]
print("Peak time:", peak["datetime"].time())
print("Temperature:", peak["Temperature"], "| Humidity:", peak["Humidity"],
      "| Wind speed:", peak["WindSpeed"])
print("Sunrise:", peak["Sunrise"].time(), "| Sunset:", peak["Sunset"].time())
delta = peak["datetime"] - peak["Sunrise"]
print(f"Peak occurred {delta} after sunrise ({delta.total_seconds() / 3600:.2f} hours)")
print("Day length:", peak["Sunset"] - peak["Sunrise"])

print("\nTop 5 days by average radiation:")
print(report.sort_values("Avg_Radiation", ascending=False).head(5))
report.to_csv(OUT / "daily_solar_report.csv")


print("\n================ BONUS: PREDICTION ================")
df["MinsSinceSunrise"] = (df["datetime"] - df["Sunrise"]).dt.total_seconds() / 60
df["DayLengthHrs"] = (df["Sunset"] - df["Sunrise"]).dt.total_seconds() / 3600
df["DayOfYear"] = df["datetime"].dt.dayofyear

features = ["Temperature", "Pressure", "Humidity", "WindDirection", "WindSpeed",
            "HourFrac", "MinsSinceSunrise", "DayLengthHrs", "DayOfYear"]
X, y = df[features], df["Radiation"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def scores(name, model):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(f"{name:20s} RMSE = {rmse:8.2f}   R2 = {r2_score(y_test, pred):.4f}")
    return model


scores("Linear Regression", LinearRegression())
rf = scores("Random Forest", RandomForestRegressor(n_estimators=200, n_jobs=-1,
                                                    random_state=42))

imp = pd.Series(rf.feature_importances_, index=features).sort_values()
print("\nFeature importances (Random Forest):")
print(imp.sort_values(ascending=False).round(4))
plt.figure(figsize=(8, 5))
imp.plot(kind="barh", color="teal")
plt.title("Feature importance for predicting radiation")
save("ML_feature_importance.png")

print("\nDone. Plots and daily_solar_report.csv are in:", OUT)


