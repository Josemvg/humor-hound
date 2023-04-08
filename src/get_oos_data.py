from data_augmentation.data_augmentation import Data_augmentation

def main():
    """
    Calls the Data_augmentation class to augment the dataset.
    """
    data_augmentation = Data_augmentation()

    # Get the titles of articles from the news websites
    data = data_augmentation.get_news_titles()

    # Preprocess the data
    data = data_augmentation.preprocess_data(data)

    # Save the data to a CSV file
    data_augmentation.save_data(data, 'Sarcasm_Headlines_Dataset_OOS.csv')

if __name__ == '__main__':
    main()