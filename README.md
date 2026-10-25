# STAC WARS: Team Clock It

Submission repository for the STAC WARS hackathon, IIT Mandi.

**Team:** Clock It (Clock_it!)

| Member | Roll no. |
|---|---|
| Sai Sasmitha (team leader) | B26470 |
| Khwaish Gupta | B26423 |
| Manya Gupta | B26139 |
| Harshita Mishra | B26036 |
| Tisna Singla | B26026 |

This README explains the three problem statements we attempted, what we attempted, what we found, how to run or open our files, and how the repository is organised.

---

## Tasks at a glance

| Task | Problem | What we submitted | Status |
|---|---|---|---|
| 1. OpenRocket | PS 1: Operation Ember Ascent, a two-stage rocket for the fictional planet Mustafar | `.ork` file, flight data CSV, PDF report | Attempted. Apogee, length, impulse and recovery met; ground hit velocity missed (see below) |
| 2. Data Visualization | PS 2: Solar Radiation Analysis and Prediction (Voyage-123 data) | `.py` script, PDF report | Parts A, B, C and the bonus model all done |
| 3. Astronomy | PS 3: Exoplanet Hunters (three stars, transit data) | PDF report in IEEE format | Parts A to D done |

We chose three of the problem statements. We also made one combined presentation covering all three, for the Sunday round if we are shortlisted.

---

---

## Task 1: OpenRocket (PS 1, Operation Ember Ascent)

### The challenge

Design a two-stage rocket in OpenRocket for the fictional planet Mustafar and fly it under Mustafar's conditions. The brief asks for:

- Apogee between 3900 and 4100 m

- Payload mass between 0.95 and 1.05 kg

- Length at most 220 cm

- Total impulse at most 2800 N·s

- A parachute deployed at apogee

- Descent (ground hit) velocity between 4 and 8 m/s

- The body material stated (aluminium, cardboard or PVC), with no manual mass overrides

- A report comparing Mustafar with Earth for gravity, pressure, temperature, density and wind

### Mustafar vs Earth conditions

| Setting | Earth (comparison) | Mustafar (mission) |
|---|---|---|
| Gravity | 9.81 m/s² | 6.5 m/s² |
| Pressure | 101.3 kPa | 75 kPa (750 mbar) |
| Temperature | 15 °C (288 K) | 700 K (426.85 °C) |
| Air density | 1.225 kg/m³ | 0.374 kg/m³ |
| Wind | Earth setting | 10 m/s average at 270° (1 m/s std dev, 10% turbulence) |
| Launch | 0 m altitude | 0 m altitude, 200 cm rod, 0° angle |

OpenRocket's launch conditions have no gravity box, so gravity is set with the **Planetary Environment (Mustafar)** simulation extension, which fixes it at 6.5 m/s². That extension does not change the atmosphere, so pressure and temperature were typed in by hand, with "Use International Standard Atmosphere" unticked. OpenRocket then works out a density of about 0.373 kg/m³, which matches the 0.374 in the brief.

### Our rocket

- Two stages, 60.5 cm long, 7 cm maximum diameter

- Mass: 2329 g without motors, 3528 g with motors

- Motors: I120-15 and I445-6 (combined impulse at most 1280 N·s)

- Stability: 1.2 calibres (13.9% of length) at launch. CG 28.9 cm, CP 37.4 cm at Mach 0.3

- Recovery: one parachute per stage, both deployed at apogee with a 0 s delay

- Appearance: custom space-themed textures for the nose cone and both body tubes

### Results (Mustafar run)

| Requirement | Our result | Met? |
|---|---|---|
| Apogee 3900 to 4100 m | 3913 m | Yes (13 m above the lower limit) |
| Length at most 220 cm | 60.5 cm | Yes |
| Total impulse at most 2800 N·s | at most 1280 N·s | Yes |
| Deploy at apogee, parachute recovery | Both chutes at apogee, both stages recovered | Yes |
| Payload 0.95 to 1.05 kg | See the checklist at the bottom | To confirm |
| Ground hit velocity 4 to 8 m/s | **9.16 m/s** | **No** |

Other results: max velocity 246 m/s (Mach 0.439), max acceleration 149 m/s², time to apogee 33.9 s, velocity at deployment 32.9 m/s, flight time 1317 s, downrange drift 11,550 m.

### What we attempted on the ground hit velocity

We did not get the ground hit velocity into 4 to 8 m/s. Across many attempts it sat between about 9 and 12 m/s. We resized both parachutes repeatedly and changed the motors to pull the apogee back into range when the lower gravity pushed it too high. Nothing brought it under 8 m/s.

The one-at-a-time runs below point at the **10 m/s side wind**. OpenRocket's ground hit velocity is the total speed, so it includes sideways drift under the chutes. A rough check on our data agrees: the rocket sinks only about 3 m/s on average (3913 m in about 1283 s) but drifts about 9 m/s sideways (11,550 m in the same time), giving about 9.5 m/s combined against the 9.16 m/s reported. These are averages, not measured landing values, so this is a well-supported explanation, not a proof. A confirming run would be the same Mustafar rocket with wind set to 0.

