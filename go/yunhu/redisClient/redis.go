package redisclient

import (
	"github.com/go-redis/redis"
	"time"
)

func RedisBegin() *redis.Client {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "192.168.1.10:31328",
		Password: "", // no password set
		DB:       9,  // use default DB
	})
	return rdb
}

func RedisSet(rdb *redis.Client, key string, value string) {
	err := rdb.Set(key, value, time.Hour).Err()
	if err != nil {
		panic(err)
	}
}

func RedisGet(rdb *redis.Client, key string) string {
	val, err := rdb.Get(key).Result()
	if err == redis.Nil {
		return ""
	} else if err != nil {
		panic(err)
	}
	return val
}

func RedisDel(rdb *redis.Client, key string) {
	err := rdb.Del(key).Err()
	if err != nil {
		panic(err)
	}
}
