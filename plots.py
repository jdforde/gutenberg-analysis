"""
 most prolific authors by language ? 
"""
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('gutenberg.csv')

## Top 5 Most Downloaded
# print(df.sort_values(by='Num_Downloads', ascending=False)[0:5][['Title', 'Author', 'Num_Downloads']])

## Top 5 Authors
# print(df['Author'].value_counts()[0:5])

## Total Download Count
# download_count = 0
# for index, row in df.iterrows():
#     download_count += int(row['Num_Downloads'])
# print(download_count)


## Pie chart of 5 most common genres and other
# subject_counts = (df['Subject1'].value_counts() + df['Subject2'].value_counts() + df['Subject3'].value_counts()).dropna().sort_values(ascending=False).reset_index()
# subject_counts.rename(columns={'index' : 'Subject', 0:'Count'}, inplace=True)
# num_displayable = 5
# other = 0
# for index, row in subject_counts[num_displayable+1:].iterrows():
#     other += int(row['Count'])

# fig1, ax1 = plt.subplots()
# ax1.pie(subject_counts['Count'][:num_displayable].to_list() + [other], labels=subject_counts['Subject'][:num_displayable].to_list() + ['Other'])
# ax1.axis('equal')
# plt.show()


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
# for language in ['French', 'Finnish', 'German', 'Italian', 'Spanish']:
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
# ax5.axes.get_xaxis().set_visible(False)
# test_seq = range(1, len(df) + 1)
# data = []
# for language in ['English', 'French', 'Finnish', 'German', 'Italian', 'Spanish']:
#     data.append((df[df['Language'] == language]['Release_Date'].sort_values()))

# for language in data:
#     ax5.plot_date(language, range(1, len(language)+1))
# plt.show()