### Mustafar vs Earth, one change at a time

Each run uses Mustafar conditions for everything except the one setting switched to its Earth value. The same rocket and chutes were used throughout. Drift is the final lateral distance exported from OpenRocket.

| Run | Apogee | Max velocity | Velocity at deployment | Ground hit | Flight time | Drift |
|---|---|---|---|---|---|---|
| Mustafar (all Mustafar) | 3913 m | 246 m/s | 32.9 m/s | 9.16 m/s | 1317 s | 11,550 m |
| Earth gravity only | 2885 m | 231 m/s | 33.9 m/s | 9.09 m/s | 788 s | 6749 m |
| Earth temperature only | 2855 m | 223 m/s | 30.4 m/s | 10.1 m/s | 1382 s | 12,510 m |
| Earth pressure only | 3548 m | 240 m/s | 30 m/s | 11.2 m/s | 1387 s | 12,440 m |
| Earth wind only | 4107 m | 247 m/s | 6.3 m/s | 3.82 m/s | 1362 s | 2404 m |
| Everything Earth | 2115 m | 202 m/s | 6 m/s | 2.93 m/s | 964 s | 1735 m |

### Did our predictions hold?

- **Gravity (lower on Mustafar): yes.** Earth gravity alone lowers apogee by 1028 m, and max acceleration changes by about 3 m/s², matching the 3.3 m/s² we predicted from the difference in g.

- **Air density (thinner on Mustafar): yes.** Denser air gave a lower apogee in every run, and the temperature run, which changes density the most, lost the most height.

- **Temperature (hotter on Mustafar): yes for Mach number.** Mustafar reached Mach 0.439 at 246 m/s, which implies a sound speed of roughly 560 m/s. Earth's 202 m/s is about Mach 0.59. In our rocket, temperature mattered more through air density than through the speed of sound, because we never went near Mach 1.

- **Wind: yes, strongly.** Changing only the wind drops ground hit velocity from 9.16 to 3.82 m/s, velocity at deployment from 32.9 to 6.3 m/s, and drift from 11,550 m to 2404 m.

- **Parachute descent formula: no.** The terminal-speed formula (proportional to the square root of g divided by density) did not predict the ground hit velocity once sideways wind was involved.

---

## Task 2: Data Visualization (PS 2, Solar Radiation Analysis and Prediction)

### The challenge

The Voyage-123 probe logged solar radiation, temperature, humidity, pressure, wind and sunrise/sunset times. The brief has four parts:

- **A (4 marks):** visualise radiation against time and against at least two other parameters, and look for trends and outliers.

- **B (5 marks):** draw inferences supported by the data.

- **C (5 marks):** build a day-wise solar report with Pandas and NumPy.

- **Bonus (6 marks):** predict radiation with a regression model scored by RMSE and R².

### The dataset

32,686 readings from 1 Sep 2016 to 31 Dec 2016 (118 days), one every 5 minutes, with no missing values. Columns: UNIX time, date, time, radiation, temperature, pressure, humidity, wind direction, wind speed, sunrise and sunset.

### What we did

**Part A: plots.** The script saves these to `outputs/`:

- Radiation over the whole period, plus daily maximum and mean (`A1_radiation_vs_time.png`)

- Radiation through the day, mean ± 1 SD (`A2_radiation_by_hour.png`)

- Radiation against temperature, humidity, pressure and wind speed (`A3_radiation_vs_parameters.png`)

- Boxplots for outliers (`A4_boxplots_outliers.png`)

- A correlation heatmap (`A5_correlation_heatmap.png`)

- Radiation, temperature and humidity together (`A6_temp_humidity_radiation.png`)

- Bonus: a date-by-hour heatmap (`A_bonus_date_hour_heatmap.png`)

**Part B: inferences.**

- Radiation is highest at **12:00**, with a mean of 727.5 W/m².

- The strongest relationship is with **temperature**, r = 0.74. Humidity is negatively related (r = −0.23 overall, −0.39 in daytime only), and temperature and humidity move in opposite directions (r = −0.29).

- There are no daytime outliers by the IQR rule. There are **102 night-time readings above 5 W/m²**, most likely sensor noise, and 149 readings with wind speed above 20.

- Bonus insight: the sunlit window shrinks from about 12.5 hours in September to about 11 hours in December, and the date-by-hour heatmap shows the bright band narrowing with it.

**Part C: solar-day report.** Built with a proper datetime column, a groupby on date, and the sunrise and sunset times. It is saved as `outputs/daily_solar_report.csv`.

