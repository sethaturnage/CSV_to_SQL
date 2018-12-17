# CSV_to_SQL

This Python program emerged in response to the fact that I had to manually insert an entire database from Microsoft Access into Oracle SQL-server. Rather than inserting 100's of tuples manually, like the rest of my class, I opted to write a script to automate this process.

I exported each table as a .csv file, and placed them in a folder, 'CSV'. Then, I wrote a Python script to read files within this folder, along with their respective delimeters, and generate two SQL files: one to create the tables, and another to insert the data. By doing this, I hoped to avoid the unnecessary doldrum of manually inserting this data by hand.

However, the code presents several challenges. The primary challenge is to determine the SQL data-type from the text along, and then properly insert it into the Tuple. Also challenging is finding a quick way to automate specifiers such as "not null", and to detect foreign keys and primary keys, which the code currently does not do. There are manual inputs to do this, but they have been commented out for debugging purposes. 

I will continue to work on this program, iteratively resolving these issues. In the mean time, the output isn't perfect: so stay tuned for updates.
