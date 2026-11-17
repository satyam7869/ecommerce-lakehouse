import pandas as pd

df = pd.read_csv("data/samples/customers_sample_50rows.csv")

    # print("Dataset Shape:")
    #     print(df.shape)
    #
    #     print("\nColumn Names:")
    #     print(df.columns)
    #
    #     print("\nColumn Data Types:")
    #     print(df.dtypes)
    #
    #     print("\nComplete DataFrame Information:")
    #     df.info()
    #
    #     print("\nNull Values in Each Column:")
    #     print(df.isnull())
    #     print(df.isnull().sum())
    #     print(df.isnull().sum().sum())
    #
    #     print("\nDuplicate Rows in the DataFrame:")
    #     print(df.duplicated())
    #     print(df.duplicated().sum())
    #     print(df.duplicated(["customer_id"]).sum())
    #
    #     print("\nFirst 50 Rows of the DataFrame:")
    #     print(df.head(50))
    #     print(df.describe())

# print("\nNegative Lifetime Spend:")
# print(df[df["lifetime_spend"] < 0])
#
# print("\nZero Order Customers:")
# print(df[df["lifetime_orders"] == 0].head())
#
# print("\nSignup Date Samples:")
# print(df["signup_date"].head(10))
#
# print("\nSignup Date Data Type:")
# print(df["signup_date"].dtype)
#
# print("\nConverting 'signup_date' to datetime format...")
# df["signup_date"] = pd.to_datetime(df["signup_date"],format= "%Y-%m-%d", errors="raise")
# print("\nUpdated 'signup_date' Data Type:")
# print(df["signup_date"].dtype)
#
# print("\nDateColumn Summary Statistics:")
# print(df["signup_date"].describe())
# print(df["signup_date"].info())
