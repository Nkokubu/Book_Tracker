import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


GENRE_FILE = "genre_colors.json"



def save_genre_colors(genre_color_dict):
    with open(GENRE_FILE, 'w') as f:
        json.dump(genre_color_dict, f, indent=4)

# Initialize genre-color mapping with a fresh start
genre_color_dict = {
    'Fantasy': 'purple',
    'Science Fiction': 'blue',
    'Romance': 'red'
}

FILE_NAME = 'book_log.csv'

# Create the CSV file if it doesn't exist yet
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=['Title', 'Author', 'Pages', 'Genre', 'Date Finished'])
    df.to_csv(FILE_NAME, index=False)

def plot_by_genre():
    df = pd.read_csv(FILE_NAME)
    df['Date Finished'] = pd.to_datetime(df['Date Finished'], errors='coerce')

    if df.empty:
        print("No data to analyze.")
        return

    # Show available genres
    print("Available genres:")
    for genre in genre_color_dict:
        print(f" - {genre}")

    genre_filter = input("Enter genre to visualize (or press Enter to show all): ").strip()

    if genre_filter:
        # Normalize for comparison
        genre_filter_normalized = genre_filter.lower().strip()
        filtered_df = df[df['Genre'].str.lower().str.strip() == genre_filter_normalized]

        if filtered_df.empty:
            print(f"No books found for genre: {genre_filter}")
            return

        # Standardize genre format for color lookup and title
        genre_filter_proper = genre_filter.title().strip()
        color = genre_color_dict.get(genre_filter_proper, 'darkorange')
        title = f'Pages Read Per Month (Genre: {genre_filter_proper})'
        df = filtered_df
    else:
        color = 'steelblue'
        title = 'Pages Read Per Month (All Genres)'

    df['Month'] = df['Date Finished'].dt.to_period('M')
    genre_stats = df.groupby('Month')['Pages'].sum().sort_index()

    plt.figure(figsize=(10, 6))
    genre_stats.plot(kind='bar', color=color)
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Pages')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()
def add_book():
    title = input("Book title: ")
    author = input("Author: ")
    pages = int(input("Number of pages: "))
    genre = input("Genre: ")
    date_str = input("Date finished (YYYY-MM-DD): ")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format.")
        return

    new_entry = pd.DataFrame([{
        'Title': title,
        'Author': author,
        'Pages': pages,
        'Genre': genre,
        'Date Finished': date
    }])

    df = pd.read_csv(FILE_NAME)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    print("Book added!")

def import_from_csv():
    file_path = input("Enter path to CSV file: ").strip()
    try:
        imported = pd.read_csv(file_path)
        required = {'Title', 'Author', 'Pages', 'Genre', 'Date Finished'}
        if not required.issubset(imported.columns):
            print("Missing required columns.")
            return
        imported['Date Finished'] = pd.to_datetime(imported['Date Finished'], errors='coerce')
        existing = pd.read_csv(FILE_NAME)
        combined = pd.concat([existing, imported], ignore_index=True).drop_duplicates()
        combined.to_csv(FILE_NAME, index=False)
        print("Import successful!")
    except Exception as e:
        print(f"Error during import: {e}")

def list_books():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No books found.")
    else:
        print(df)

