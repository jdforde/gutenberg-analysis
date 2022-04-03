"""
 most prolific authors by language ? 
"""
import pandas as pd
from matplotlib import pyplot as plt
from collections import OrderedDict

df = pd.read_csv('gutenberg.csv')


print(df['Num_Downloads'].sum())

## Top 5 Most Downloaded
# print(df.sort_values(by='Num_Downloads', ascending=False)[0:5][['Title', 'Author', 'Num_Downloads']].to_string(index=False))

## Top 5 Authors
# print(df['Author'].value_counts()[0:5].to_string())

## Total Download Count
download_count = 0
# for index, row in df.iterrows():
#     download_count += int(row['Num_Downloads'])
# print(download_count)


## Pie chart of 5 most common genres and other
# subject_counts = (df['Subject1'].value_counts() + df['Subject2'].value_counts() + df['Subject3'].value_counts()).dropna().sort_values(ascending=False).reset_index()
# subject_counts.rename(columns={'index' : 'Subject', 0:'Count'}, inplace=True)
# num_displayable = 10
# other = 0
# for index, row in subject_counts[num_displayable+1:].iterrows():
#     other += int(row['Count'])

# fig1, ax1 = plt.subplots()
# ax1.pie(subject_counts['Count'][:num_displayable].to_list() + [other], labels=subject_counts['Subject'][:num_displayable].to_list() + ['Other'])
# ax1.axis('equal')
# plt.show()

# print(subject_counts[])


## Pie chart of language breakdown
# language_counts = df['Language'].value_counts().dropna().reset_index()
# language_counts.rename(columns={'index': 'Language', 'Language' : 'Count'}, inplace=True)
# num_displayable = 8
# other = 0
# for index, row in language_counts[num_displayable+1:].iterrows():
#     other+= int(row['Count'])

# fig2, ax2 = plt.subplots()
# ax2.pie(language_counts[:num_displayable]['Count'].to_list() + [other], labels=language_counts[:num_displayable]['Language'].to_list() + ['Other'])
# plt.show()

## Violin plot of number of downloads for minor languages
# violin_list = []
# for language in ['French', 'Finnish', 'German', 'Italian', 'Dutch']:
#     violin_list.append(df[(df['Language'] == language) & (df['Num_Downloads'] > 100)]['Num_Downloads'].tolist())
# fig3, ax3 = plt.subplots()
# ax3.violinplot(violin_list)
# plt.show()

## Violin plot for English only
# fig4, ax4 = plt.subplots()
# ax4.violinplot(df[(df['Language'] == 'English') & (df['Num_Downloads'] > 8000)]['Num_Downloads'])
# plt.show()

## Bar plot for avg word length by language
# language_dict = {}
# for language in ['English', 'French', 'Finnish', 'German', 'Italian', 'Spanish']:
#     language_dict[language] = df[(df['Language'] == language) & (df['Word_Count'] != 17) & (df['Word_Count'] != 0)]['Word_Count'].mean()

# fig4, ax4 = plt.subplots()
# ax4.bar(['English', 'French', 'Finnish', 'German', 'Italian', 'Spanish'], language_dict.values())
# plt.show()


## Line plot of number of books on site broken down by top 6 languages over time 
# fig5, ax5 = plt.subplots()
# ax5.set_xticks(range(1, len(df)+1, 800))

# data = []
# for language in ['English', 'French', 'Finnish', 'German', 'Italian', 'Spanish']:
#     data.append((df[df['Language'] == language]['Release_Date'].sort_values()))

# for language in data:
#     ax5.plot_date(language, range(1, len(language)+1))
# plt.show()

fig5, ax5 = plt.subplots()
years = range(1971, 2023)
for language in ['English', 'French', 'Finnish', 'German', 'Italian', 'Spanish']:
    ordered_release = df[df['Language'] == language]['Release_Date'].sort_values()
    year_dict = OrderedDict().fromkeys(years, 0)
    for row in ordered_release:
        year = row[:row.index('-')]
        year_dict[int(year)] += 1


    cum_sum = []
    sum = 0
    for item in year_dict.values():
        sum += item
        cum_sum.append(sum)

    print(year_dict)
    
    ax5.plot(years, cum_sum)
plt.show()


