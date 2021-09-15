import read_wos_database
#%%
# Define path to datanase files
path_to_file = 'C:\\Temp\\'
#%%
# Create 'read_wos_database' instance
test=read_wos_database.read_wos_database()
# Set path to file(s)
test.set_path_to_file(path_to_file)
# Load files
test.read_file(['uav_guidance_01.txt','uav_guidance_02.txt','uav_guidance_03.txt'])
    
#%% Parse database file
test.parse_file()
#%% Extract publication year statistics
test.extract_pub_year_stats()
#%% Extract list of countries statistics
test.extract_countries_list_stats()
#%% Compute country publications per year
test.compute_country_pub_per_year()
#%% Extract list of Web of Science's research categories statistics
test.extract_wos_categories_list_stats()
#%% Extract list of Web of Science's research areas statistics
test.extract_wos_research_areas_list_stats()

#%% Plot publications per year distribution
test.plot_pub_per_year()
#test.plot_pub_per_year(norm=True)
#%% Plot publications per country distribution
test.plot_pub_per_country()
#test.plot_pub_per_country(norm=True)
#%% Plot publications per country per year distribution
test.plot_country_pub_per_year()
#test.plot_country_pub_per_year(norm=True)
#%% Plot Treemap of total (i.e., for all years) Web of Science's research categories
test.plot_treemap_wos_categories_total(show_labels=False)
#%% Plot Treemap of total (i.e., for all years) Web of Science's research areas
test.plot_treemap_wos_research_areas_total()