package xianbao

import (
	"fmt"
	"github.com/yhchat/bot-go-sdk/openapi"
)

func XianBaoBegin() {

	openApi := openapi.NewOpenApi("token")

	buttons := []openapi.Button{
		{
			Text:       "点击跳转原文",
			ActionType: 1,
			Url:        "http://new.ixbk.net",
		},
	}
	message := openapi.TextMessage{
		RecvId:   "527",
		RecvType: "user",
		Text:     "标题: ",
		Buttons:  buttons,
	}

	textMessage, err := openApi.SendTextMessage(message)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(textMessage)

	//fmt.Println(message)

}