def plot_progress():
    df = pd.read_csv(FILE_NAME)
    df['Date Finished'] = pd.to_datetime(df['Date Finished'], errors='coerce')

    if df.empty:
        print("No data to plot.")
        return

    df['Month'] = df['Date Finished'].dt.to_period('M')
    df['Genre'] = df['Genre'].str.strip().str.title()

    # Filter genres to ones actually defined in GENRE_COLORS
    df = df[df['Genre'].isin(genre_color_dict.keys())]

    # Group by Month and Genre, then pivot for stacked bar chart
    genre_monthly = df.groupby(['Month', 'Genre'])['Pages'].sum().unstack(fill_value=0).sort_index()

    # Get colors in same order as columns
    colors = [genre_color_dict.get(genre, 'gray') for genre in genre_monthly.columns]

    # Plot stacked bar chart with genre-based colors
    genre_monthly.plot(kind='bar', stacked=True, color=colors, figsize=(12, 7))

    plt.title('Pages Read Per Month by Genre')
    plt.xlabel('Month')
    plt.ylabel('Pages')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_genre_distribution():
    df = pd.read_csv(FILE_NAME)
    df['Genre'] = df['Genre'].str.strip().str.title()

    if df.empty:
        print("No data to visualize.")
        return

    genre_counts = df['Genre'].value_counts()
    colors = [genre_color_dict.get(genre, 'gray') for genre in genre_counts.index]

    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts, labels=genre_counts.index, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Overall Genre Distribution')
    plt.axis('equal')  # Keeps the pie chart round
    plt.tight_layout()
    plt.show()