| Fact | Value |
|---|---|
| Highest-radiation date | 2016-09-04 |
| Maximum radiation | 1601.26 W/m² at 12:15 |
| Temperature, humidity, wind at the peak | 61, 93, 9.0 (temperature in the dataset's own units) |
| Peak after sunrise | 6.12 hours (sunrise 06:08, sunset 18:35) |
| Top 5 days by average radiation | 19 Sep (335.5), 2 Sep (333.5), 22 Sep (325.5), 25 Sep (319.9), 28 Sep (312.4) W/m² |

The 1601 W/m² peak is a single reading with 93% humidity, well above the next highest readings (about 1400 to 1475 W/m²), so it may be a sensor spike.

**Bonus: prediction.** 80/20 train-test split (`random_state=42`). Features: temperature, pressure, humidity, wind direction, wind speed, hour of day, minutes since sunrise, day length and day of year.

| Model | RMSE | R² |
|---|---|---|
| Linear Regression | 191.25 | 0.6238 |
| Random Forest (200 trees) | 75.39 | 0.9415 |

The most useful features for the Random Forest are temperature (0.567), minutes since sunrise (0.170) and hour of day (0.144).

---

## Task 3: Astronomy (PS 3, Exoplanet Hunters)

### The challenge

Given brightness-over-time data for three stars (STAC-1, STAC-2, STAC-3), detect transiting exoplanets, estimate their size and orbits, and pick the most promising world for habitability. All calculations must be shown, in an IEEE-format PDF report.

### Star properties given

| Property | STAC-1 | STAC-2 | STAC-3 |
|---|---|---|---|
| Mass | 1.00 M☉ | 0.80 M☉ | 0.50 M☉ |
| Radius | 1.00 R☉ | 0.80 R☉ | 0.50 R☉ |
| Luminosity | 1.00 L☉ | 0.40 L☉ | 0.08 L☉ |
| Temperature | 5800 K | 5000 K | 3800 K |

### What we did

**A. Detect.** A transit shows up as a repeating dip in relative brightness, because a planet passing in front of its star blocks a little of the light. Transit depth is δ = (F_normal − F_transit) / F_normal.

| Star | Dips at day | Orbital period | Depth δ | Planet detected? |
|---|---|---|---|---|
| STAC-1 | 3, 8, 12, 16, 20 | about 4 days | 0.003 | Yes |
| STAC-2 | 20, 100, 180 | 80 days | 0.001 | Yes |
| STAC-3 | 20, 60, 100, 140, 170 | Not periodic | about 0.00088 (average) | Not sure |

For STAC-1 the gaps are 5, 4, 4 and 4 days, so we took 4 days. For STAC-2 the samples are 20 days apart, so we tested periods of 10, 20, 40 and 80 days. Only 80 days gives no dip where the data show none. For STAC-3 the gaps are 40, 40, 40 and 30 days, which is not consistent enough to confirm a period. That does not prove there is no planet, only that the data are insufficient.

**B. Planet size.** Using R_p = R_s × √δ:

| Star | Radius | In Earth radii | Class |
|---|---|---|---|
| STAC-1 | about 38,121 km | 5.98 R⊕ | Neptune-sized |
| STAC-2 | about 17,605 km | 2.76 R⊕ | Super-Earth |
| STAC-3 | about 10,322 km | 1.62 R⊕ | Super-Earth (tentative) |

**C. Orbits.** Using Kepler's third law, a = (P² × M)^(1/3), with P in years and M in solar masses:

| Star | Period | Orbital distance | Compared with Earth (1 AU) |
|---|---|---|---|
| STAC-1 | 4 days | 0.049 AU (about 7.4 million km) | about 5% of Earth's distance |
| STAC-2 | 80 days | 0.337 AU (about 50.3 million km) | about 34% of Earth's distance |
| STAC-3 | 40 days (assumed) | about 0.182 AU (about 27.2 million km) | about 18% of Earth's distance |

STAC-3's distance only holds if its dips repeat every 40 days, which the data do not confirm.

**D. Most promising world.** The simplified habitable-zone distance is d_HZ ≈ √(L / L☉):

| Star | Planet's orbit | Habitable-zone distance |
|---|---|---|
| STAC-1 | 0.049 AU | 1.0 AU |
| STAC-2 | 0.337 AU | 0.632 AU |
| STAC-3 | about 0.182 AU (unconfirmed) | 0.283 AU |

**Conclusion: STAC-2's planet** is the most promising among the detected planets. The evidence:

1\. Its orbit (0.337 AU) is far closer to its habitable zone than STAC-1's (0.049 AU against 1.0 AU).

2\. It has a longer period (80 days against 4 days), so it is farther from its star.

3\. Its star is cooler (5000 K) and dimmer, so the habitable zone sits closer in (0.632 AU).

4\. It is a confirmed detection, unlike STAC-3.

**Limitation:** STAC-2's planet is still inside the inner edge of the simplified habitable zone, so it is a candidate for further study, not a proven habitable world.

**Additional observation:** study the starlight passing through the planet's atmosphere during a transit. Different gases absorb different wavelengths, which would show whether it has an atmosphere and what gases are in it.

---
