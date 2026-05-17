#import colours
import matplotlib.colors as colors

# Plotting theoretical isochrones over our stars as a reference to what a HR diagram usually looks like

#remake HR diagram but log scaled to clearly see the locations of the stars on the bigger picture
plt.figure(figsize = (14, 8))

query = """
SELECT TOP 20000
    parallax,
    phot_g_mean_mag,
    teff_gspphot

FROM gaiadr3.gaia_source

WHERE parallax_over_error > 5
AND phot_g_mean_mag IS NOT NULL
AND teff_gspphot IS NOT NULL

ORDER BY random_index
"""

job = Gaia.launch_job(query)
gaia_random = job.get_results().to_pandas()

# Distance in parsec
gaia_random["distance_pc"] = 1000 / gaia_random["parallax"]

# Absolute magnitude
gaia_random["abs_mag"] = (
    gaia_random["phot_g_mean_mag"]
    + 5
    - 5 * np.log10(gaia_random["distance_pc"])
)

# Clean invalid values
gaia_random = gaia_random.replace([np.inf, -np.inf], np.nan)
gaia_random = gaia_random.dropna(subset=["teff_gspphot", "abs_mag"])

# Plot Gaia background stars
plt.scatter(
    gaia_random["teff_gspphot"],
    gaia_random["abs_mag"],
    s=2,
    color="gray",
    alpha=0.12,
    label="Random Gaia stars"
)
t_range = np.linspace(3000, 30000, len(gaia_df))

# mask = np.where((all_char["teff"] >= 0) & (all_char["teff"] <= 30000)) 
# intermiadate_step = all_char["teff"]
vmin = min(full_char["teff"].min(), quasi_char["teff"].min(), semi_char["teff"].min())
vmax = max(full_char["teff"].max(), quasi_char["teff"].max(), semi_char["teff"].max())

# print(vmin, vmax)


sc = plt.scatter(full_char["teff"], full_char["abs_mag"], c = full_char["teff"], cmap = "coolwarm_r", s = 60, 
                 label = "Full solar-like stars", marker="o", vmin=vmin, vmax=vmax, edgecolors = "black", alpha = 0.7) 
sc1 = plt.scatter(quasi_char["teff"], quasi_char["abs_mag"], c = quasi_char["teff"], cmap = "coolwarm_r", s = 60, 
                  label = "Quasi solar-like stars", marker="^", vmin=vmin, vmax=vmax, edgecolors = "black", alpha = 0.7) 
sc2 = plt.scatter(semi_char["teff"], semi_char["abs_mag"], c = semi_char["teff"], cmap = "coolwarm_r", s = 60, 
                  label = "Semi solar-like stars", marker="s", vmin=vmin, vmax=vmax, edgecolors = "black", alpha = 0.7) 

plt.colorbar(sc, label="Temperature (K)") 

# Plotting the sun for reference
plt.scatter(5772, 4.83, marker = "*", s = 200, label = "Sun", color = "yellow", edgecolors = "black") # plotting the sun for reference

plt.xlim(2500, 30000)
plt.ylim(15, -5)


plt.gca().invert_xaxis()
#plt.gca().invert_yaxis()


plt.xscale('log')
plt.xlabel("Temperature (K)", fontsize = 15)
plt.ylabel("Absolute magnitude", fontsize = 15)
plt.title("HR diagram - Absolute magnitude against Temperature", fontsize = 15)
plt.gca().tick_params(axis = 'both', which = 'both', labelsize=15)
plt.yticks(size = 15)
plt.tight_layout()
plt.legend()
plt.show()