def show_genre_summary_chart():
    df = pd.read_csv(FILE_NAME)
    df['Genre'] = df['Genre'].str.strip().str.title()
    df['Date Finished'] = pd.to_datetime(df['Date Finished'], errors='coerce')

    if df.empty:
        print("No data to visualize.")
        return

    print("Choose chart type:")
    print("1. Pie Chart (Overall Genre Distribution)")
    print("2. Bar Chart (Pages per Genre by Month)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        genre_counts = df['Genre'].value_counts()
        colors = [genre_color_dict.get(g, 'gray') for g in genre_counts.index]

        plt.pie(genre_counts, labels=genre_counts.index, colors=colors, autopct='%1.1f%%')
        plt.title('Overall Genre Distribution')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        df['Month'] = df['Date Finished'].dt.to_period('M')
        genre_monthly = df.groupby(['Month', 'Genre'])['Pages'].sum().unstack(fill_value=0).sort_index()
        colors = [genre_color_dict.get(genre, 'gray') for genre in genre_monthly.columns]

        genre_monthly.plot(kind='bar', stacked=True, color=colors, figsize=(12, 7))
        plt.title('Pages Read Per Month by Genre')
        plt.xlabel('Month')
        plt.ylabel('Pages')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y')
        plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
    else:
        print("Invalid selection.")
def show_genre_summary_chart_filtered():
    df = pd.read_csv(FILE_NAME)
    df['Date Finished'] = pd.to_datetime(df['Date Finished'], errors='coerce')

    if df.empty:
        print("No data available.")
        return

    try:
        year_input = input("Enter year to analyze (e.g. 2024): ").strip()
        year = int(year_input)
    except ValueError:
        print("Invalid year.")
        return

    df = df[df['Date Finished'].dt.year == year]

    if df.empty:
        print(f"No data found for year {year}.")
        return

    quarter_input = input("Enter quarter to analyze (1-4) or press Enter to skip: ").strip()
    if quarter_input:
        try:
            quarter = int(quarter_input)
            if quarter not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            print("Invalid quarter.")
            return

        df = df[df['Date Finished'].dt.quarter == quarter]

        if df.empty:
            print(f"No data found for Q{quarter} {year}.")
            return

    print("Choose chart type:")
    print("1. Pie Chart (Genre Distribution)")
    print("2. Bar Chart (Pages per Genre by Month)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        genre_counts = df['Genre'].value_counts()
        colors = [genre_color_dict.get(genre, 'gray') for genre in genre_counts.index]
        plt.figure(figsize=(8, 6))
        plt.pie(genre_counts, labels=genre_counts.index, colors=colors, autopct='%1.1f%%')
        title = f"Genre Distribution - {year}"
        if quarter_input:
            title += f" Q{quarter}"
        plt.title(title)
        plt.show()
    elif choice == "2":
        df['Month'] = df['Date Finished'].dt.to_period('M')
        genre_stats = df.groupby(['Month', 'Genre'])['Pages'].sum().unstack(fill_value=0)
        genre_stats.plot(kind='bar', stacked=True, figsize=(10, 6), color=[
            genre_color_dict.get(genre, 'gray') for genre in genre_stats.columns
        ])
        title = f"Pages per Genre by Month - {year}"
        if quarter_input:
            title += f" Q{quarter}"
        plt.title(title)
        plt.ylabel("Pages Read")
        plt.xlabel("Month")
        plt.tight_layout()
        plt.show()
    else:
        print("Invalid choice.")
def show_avg_pages_per_genre_per_quarter():
    df = pd.read_csv(FILE_NAME)
    df['Date Finished'] = pd.to_datetime(df['Date Finished'], errors='coerce')
    df.dropna(subset=['Date Finished', 'Pages', 'Genre'], inplace=True)
    
    df['Quarter'] = df['Date Finished'].dt.to_period('Q')
    df['Genre'] = df['Genre'].str.strip().str.title()

    if df.empty:
        print("No data available.")
        return

    avg_pages = df.groupby(['Quarter', 'Genre'])['Pages'].mean().unstack().fillna(0)

    print("\nAverage Pages Per Genre Per Quarter:")
    print(avg_pages.round(1))

    # Optional: heatmap visualization
    plt.figure(figsize=(12, 6))
    avg_pages.T.plot(kind='bar', stacked=False, colormap='tab20', figsize=(12,6))
    plt.title("Average Pages per Genre per Quarter")
    plt.ylabel("Average Pages")
    plt.xlabel("Genre")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title="Quarter", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y')
    plt.show()

# genre_color_dict may already be defined globally like this:
genre_color_dict = {
    'Fantasy': 'purple',
    'Science Fiction': 'blue',
    'Romance': 'pink'
}

# Adding the new genre that does not exist:
def add_new_genre_color(genre_color_dict, new_genre, new_color):
    """
    Adds a new genre and color to the genre_color_dict if not already present.
    """
    if new_genre in genre_color_dict:
        print(f"{new_genre} already exists with color {genre_color_dict[new_genre]}.")
    else:
        genre_color_dict[new_genre] = new_color
        save_genre_colors(genre_color_dict)
        print(f"Added new genre: {new_genre} with color {new_color}.")

# ✅ Add this function to open a color picker dialog
def choose_color_gui():
    import tkinter as tk
    from tkinter import colorchooser
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    color_code = colorchooser.askcolor(title="Choose a Color")[1]
    return color_code

def rename_or_delete_genre(genre_color_dict):
    print("\nCurrent Genres:")
    for genre in genre_color_dict:
        print(f"- {genre}")
    
    choice = input("\nWould you like to (r)ename or (d)elete a genre? (r/d): ").strip().lower()
    
    if choice not in ['r', 'd']:
        print("Invalid choice.")
        return

    target_genre = input("Enter the genre name to modify: ").strip()
    
    if target_genre not in genre_color_dict:
        print(f"Genre '{target_genre}' not found.")
        return

    if choice == 'r':
        new_name = input("Enter the new name for this genre: ").strip()
        if new_name in genre_color_dict:
            print(f"Genre '{new_name}' already exists.")
            return
        genre_color_dict[new_name] = genre_color_dict.pop(target_genre)
        print(f"Renamed '{target_genre}' to '{new_name}'.")
    
    elif choice == 'd':
        confirm = input(f"Are you sure you want to delete '{target_genre}'? (y/n): ").strip().lower()
        if confirm == 'y':
            del genre_color_dict[target_genre]
            print(f"Deleted genre '{target_genre}'.")
        else:
            print("Deletion cancelled.")

    save_genre_colors(genre_color_dict)

def reorder_genres(genre_color_dict):
    """
    Allows the user to manually reorder the genres.
    """
    print("\nCurrent genre order:")
    genres = list(genre_color_dict.keys())
    for idx, genre in enumerate(genres, start=1):
        print(f"{idx}. {genre}")

    print("\nEnter the new order by specifying the current numbers separated by commas (e.g., 3,1,2):")
    try:
        new_order = input("New order: ").strip()
        indices = [int(i) - 1 for i in new_order.split(",")]
        if sorted(indices) != list(range(len(genres))):
            print("Invalid input. Please include each number exactly once.")
            return genre_color_dict

        reordered_dict = {genres[i]: genre_color_dict[genres[i]] for i in indices}
        save_genre_colors(reordered_dict)  # Re-save the new order to JSON
        print("Genres reordered successfully.")
        return reordered_dict
    except Exception as e:
        print(f"Error: {e}")
        return genre_color_dict

def edit_or_delete_book():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No books available to edit or delete.")
        return

    print("\nCurrent Book List:")
    for idx, row in df.iterrows():
        print(f"{idx+1}. {row['Title']} by {row['Author']} ({row['Pages']} pages, {row['Genre']}, Finished: {row['Date Finished']})")

    try:
        choice = int(input("\nEnter the number of the book to modify: ")) - 1
        if choice < 0 or choice >= len(df):
            print("Invalid number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    print("\nWhat would you like to do?")
    print("1. Edit this book")
    print("2. Delete this book")
    action = input("Enter 1 or 2: ").strip()

    if action == "1":
        print("Leave blank to keep current value.")
        title = input(f"New title (current: {df.at[choice, 'Title']}): ").strip()
        author = input(f"New author (current: {df.at[choice, 'Author']}): ").strip()
        pages = input(f"New page count (current: {df.at[choice, 'Pages']}): ").strip()
        genre = input(f"New genre (current: {df.at[choice, 'Genre']}): ").strip()
        date_finished = input(f"New date finished (YYYY-MM-DD, current: {df.at[choice, 'Date Finished']}): ").strip()

        if title:
            df.at[choice, 'Title'] = title
        if author:
            df.at[choice, 'Author'] = author
        if pages:
            try:
                df.at[choice, 'Pages'] = int(pages)
            except ValueError:
                print("Invalid page number. Keeping original.")
        if genre:
            df.at[choice, 'Genre'] = genre
        if date_finished:
            try:
                df.at[choice, 'Date Finished'] = pd.to_datetime(date_finished).date()
            except ValueError:
                print("Invalid date format. Keeping original.")

        print("Book updated.")

    elif action == "2":
        confirm = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
        if confirm == 'y':
            df = df.drop(index=choice).reset_index(drop=True)
            print("Book deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("Invalid action.")

    df.to_csv(FILE_NAME, index=False)


def main():
# Load the initial genre-color dictionary (start fresh or modify here)
    genre_color_dict = {
    'Fantasy': 'purple',
    'Science Fiction': 'blue',
    'Romance': 'red'
    }
    
    while True:
        print("\n📚 Book Reading Tracker")
        print("1. Add a book")
        print("2. Edit or delete a book")
        print("3. Show all books")
        print("4. Import from CSV")
        print("5. Show overall reading graph")
        print("6. Show genre summary chart (Pie or Bar)")
        print("7. Show filtered chart by year and quarter")
        print("8. Show average pages per genre per quarter")
        print("9. Add new genre and color")
        print("10. Rename or delete a genre")
        print("11. Reorder genre list manually")
        print("12. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_or_delete_book()
        elif choice == "3":
            list_books()
        elif choice == "4":
            import_from_csv()
        elif choice == "5":
            plot_progress()
        elif choice == "6":
            show_genre_summary_chart()
        elif choice == "7":
            show_genre_summary_chart_filtered()
        elif choice == "8":
            show_avg_pages_per_genre_per_quarter()
        elif choice == "9":
            new_genre = input("Enter the new genre name: ").strip()
            print("A color picker will open. Please select a color for this genre.")
            new_color = choose_color_gui()
            if new_color:
                add_new_genre_color(genre_color_dict, new_genre, new_color)
            else:
                print("No color selected. Genre was not added.")
        elif choice == "10":
            rename_or_delete_genre(genre_color_dict)
        elif choice == "11":
            genre_color_dict = reorder_genres(genre_color_dict)
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
        
# ✅ This line should be the very last line in the file
if __name__ == "__main__":
    main()
 
