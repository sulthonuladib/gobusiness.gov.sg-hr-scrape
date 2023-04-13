import camelot
import pandas as pd

to_update = pd.read_csv('./out/hr_data.csv')

pdf_urls = []
for i in range(len(to_update)):
    url = to_update.values[i][4]
    pdf_urls.append(url)

print(len(pdf_urls))

counter = 1;
cost_item = []

# extract pdf
for url in pdf_urls:
    # parsing filename
    print('\n\n\nDownloading PDF in URL:', url)
    file_name = url.split('/').pop().replace('pdf', 'csv')

    # save unreadable csv, can read with camelot
    print('\nSaving raw unreadable csv at: ', 'tmp/' + file_name)
    raw_tables = camelot.read_pdf(url)
    raw_tables[0].to_csv('tmp/' + file_name)

    # read unreadable csv as dataframe with pandas
    print('\nReading CSV: ', 'tmp/' + file_name)
    result = pd.read_csv('tmp/' + file_name).values[0][0]
    print('saved pdf number', counter)
    cost_item.append(result)
    counter = counter + 1

# writing new csv after update with cost item from pdf
print("add updated cost item column from pdf")
to_update['Cost Item'] = cost_item

print("save new updated csv")
to_update.to_csv("out/hr_data_updated.csv", index=False)
