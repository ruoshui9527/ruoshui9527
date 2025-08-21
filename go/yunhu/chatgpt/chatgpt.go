package chatgpt

import (
	"bytes"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/go-redis/redis"
	"github.com/yhchat/bot-go-sdk/openapi"
	"github.com/yhchat/bot-go-sdk/subscription"
	"io/ioutil"
	"net/http"
	"strings"
	"yunhu/redisClient"
)

type pushChat struct {
	Id             string `json:"id"`
	ConversationId string `json:"conversation_id"`
	Model          string `json:"model"`
	Jailbreak      string `json:"jailbreak"`
	WebSearch      bool   `json:"web_search"`
	Provider       string `json:"provider"`
	Messages       []struct {
		Role    string `json:"role"`
		Content string `json:"content"`
	} `json:"messages"`
}

type MessageHistory struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type sendChat struct {
	Type    string `json:"type"`
	Content string `json:"content"`
	Error   string `json:"error"`
}

var rdb *redis.Client

func ChatGptBegin() {
	rdb = redisclient.RedisBegin()
	port := 30000
	subscription := subscription.NewSubscription(port)
	subscription.OnMessageNormal = onMessageNormal
	subscription.OnMessageInstruction = onMessageInstruction
	subscription.Start()

}

func onMessageInstruction(event subscription.MessageEvent) {
	//清除记忆
	if event.Message.CommandId == 471 {
		redisclient.RedisDel(rdb, event.Sender.SenderId)
		send(event.Sender.SenderId, "记忆已清除")
	}
}

func onMessageNormal(event subscription.MessageEvent) {
	id := generateRandomString(16)
	var senderId = event.Sender.SenderId
	var content = event.Message.Content["text"].(string) + " \n 使用中文答复"

	marshalContent := assemblyHistory(senderId, content, "user")
	var chart pushChat
	err2 := json.Unmarshal(marshalContent, &chart.Messages)
	if err2 != nil {
		panic(err2)
	}

	chat := pushChat{
		Id:             id,
		ConversationId: id,
		Model:          "",
		Jailbreak:      "default",
		WebSearch:      false,
		Provider:       "",
		Messages:       chart.Messages,
	}

	marshal, err := json.Marshal(chat)
	if err != nil {
		panic(err)
	}

	/*	client := &http.Client{
		Timeout: 60 * time.Second,
	}*/

	resp, err := http.Post("http://192.168.1.10:3000/backend-api/v2/conversation", "application/json", bytes.NewBuffer(marshal))
	if err != nil || resp.StatusCode != 200 {
		send(senderId, err.Error())
		panic(err)
	}

	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		messageJoin(resp, senderId)
	}

}

func messageJoin(resp *http.Response, id string) {
	all, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		send(id, err.Error())
		panic(err)
	}

	fmt.Printf("%s", all)

	var contents strings.Builder

	for _, line := range bytes.Split(all, []byte("\n")) {
		var chat sendChat
		if err := json.Unmarshal(line, &chat); err == nil {
			if chat.Type == "content" {
				contents.WriteString(chat.Content)
			} else {
				contents.WriteString(chat.Error)
			}
		}
	}

	send(id, contents.String())

}

func send(senderId string, content string) {
	openapi := openapi.NewOpenApi("token")
	_, err := openapi.SendMessage(senderId, "user", "text", map[string]interface{}{"text": content})
	if err != nil {
		panic(err)
	}
	assemblyHistory(senderId, content, "assistant")
}

func generateRandomString(length int) string {
	bytes := make([]byte, length)
	_, err := rand.Read(bytes)
	if err != nil {
		panic(err)
	}
	return hex.EncodeToString(bytes)
}

func assemblyHistory(senderId, content, role string) []byte {
	getContent := redisclient.RedisGet(rdb, senderId)
	var messages []MessageHistory
	err2 := json.Unmarshal([]byte(getContent), &messages)

	if err2 != nil {
		fmt.Println(err2)
	}

	if role == "user" && len(messages) >= 10 {
		redisclient.RedisDel(rdb, senderId)
		messages = nil
	}

	// 创建一个新的消息
	newMessage := MessageHistory{
		Role:    role,
		Content: content,
	}

	messages = append(messages, newMessage)

	marshalContent, err := json.Marshal(messages)
	if err != nil {
		panic(err)
	}
	redisclient.RedisSet(rdb, senderId, string(marshalContent))
	return marshalContent
}
