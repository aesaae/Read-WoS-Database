import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import squarify

#%%
class read_wos_database():
    def __init__(self):
        
        # Entry dictionary
        self.entry = {}
        # Database number of entries counter
        self.n_entries = 0
        # New entry flag
        self.new_entry = False
        # Entries database (list)
        self.entry_database = []
        
    def set_path_to_file(self, path_to_file):
        
        #
        self.path_to_file = path_to_file

    def read_file(self, filename, file_encoding='utf8'):
        
        #
        file_content = []
        if type(filename) == str:
            no_files = 1
        elif type(filename) == list:
            no_files = len(filename)
        #
        for files in range(0, no_files):
            with open(self.path_to_file+filename[files], 'r', encoding=file_encoding) as f:
                lines = f.readlines()
            #
            if files < (no_files-1):
                lines.pop()
            #
            file_content.extend(lines)
        #
        self.file_content = file_content
        
    def reset_entry_dict(self):
        '''
        
        The following two-character filed tags have been taken from the Web of Science definitions,
        found at https://images.webofknowledge.com/images/help/WOS/hs_wos_fieldtags.html

        Returns
        -------
        None.

        '''
        
        #
        self.entry['PT'] = None # Publication Type (J=Journal; B=Book; S=Series; P=Patent)
        self.entry['AU'] = None # Authors
        self.entry['AF'] = None # Author Full Name
        self.entry['BE'] = None # Editors
        self.entry['TI'] = None # Document Title
        self.entry['SO'] = None # Publication Name
        self.entry['SE'] = None # Book Series Title
        self.entry['LA'] = None # Language
        self.entry['DT'] = None # Document Type
        self.entry['CT'] = None # Conference Title
        self.entry['CY'] = None # Conference Date
        self.entry['SP'] = None # Conference Sponsors
        self.entry['DE'] = None # Author Keywords
        self.entry['ID'] = None # Keywords Plus
        self.entry['AB'] = None # Abstract
        self.entry['C1'] = None # Author Address
        self.entry['RP'] = None # Reprint Address
        self.entry['EM'] = None # E-mail Address
        self.entry['FU'] = None # Funding Agency and Grant Number
        self.entry['FX'] = None # Funding Text
        self.entry['CR'] = None # Cited References
        self.entry['NR'] = None # Cited Reference Count
        self.entry['TC'] = None # Web of Science Core Collection Times Cited Count
        self.entry['Z9'] = None # Total Times Cited Count (Web of Science Core Collection, Arabic Citation Index, BIOSIS Citation Index, Chinese Science Citation Database, Data Citation Index, Russian Science Citation Index, SciELO Citation Index)
        self.entry['U1'] = None # Usage Count (Last 180 Days)
        self.entry['U2'] = None # Usage Count (Since 2013)
        self.entry['PU'] = None # Publisher
        self.entry['PI'] = None # Publisher City
        self.entry['PA'] = None # Publisher Address
        self.entry['SN'] = None # International Standard Serial Number (ISSN)
        self.entry['BN'] = None # International Standard Book Number (ISBN)
        self.entry['J9'] = None # 29-Character Source Abbreviation
        self.entry['PY'] = None # Year Published
        self.entry['BP'] = None # Beginning Page
        self.entry['EP'] = None # Ending Page
        self.entry['PG'] = None # Page Count
        self.entry['WC'] = None # Web of Science Categories
        self.entry['SC'] = None # Research Areas
        self.entry['GA'] = None # Document Delivery Number
        self.entry['UT'] = None # Accession Number
        self.entry['DA'] = None # Date this report was generated.
        self.entry['ER'] = None # End of Record
        #
        self.entry['BA'] = None # Book Authors
        self.entry['BF'] = None # Book Authors Full Name
        self.entry['CA'] = None # Group Authors
        self.entry['GP'] = None # Book Group Authors
        self.entry['BS'] = None # Book Series Subtitle
        self.entry['CL'] = None # Conference Location
        self.entry['HO'] = None # Conference Host
        self.entry['RI'] = None # ResearcherID Number
        self.entry['OI'] = None # ORCID Identifier (Open Researcher and Contributor ID)
        self.entry['EI'] = None # Electronic International Standard Serial Number (eISSN)
        self.entry['JI'] = None # ISO Source Abbreviation
        self.entry['PD'] = None # Publication Date
        self.entry['VL'] = None # Volume
        self.entry['IS'] = None # Issue
        self.entry['SI'] = None # Special Issue
        self.entry['PN'] = None # Part Number
        self.entry['SU'] = None # Supplement
        self.entry['MA'] = None # Meeting Abstract
        self.entry['AR'] = None # Article Number
        self.entry['DI'] = None # Digital Object Identifier (DOI)
        self.entry['D2'] = None # Book Digital Object Identifier (DOI)
        self.entry['EA'] = None # Early access date
        self.entry['EY'] = None # Early access year
        self.entry['P2'] = None # Chapter Count (Book Citation Index)
        self.entry['PM'] = None # PubMed ID
        self.entry['OA'] = None # Open Access Indicator
        self.entry['HP'] = None # ESI Hot Paper. Note that this field is valued only for ESI subscribers.
        self.entry['HC'] = None # ESI Highly Cited Paper. Note that this field is valued only for ESI subscribers.
        #
        self.entry['CNTY'] = None # Aythor's Country
    
    def extract_authors_list(self, line):
        
        # Initialise 'authors_list'
        authors_list = []
        # Add first author
        author = self.file_content[line][3:-1]
        authors_list.append(author)
        # Increase 'line'
        line += 1
        # Look for additional authors
        while self.file_content[line][0:2] == '  ':
            # Additional author found, add them to list
            author = self.file_content[line][3:-1]
            authors_list.append(author)
            # Increase 'line'
            line += 1
        # Return 'authors_list' and 'line'
        return authors_list, line
    
    def extract_title(self, line):
        
        # Initialise 'title_string'
        title_string = ''
        title_string = self.file_content[line][3:-1]
        # Increase 'line'
        line += 1
        # Look for additional lines of text (i.e., title spans several lines)
        while self.file_content[line][0:2] == '  ':
            # Additional title text lines found, add them to 'title_string'
            title_string = title_string +' '+ self.file_content[line][3:-1]
            # Increase 'line'
            line += 1
        # Return 'title_string' and 'line'
        return title_string, line
    
    def extract_publication_name(self, line):
        
        # Initialise 'pub_name_string'
        pub_name_string = ''
        pub_name_string = self.file_content[line][3:-1]
        # Increase 'line'
        line += 1
        # Look for additional lines of text (i.e., publication name spans several lines)
        while self.file_content[line][0:2] == '  ':
            # Additional publication name text lines found, add them to 'pub_name_string'
            pub_name_string = pub_name_string +' '+ self.file_content[line][3:-1]
            # Increase 'line'
            line += 1
        # Return 'pub_name_string' and 'line'
        return pub_name_string, line
    
    def extract_document_type(self, line):
        
        # Initialise 'doc_type_string'
        doc_type_string = ''
        doc_type_string = self.file_content[line][3:-1]
        # Increase 'line'
        line += 1
        # Look for additional lines of text (i.e., document type name spans several lines)
        while self.file_content[line][0:2] == '  ':
            # Additional document type name text lines found, add them to 'doc_type_string'
            doc_type_string = doc_type_string +' '+ self.file_content[line][3:-1]
            # Increase 'line'
            line += 1
        # Return 'doc_type_string' and 'line'
        return doc_type_string, line
    
    def extract_pub_year(self, line):
        
        # Initialise 'pub_year'
        pub_year = self.file_content[line][3:-1]
        if pub_year.isnumeric():
            pub_year = pub_year#int(pub_year)
            # Increase 'line'
            line += 1
        else:
            print("Warning 'pub_year' string in line {0}, is not a number!".format(line))
        # Return 'pub_year' and 'line'
        return pub_year, line
    
    def extract_author_address(self, line):
        
        # Initialise 'author_address_list'
        author_address_list = []
        # Add first address
        this_address = self.file_content[line][3:-1]
        author_address_list.append(this_address)
        # Increase 'line'
        line += 1
        # Look for additional address
        while self.file_content[line][0:2] == '  ':
            # Additional address found, add them to list
            this_address = self.file_content[line][3:-1]
            author_address_list.append(this_address)
            # Increase 'line'
            line += 1
        # Return 'author_address_list' and 'line'
        return author_address_list, line
    
    def extract_author_keywords(self, line):
        
        # Initialise 'author_keywords_list'
        author_keywords_list = []
        # Add first country
        this_keyword = self.file_content[line][3:-1]
        author_keywords_list.append(this_keyword)
        # Increase 'line'
        line += 1
        # Look for additional countries
        while self.file_content[line][0:2] == '  ':
            # Additional country found, add them to list
            this_keyword = self.file_content[line][3:-1]
            author_keywords_list.append(this_keyword)
            # Increase 'line'
            line += 1
        #
        author_keywords_string = author_keywords_list[0]
        for elem in range(1,len(author_keywords_list)):
            #
            author_keywords_string = author_keywords_string +' ' +author_keywords_list[elem]
        # Return 'author_keywords_string' and 'line'
        return author_keywords_string, line
    
    def extract_author_country_list(self, author_address):
        
        #
        author_country_list = []
        # Look for author's countries
        for line in range(0,len(author_address)):
            #
            this_country = author_address[line].split(sep=',')[-1][1:-1]
            # Check if country is USA. Some entries include state and post code in same line as country,
            # e.g., 'VA 23529 USA', includes VA for Virginia, the postcode 23529 and USA for the country.
            if 'USA' in this_country:
                this_country = 'USA'
            author_country_list.append(this_country)
        # Return 'author_country_list' and 'line'
        return author_country_list
    
    def extract_wos_categories(self, line):
        
        # Initialise 'wos_categories_list'
        wos_categories_list = []
        # Add first country
        this_category = self.file_content[line][3:-1]
        wos_categories_list.append(this_category)
        # Increase 'line'
        line += 1
        # Look for additional catergories
        while self.file_content[line][0:2] == '  ':
            # Additional category found, add them to list
            this_category = self.file_content[line][3:-1]
            wos_categories_list.append(this_category)
            # Increase 'line'
            line += 1
        #
        wos_categories_string = wos_categories_list[0]
        for elem in range(1,len(wos_categories_list)):
            #
            wos_categories_string = wos_categories_string +' ' +wos_categories_list[elem]
        # Return 'wos_categories_string' and 'line'
        return wos_categories_string, line
    
    def extract_wos_research_areas(self, line):
        
        # Initialise 'wos_research_areas_list'
        wos_research_areas_list = []
        # Add first country
        this_area = self.file_content[line][3:-1]
        wos_research_areas_list.append(this_area)
        # Increase 'line'
        line += 1
        # Look for additional areas
        while self.file_content[line][0:2] == '  ':
            # Additional area found, add them to list
            this_area = self.file_content[line][3:-1]
            wos_research_areas_list.append(this_area)
            # Increase 'line'
            line += 1
        #
        wos_research_areas_string = wos_research_areas_list[0]
        for elem in range(1,len(wos_research_areas_list)):
            #
            wos_research_areas_string = wos_research_areas_string +' ' +wos_research_areas_list[elem]
        # Return 'wos_research_areas_string' and 'line'
        return wos_research_areas_string, line
                
    def parse_record(self, line):
        
        #
        if self.file_content[line][0:2] == 'PT':
            # Clear entry dictionary
            self.reset_entry_dict()
            #
            self.entry['PT'] = self.file_content[line][3:-1]
            # Increase 'line'
            line += 1
        elif self.file_content[line][0:2] == 'AU':
            # 
            authors_list_short, line = self.extract_authors_list(line)
            #print('In line {0}, found {1} authors, namely: {2}'.format(line,len(authors_list_short),authors_list_short))
            #
            self.entry['AU'] = authors_list_short
        elif self.file_content[line][0:2] == 'AF':
            authors_list_full, line = self.extract_authors_list(line)
            #print('In line {0}, found {1} authors, namely: {2}'.format(line,len(authors_list_full),authors_list_full))
            #
            self.entry['AF'] = authors_list_full
        elif self.file_content[line][0:2] == 'TI':
            entry_title, line = self.extract_title(line)
            #
            self.entry['TI'] = entry_title
        elif self.file_content[line][0:2] == 'SO': 
            publication_name, line = self.extract_publication_name(line)
            #
            self.entry['SO'] = publication_name
        elif self.file_content[line][0:2] == 'DT':    
            doc_type, line = self.extract_document_type(line)
            #
            self.entry['DT'] = doc_type
        elif self.file_content[line][0:2] == 'PY':    
            pub_year, line = self.extract_pub_year(line)
            #
            self.entry['PY'] = pub_year
        elif self.file_content[line][0:2] == 'C1':      
            author_address, line = self.extract_author_address(line)
            #
            country_list = self.extract_author_country_list(author_address)
            #
            self.entry['C1'] = author_address
            self.entry['CNTY'] = country_list
        elif self.file_content[line][0:2] == 'DE':      
            author_keywords, line = self.extract_author_keywords(line)
            #
            self.entry['DE'] = author_keywords
        elif self.file_content[line][0:2] == 'ID':      
            keywords_plus, line = self.extract_author_keywords(line)
            #
            self.entry['ID'] = keywords_plus
        elif self.file_content[line][0:2] == 'WC':
            wos_categories, line = self.extract_wos_categories(line)
            #
            self.entry['WC'] = wos_categories
        elif self.file_content[line][0:2] == 'SC':
            wos_research_areas, line = self.extract_wos_research_areas(line)
            #
            self.entry['SC'] = wos_research_areas
        # Leave this space to include additional fields after this
            
        # Don't include additional fields after this
        elif self.file_content[line][0:2] == 'ER':
            # End of record
            self.n_entries += 1
            self.new_entry = True
        elif self.file_content[line][0:2] == '  ':
            pass
        # Return 'line'
        return line
    
    def parse_file(self):
        
        # Initialise line counter to zero
        line = 0
        while self.file_content[line] != 'EF':
            # Read input file looking for entries/records
            self.parse_record(line)
            if self.new_entry == True:
                # New full entry parsed, add entry/record to entries database (list)
                self.entry_database.append(self.entry.copy())
                # Reset 'new_entry' flag to False
                self.new_entry = False
            # Increase 'line'
            #print(line)
            line += 1
        # Create Pandas dataframe to handle database
        self.pd_df=pd.DataFrame(self.entry_database)
        
    def extract_pub_year_stats(self):
        
        # Extract unique years 
        self.unique_years = self.pd_df.PY.sort_values().unique()
        # Initialise publications per year array
        self.pub_per_year = np.zeros(self.unique_years.shape)
        # Extract number of publications per year
        for this_year in range(0, self.unique_years.size):
            self.pub_per_year[this_year] = np.sum(self.pd_df.PY==self.unique_years[this_year])
            
    def extract_countries_list_stats(self):
        
        #
        countries_list = []
        unique_countries_list = []
        #
        n_entries = self.pd_df.shape[0]
        #
        for entry in range(0,n_entries):
            if self.pd_df.CNTY[entry] != None:
                countries_in_entry = len(self.pd_df.CNTY[entry])
                for this_country in range(0,countries_in_entry):
                    countries_list.append(self.pd_df.CNTY[entry][this_country])
        #
        unique_countries_list=list(set(countries_list))
        unique_countries_list.sort()
        #
        self.unique_countries_list = unique_countries_list
        self.unique_countries_total = len(self.unique_countries_list)
        
    def extract_wos_categories_list_stats(self):
        
        #
        wos_categories_list = []
        unique_wos_categories_list = []
        # Extract number of entries in database
        n_entries = self.pd_df.shape[0]
        #
        for entry in range(0,n_entries):
            if self.pd_df.WC[entry] != None:
                categories_in_entry = self.pd_df.WC[entry].split(sep=';')
                for this_category in range(0,len(categories_in_entry)):
                    wos_categories_list.append(categories_in_entry[this_category])
        # Sort resulting list
        unique_wos_categories_list=list(set(wos_categories_list))
        unique_wos_categories_list.sort()
        # Store results
        self.unique_wos_categories_list = unique_wos_categories_list
        self.unique_wos_categories_total = len(self.unique_wos_categories_list)
        #
        self.compute_wos_categories_per_year()
        
    def extract_wos_research_areas_list_stats(self):
        
        #
        wos_research_areas_list = []
        unique_wos_research_areas_list = []
        # Extract number of entries in database
        n_entries = self.pd_df.shape[0]
        #
        for entry in range(0,n_entries):
            if self.pd_df.SC[entry] != None:
                areas_in_entry = self.pd_df.SC[entry].split(sep=';')
                for this_area in range(0,len(areas_in_entry)):
                    wos_research_areas_list.append(areas_in_entry[this_area])
        # Sort resulting list
        unique_wos_research_areas_list=list(set(wos_research_areas_list))
        unique_wos_research_areas_list.sort()
        # Store results
        self.unique_wos_research_areas_list = unique_wos_research_areas_list
        self.unique_wos_research_areas_total = len(self.unique_wos_research_areas_list)
        #
        self.compute_wos_research_areas_per_year()
    
    def compute_country_pub_per_year(self):
        
        #
        columns_dataframe = self.unique_years.tolist()
        columns_dataframe.append('Total')
        #
        country_pub_per_year=pd.DataFrame(np.zeros((len(self.unique_years)+1,len(self.unique_countries_list))),index=columns_dataframe,columns=self.unique_countries_list)
        #
        n_entries = self.pd_df.shape[0]
        # Loop through entries in database
        for entry in range(0,n_entries):
            if self.pd_df.CNTY[entry] != None:
                # Extract author's country of residence
                countries = list(set(self.pd_df.CNTY[entry]))
                # For each country in list 'countries', update (country, year) pair
                for this_country in range(0,len(countries)):
                    # Increase publication count for (country, year) pair
                    country_pub_per_year.loc[self.pd_df.PY[entry],countries[this_country]] += 1
        #
        country_pub_per_year.loc['Total',:] = country_pub_per_year.iloc[:-1,:].sum()
        #
        country_pub_per_year = country_pub_per_year.transpose().sort_values(by=['Total'], ascending=False)
        self.country_pub_per_year = country_pub_per_year.transpose()
        
    def compute_wos_categories_per_year(self):
        
        #
        columns_dataframe = self.unique_years.tolist()
        columns_dataframe.append('Total')
        #
        unique_wos_categories_stats=pd.DataFrame(np.zeros((len(self.unique_years)+1,len(self.unique_wos_categories_list))),index=columns_dataframe,columns=self.unique_wos_categories_list)
        #
        n_entries = self.pd_df.shape[0]
        # Loop through entries in database
        for entry in range(0,n_entries):
            if self.pd_df.WC[entry] != None:
                # Extract entry's categories
                categories_in_entry = self.pd_df.WC[entry].split(sep=';')
                # For each category in list 'categories_in_entry', update (category, year) pair
                for this_category in range(0,len(categories_in_entry)):
                    # Increase publication count for (category, year) pair
                    unique_wos_categories_stats.loc[self.pd_df.PY[entry],categories_in_entry[this_category]] += 1
        #
        unique_wos_categories_stats.loc['Total',:] = unique_wos_categories_stats.iloc[:-1,:].sum()
        #
        unique_wos_categories_stats = unique_wos_categories_stats.transpose().sort_values(by=['Total'], ascending=False)
        self.unique_wos_categories_stats = unique_wos_categories_stats.transpose()
        
    def compute_wos_research_areas_per_year(self):
        
        #
        columns_dataframe = self.unique_years.tolist()
        columns_dataframe.append('Total')
        #
        unique_wos_research_areas_stats=pd.DataFrame(np.zeros((len(self.unique_years)+1,len(self.unique_wos_research_areas_list))),index=columns_dataframe,columns=self.unique_wos_research_areas_list)
        #
        n_entries = self.pd_df.shape[0]
        # Loop through entries in database
        for entry in range(0,n_entries):
            if self.pd_df.WC[entry] != None:
                # Extract entry's categories
                areas_in_entry = self.pd_df.SC[entry].split(sep=';')
                # For each category in list 'areas_in_entry', update (area, year) pair
                for this_area in range(0,len(areas_in_entry)):
                    # Increase publication count for (area, year) pair
                    unique_wos_research_areas_stats.loc[self.pd_df.PY[entry],areas_in_entry[this_area]] += 1
        #
        unique_wos_research_areas_stats.loc['Total',:] = unique_wos_research_areas_stats.iloc[:-1,:].sum()
        #
        unique_wos_research_areas_stats = unique_wos_research_areas_stats.transpose().sort_values(by=['Total'], ascending=False)
        self.unique_wos_research_areas_stats = unique_wos_research_areas_stats.transpose()
    
    def plot_pub_per_year(self, norm=False):
        
        #
        valid_entries=self.unique_years!=None
        #
        fig = plt.figure(figsize=(22,12))
        if norm:
            plt.bar(self.unique_years[valid_entries],self.pub_per_year[valid_entries]/self.pub_per_year.sum())
            plt.ylabel('Proportion of publications')
        else:
            plt.bar(self.unique_years[valid_entries],self.pub_per_year[valid_entries])
            plt.ylabel('Number of publications')
        plt.xlabel('Publication year')
        
        plt.show()
        
    def plot_pub_per_country(self, norm=False, log_scale=False):
        
        #
        country_list_sorted = self.country_pub_per_year.loc['Total'].sort_values(ascending=False).index
        total_pub_per_country_sorted = self.country_pub_per_year.loc['Total'].sort_values(ascending=False).values
        #
        fig = plt.figure(figsize=(22,12))
        if norm:
            plt.bar(country_list_sorted, total_pub_per_country_sorted/total_pub_per_country_sorted.sum())
            plt.ylabel('Proportion of publications')
        else:
            plt.bar(country_list_sorted, total_pub_per_country_sorted)
            plt.ylabel('Number of publications')
        if log_scale:
            plt.yscale('log')
        plt.xlabel('Country')
        plt.xticks(rotation='vertical')
    
    def plot_country_pub_per_year(self, norm=False):

        #
        country_list_sorted = self.country_pub_per_year.loc['Total'].sort_values(ascending=False).index
        total_pub_per_country_sorted = self.country_pub_per_year.loc['Total'].sort_values(ascending=False).values
        years = self.country_pub_per_year.index[:-1].astype(float)
        #
        fig = plt.figure(figsize=(22,12))
        
        offset = np.zeros(len(country_list_sorted),)
        #
        for this_year in range(0,len((years))):
            #
            values = self.country_pub_per_year.iloc[this_year]
            #
            if norm:
                #
                values = values/total_pub_per_country_sorted.sum()
                #
                plt.bar(country_list_sorted, values, bottom=offset, label=years[this_year])
            else:
                #
                plt.bar(country_list_sorted, values, bottom=offset, label=years[this_year])
            #
            offset += values
        #
        plt.xlabel('Country')
        if norm:
            plt.ylabel('Proportion of publications')
        else:
            plt.ylabel('Number of publications')
        #
        plt.xticks(rotation='vertical')
        plt.legend()
        plt.show()
        
    def plot_treemap_wos_categories_total(self, show_labels=True):
        
        #
        a=self.unique_wos_categories_stats.loc['Total']
        b=pd.DataFrame({'categories':a.index,'values':a.values})
        #
        fig = plt.figure(figsize=(22,12))
        if show_labels:
            squarify.plot(sizes=b['values'], label=b['categories'], alpha=.8 )
        else:
            squarify.plot(sizes=b['values'], alpha=.8 )
        plt.axis('off')
        plt.show()
    
    def plot_treemap_wos_research_areas_total(self, show_labels=True):
        
        #
        a=self.unique_wos_research_areas_stats.loc['Total']
        b=pd.DataFrame({'categories':a.index,'values':a.values})
        #
        fig = plt.figure(figsize=(22,12))
        if show_labels:
            squarify.plot(sizes=b['values'], label=b['categories'], alpha=.8)
        else:
            squarify.plot(sizes=b['values'], alpha=.8)
        plt.axis('off')
        plt.show()