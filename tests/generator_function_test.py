def test_provider_info():
    tweet_info = {'tweet_id': 123}

    provider_info = []
    assert(next((j for j, item in enumerate(provider_info) if item["tweet_id"] == 123), None) is None)

    provider_info.append(tweet_info)
    assert(next((j for j, item in enumerate(provider_info) if item["tweet_id"] == 123), None) == 0)

    provider_info.append({'tweet_id': 456})
    assert(next((j for j, item in enumerate(provider_info) if item["tweet_id"] == 456), None) == 1)

def test_generator_close_company():    
    j = 0
    [for k in (j + ord('close'[i]) for i in range(0, 5))]
    print(j)
