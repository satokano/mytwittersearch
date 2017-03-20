import twitter
import config

api = twitter.Api(consumer_key=config.config['consumer_key'],
                  consumer_secret=config.config['consumer_secret'],
                  access_token_key=config.config['access_token_key'],
                  access_token_secret=config.config['access_token_secret'])

print(api.VerifyCredentials())

# Searchだと鍵垢はfromに指定しても取れない
#results = api.GetSearch(raw_query="q=from%3Akabao&result_type=recent&count=100")
#print(len(results))

#for r in results:
#    print(r.text + " / " + r.user.name + "(" + r.user.screen_name + ")")

len_all = 0

### 初回
results = api.GetUserTimeline(screen_name=config.config['screen_name_for_search'], count=200, include_rts=1)
len_results = len(results)
len_all += len_results
#print(len_results)

min_tweet_id = min(int(r.id_str) for r in results)
#print(min_tweet_id)

for r in results:
    print(r.id_str + ", " + r.created_at + ", " + r.text)

### 2回目以降
while True:
    results = api.GetUserTimeline(screen_name=config.config['screen_name_for_search'], count=200, include_rts=1, max_id=min_tweet_id - 1)
    len_results = len(results)
    len_all += len_results

    if (len_results == 0):
        break

    min_tweet_id = min(int(r.id_str) for r in results)
    #print(min_tweet_id)

    # TODO: MongoDBへの書き込みを追加する

    for r in results:
        print(r.id_str + ", " + r.created_at + ", " + r.text)

print(len_all)
