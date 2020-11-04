for tweet in tweets:
    if (tweet != ""):
        try:
            response = nlu.analyze(
                        text=tweet,
                        features = Features(categories = CategoriesOptions(limit=6))
                    ).get_result()
            print(tweet)
            print(json.dumps(response, indent=2))
            tagged_data.append({"tweet": tweet, "tags": response})
        except ApiException as ex:
            print("Method failed with status code", str(ex.code), ": ", ex.message)
with open(tagged_path, 'w') as out_path:
    json.dump(tagged_data, out_path, indent=4)